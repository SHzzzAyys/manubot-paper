# Open-Source Benchmark Notes

This document records which public repositories were reviewed before the
open-source maintenance files were added. Star counts were observed through
GitHub search/API on 2026-05-31 and will change over time. These counts describe
the benchmark repositories, not this repository.

## Repositories Reviewed

| Repository | Stars observed | Why it was relevant | Practice adapted here |
| --- | ---: | --- | --- |
| [`jupyter-book/jupyter-book`](https://github.com/jupyter-book/jupyter-book) | 4246 | Mature documentation tool for publication-quality computational documents. | Clear contribution, changelog, and release-oriented documentation. |
| [`the-turing-way/the-turing-way`](https://github.com/the-turing-way/the-turing-way) | 2149 | Open guide for reproducible, ethical, and collaborative data science. | Citation metadata, conduct expectations, and governance-style transparency adapted to a small repository. |
| [`greenelab/deep-review`](https://github.com/greenelab/deep-review) | 1276 | Collaborative Manubot review paper in a biomedical domain. | Manuscript-specific contribution guidance and review-centered workflow framing. |
| [`benmarwick/rrtools`](https://github.com/benmarwick/rrtools) | 716 | Tooling for writing reproducible research in a compendium style. | Environment and reproducibility documentation for local checks. |
| [`manubot/rootstock`](https://github.com/manubot/rootstock) | 478 | Canonical Manubot manuscript template. | Preserved the Manubot content/build/CI structure while adding project-specific public boundaries. |
| [`manubot/manubot`](https://github.com/manubot/manubot) | 473 | Core Manubot Python utilities. | Emphasis on validation commands, release traceability, and explicit workflow documentation. |

## Adaptation Principles

- Borrow structures, not claims. High-star repositories justify useful patterns,
  but they do not imply this repository has comparable adoption.
- Keep the public boundary explicit. A research-writing workflow can be open
  without exposing private drafts, contact information, or local workspace paths.
- Prefer small, reviewable files. Citation, conduct, security, reproducibility,
  and release-checklist documents are easier to audit than a large rewritten
  README.
- Keep maintenance evidence factual. A changelog, CI workflow, issue templates,
  and release checklist are verifiable; user-count or impact claims are not.

## Changes Added After Benchmarking

- `CITATION.cff` for GitHub citation metadata.
- `CODE_OF_CONDUCT.md` for professional, evidence-centered collaboration.
- `SECURITY.md` and a privacy-boundary issue template for safe reporting.
- `docs/reproducibility.md` for local validation and build checks.
- `docs/public-release-checklist.md` for branch, tag, release, and privacy review.
- README and contribution-template links to make these files discoverable.
