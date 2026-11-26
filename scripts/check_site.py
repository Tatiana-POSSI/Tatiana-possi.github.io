"""Check a rendered Quarto site for missing assets, metadata and review files."""

import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

MAIN_PAGES = (
    "index.html",
    "research/index.html",
    "teaching/index.html",
    "cv/index.html",
    "code/index.html",
    "notes/index.html",
)
PRIVATE_DIRECTORIES = ("templates", "private", "scripts", ".github")
PUBLIC_CV = "assets/documents/approved/rayda-tatiana-possi-tahabo-cv.pdf"
GOOGLE_VERIFICATION_FILE = "google41220a8d21a06f51.html"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = Counter()
        self.links = []
        self.meta = {}
        self.canonical = None
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        # Quarto gives its alternate theme stylesheets the same IDs.
        if (identifier := attrs.get("id")) and tag != "link":
            self.ids[identifier] += 1
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.meta[key] = attrs.get("content", "")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
            return
        for attribute in ("href", "src"):
            if target := attrs.get(attribute):
                self.links.append((tag, target))


def production_url(base, path):
    relative = path.removesuffix("index.html") if path.endswith("/index.html") else path
    if relative == "index.html":
        relative = ""
    return f"{base.rstrip('/')}/{relative}"


def check(root, base_url, review):
    errors = []
    external = set()
    path_prefix = urlsplit(base_url or "").path.rstrip("/")
    files = [path for path in root.rglob("*") if path.is_file()]
    relative_files = {path.relative_to(root).as_posix() for path in files}
    for name in sorted(relative_files):
        if (
            name.split("/")[0] in PRIVATE_DIRECTORIES
            or name.endswith((".qmd", ".ejs", ".ejs.md"))
            or name.startswith("assets/documents/review/")
        ):
            errors.append(f"Review or source material in the rendered site: {name}")
    required = set(MAIN_PAGES) | {"search.json", "references.bib", PUBLIC_CV, GOOGLE_VERIFICATION_FILE}
    if base_url:
        required.add("sitemap.xml")
    for missing in sorted(required - relative_files):
        errors.append(f"Missing expected output: {missing}")

    verification_file = root / GOOGLE_VERIFICATION_FILE
    if GOOGLE_VERIFICATION_FILE in relative_files:
        expected_marker = f"google-site-verification: {GOOGLE_VERIFICATION_FILE}".encode("ascii")
        if verification_file.read_bytes() != expected_marker:
            errors.append(f"Unexpected contents in {GOOGLE_VERIFICATION_FILE}")

    pages = {
        path.relative_to(root).as_posix(): Page(path)
        for path in files
        if path.suffix == ".html" and path != verification_file
    }
    for name, page in pages.items():
        for identifier, count in page.ids.items():
            if count > 1:
                errors.append(f"{name}: duplicate ID {identifier!r}")
        for key in ("description", "og:title", "og:description"):
            if not page.meta.get(key):
                errors.append(f"{name}: missing metadata {key}")
        if ("noindex" in page.meta.get("robots", "")) != review:
            errors.append(f"{name}: unexpected robots directive for this profile")
        if base_url:
            expected = production_url(base_url, name)
            if page.canonical != expected:
                errors.append(f"{name}: expected canonical address {expected}, got {page.canonical}")
            if not page.meta.get("og:image", "").startswith(base_url.rstrip("/") + "/"):
                errors.append(f"{name}: missing absolute Open Graph image")
        for tag, link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                if url.scheme in {"http", "https"} or url.netloc:
                    external.add((tag, link))
                continue
            path = unquote(url.path)
            if path.startswith("/"):
                if path_prefix and not (path == path_prefix or path.startswith(path_prefix + "/")):
                    errors.append(f"{name}: {link} falls outside the site path {path_prefix}/")
                    continue
                target = root / path[len(path_prefix):].lstrip("/")
            else:
                target = (root / name).parent / path if path else root / name
            target = target.resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f"{name}: unresolved local {tag} target {link!r}")
                continue
            target_name = target.relative_to(root).as_posix()
            if target_name in pages and url.fragment and unquote(url.fragment) not in pages[target_name].ids:
                errors.append(f"{name}: missing fragment {url.fragment!r} in {target_name}")

    index = root / "search.json"
    if index.exists():
        search = json.loads(index.read_text(encoding="utf-8"))
        indexed = {item["href"].split("#", 1)[0] for item in search}
        if not set(MAIN_PAGES).issubset(indexed):
            errors.append("Website search does not index all six main pages")
    if "sitemap.xml" in relative_files and base_url:
        sitemap = ElementTree.parse(root / "sitemap.xml")
        locations = Counter(element.text for element in sitemap.findall(".//{*}loc"))
        for name in pages:
            canonical = production_url(base_url, name)
            if locations.pop(canonical, 0) != 1:
                errors.append(f"{name}: expected exactly one sitemap entry for {canonical}")
        for location in locations:
            errors.append(f"Unexpected sitemap entry: {location}")

    for error in errors:
        print(error)
    if errors:
        raise SystemExit(f"{len(errors)} site check(s) failed.")
    print(f"Verified metadata, local links and profile boundaries for {len(pages)} HTML pages.")
    if external:
        print("External targets for review:")
        for tag, url in sorted(external):
            print(f"  {tag}: {url}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--site-url")
    parser.add_argument("--review", action="store_true")
    args = parser.parse_args()
    check(args.folder.resolve(), args.site_url, args.review)


if __name__ == "__main__":
    main()
