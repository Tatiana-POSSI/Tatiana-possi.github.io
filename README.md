# Tatiana POSSI

This Quarto website presents academic research, teaching and education. You can request changes in natural language. Point to the page, supply the approved information, and describe what should change.

## Local review

The site uses Quarto 1.11.9 and the Python 3 standard library for build verification. GitHub Pages serves the generated HTML, styles and assets directly.

```sh
quarto render
python3 scripts/check_site.py _site --site-url https://tatiana-possi.github.io
quarto preview --host 127.0.0.1
```

For a private review, render with `quarto render --profile review --output-dir _site-review` and serve that folder on loopback for website search and PDF downloads. The review profile adds a noindex directive. Both builds use the supplied portrait's web derivative and the privacy-safe PDF prepared in `assets/documents/approved/` for publication review.

## Maintain the website

| Update | Where it belongs |
| --- | --- |
| Name, appointment, affiliation or programme wording | `_academic.yml` and the corresponding page metadata and homepage Person record |
| Homepage introduction, research fields, education or honours | `index.qmd` |
| Professional contact links | `index.qmd`, `_quarto.yml` and the homepage Person record |
| Research page interests | `_includes/research-interests.qmd` |
| Thesis, paper or publication | `research/projects/` and `references.bib` |
| Course or activity record | `teaching/courses/` or `activities/entries/` |
| Approved public media | `assets/images/` or `assets/documents/approved/` |
| Appearance and site navigation | `styles/` and `_quarto.yml` |

The reusable Quarto files under `templates/` cover papers, course pages and talks. The render allowlist excludes those files. Keep private examples and unpublished content outside the tracked repository.

Research listings use each record’s `research-type` and `year`. Only types with approved entries appear.

Reconcile academic names and dates against the latest CV provided privately and record any discrepancies for review. Add a professional email only after Rayda approves that specific address. Verify supplied academic profile URLs. Web portraits need descriptive alternative text and stripped metadata.

To refresh the CV PDF, replace `assets/documents/approved/Rayda-Tatiana-Possi-Tahabo-CV.pdf` with the approved, privacy-checked LaTeX CV. Keep the filename stable. Quarto copies this static PDF into the site, and the build checks that the output matches the approved file byte for byte. Review the PDF text, links and metadata before requesting publication approval.

## Approve and publish through GitHub

The repository is [Tatiana-POSSI/Tatiana-possi.github.io](https://github.com/Tatiana-POSSI/Tatiana-possi.github.io). Quarto builds the canonical links and sitemap for [tatiana-possi.github.io](https://tatiana-possi.github.io/).

1. Review the proposed migration in the pull request. Confirm the site content and downloadable CV.
2. After explicit publication approval, switch **Settings → Pages → Build and deployment → Source** to **GitHub Actions** before merging the migration into `main`.
3. Under **Settings → Secrets and variables → Actions → Variables**, set `PAGES_PUBLISH` to `true` for the approved release. Merge the approved pull request or run **Build Quarto website** on `main` if a first deployment needs to be triggered manually.
4. Verify the workflow's deployment URL, navigation, search, portrait, contact links and PDF download. Later pushes to `main` deploy while `PAGES_PUBLISH` is enabled. Pull requests run the build and link checks.

Repository settings require an owner or administrator with permission to manage Pages and Actions variables. GitHub Free supports Pages from a public repository, so choose its visibility only after approval. A private repository can be used for review where the account and access permit it.

## Implementation references

This project was independently implemented. The academic template informed the page organization. The linked repository did not show a reuse license when reviewed.

- [Academic Quarto website reference](https://github.com/matdehaven/quarto-academic-website)
- [Quarto websites](https://quarto.org/docs/websites/)
- [Quarto GitHub Pages guide](https://quarto.org/docs/publishing/github-pages.html)
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

Source Serif 4 and Inter are self-hosted from their Fontsource variable packages. Their SIL Open Font Licenses are in `assets/fonts/`. The MathJax 3.2.2 browser assets and Apache license are in `assets/vendor/mathjax/`. Mathematical pages load MathJax only when they contain equations.
