# Maintaining the academic website

Keep Quarto Markdown as the source of truth for public content. Apply changes within the existing page structure and design. Use Quarto's navigation, search, listings, MathJax and BibTeX support. Keep the serif headings, restrained navy and rust palette, thin rules, keyboard focus styles and both color schemes consistent.

## Academic content

- Check wording, names, institution, dates and status against the most recent material Rayda supplied. Record discrepancies for review. Keep factual statements concise.
- Use `research-type` in each research record. Add working papers, publications, talks, links and resources only with verified details. Show genuine fields only.
- Reuse `_academic.yml`, the research interests partial and the Quarto templates when applicable. Keep research entries, CV and profile metadata consistent.
- Keep vacant publication sections out of the public pages. Prefer useful descriptions of active areas over invented filler.

## Private material and publishing

- Keep the original and working CVs, unpublished research and datasets, private teaching resources, and any private contact information outside the repository.
- Verify explicit approval for the intended public email, photo and PDF CV. Remove PDF and photo metadata that could disclose local paths, precise location or other sensitive information. Keep approved and review assets in their respective locations.
- Keep the approved academic email in the HTML and PDF CV. Keep the university profile in the HTML contact area, and verify the website and professional profile links in the PDF. Use the approved LaTeX-formatted PDF as a static asset and retain its filename.
- Treat the Quarto render allowlist as the production content boundary. Keep templates and private examples outside it. Review the rendered output and search index for leaks.
- Work on a development branch and use a review PR when a repository is connected. Wait for Rayda's explicit approval before merging to `main`, changing visibility or enabling Pages. Keep the publication gate disabled until approval.
- Keep the Quarto project at the repository root and use `https://tatiana-possi.github.io/` in canonical metadata. The deployment job requires `main` and the `PAGES_PUBLISH` repository variable.

## Verification

Run `quarto render` and `python3 scripts/check_site.py _site --site-url https://tatiana-possi.github.io`. Check mobile and desktop in light and dark mode. Exercise the navigation, keyboard focus, search, CV download, mathematics and citations for pages affected by the change. For deployment changes, use actionlint and verify the configured Pages address. Document unexecuted checks and new content awaiting approval.
