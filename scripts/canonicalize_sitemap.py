"""Use the same directory URLs in the sitemap as Quarto's canonical links."""

import os
from pathlib import Path
from xml.etree import ElementTree


NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


def main():
    path = Path(os.environ["QUARTO_PROJECT_OUTPUT_DIR"]) / "sitemap.xml"
    if not path.is_file():
        return

    ElementTree.register_namespace("", NAMESPACE)
    sitemap = ElementTree.parse(path)
    root = sitemap.getroot()
    entries = {}
    for entry in root.findall(f"{{{NAMESPACE}}}url"):
        location = entry.find(f"{{{NAMESPACE}}}loc")
        if location.text.endswith("/index.html"):
            location.text = location.text.removesuffix("index.html")
        # An incremental Quarto render can append an index.html alias that is newer.
        if location.text in entries:
            root.remove(entries[location.text])
        entries[location.text] = entry

    sitemap.write(path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
