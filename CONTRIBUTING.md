# Contributing

## Branching

- Use `main` for the stable manuscript state.
- Create short-lived branches for section revisions, figure updates, and reference cleanups.
- Prefer one pull request per topic.

## Writing Conventions

- Keep one sentence per line in manuscript source files.
- Put manuscript text in `content/*.md`.
- Do not manually edit generated files under `output/` or `webpage/`.
- Prefer DOI, PMID, PMCID, arXiv, ISBN, or URL citation keys instead of hand-written references.

## Pull Requests

- Describe what changed and why.
- Mention any sections that need scientific review.
- Note whether figures, tables, or references were added.
- Wait for the Manubot build to pass before merging.
- Confirm that no private contact information, local paths, thesis/proposal/defense drafts, or private planning material were added.
- For evidence-table changes, identify whether the source is a direct cat study, support study, review, or research-gap entry.

## Review Checklist

- scientific claim is supported
- citations resolve correctly
- headings and section order remain coherent
- figures and tables are referenced in the text
- public-data boundary remains intact
- validation commands in `docs/reproducibility.md` pass or the failure is explained

## Release Preparation

Before tagging a public release, follow `docs/public-release-checklist.md`.
Release notes should describe real workflow or manuscript changes only, without
unsupported claims about adoption, user counts, or production use.
