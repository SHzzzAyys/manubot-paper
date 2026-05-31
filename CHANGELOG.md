# Changelog

All notable changes to this repository are documented here. This project follows
a lightweight versioning convention for a reproducible research-writing workflow;
entries describe real changes only and make no claims about adoption or usage.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and the project aims to follow [Semantic Versioning](https://semver.org/) for
workflow milestones.

## [Unreleased]

## [0.1.0] - 2026-05-31

First public release of the manuscript workspace as an open, reproducible
research-writing workflow.

### Added
- Public-facing English `README.md` describing the workflow, scope, repository
  layout, and an explicit public-data boundary.
- `ROADMAP.md` outlining planned work: reference management, figure/table checks,
  CI, manuscript version control, and citation-consistency checks.
- Dual licensing: `CC-BY-4.0` for content (`LICENSE`, `LICENSE.md`) and `CC0-1.0`
  for code/data (`LICENSE-CC0.md`).
- Manubot manuscript sources under `content/`, structured evidence tables under
  `data/`, and validation/export scripts under `scripts/`.
- GitHub Actions and AppVeyor build configuration for the Manubot pipeline.
- CI build-status and license badges in the README.

### Changed
- Set the author affiliation in `content/metadata.yaml` to `Independent Researcher`
  in place of the template placeholder.

### Removed
- `docs/github-pr-demo.md`, a demonstration-only note that was not part of the
  manuscript toolchain.

[Unreleased]: https://github.com/SHzzzAyys/manubot-paper/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SHzzzAyys/manubot-paper/releases/tag/v0.1.0
