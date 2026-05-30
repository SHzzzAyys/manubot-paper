# Cat Toxoplasma Vaccine Review Workflow

This repository is a reproducible research writing workflow for veterinary parasitology / Toxoplasma research.

It uses Manubot-style manuscript sources, structured evidence tables, validation scripts, and CI-oriented build configuration to maintain a review project on cat toxoplasmosis vaccine research. The goal is to make the literature review process inspectable: source text, evidence tables, references, generated outputs, and validation logic live together in one version-controlled workflow.

This repository does not claim broad adoption, production deployment, or a large user base. It is an open research workflow and manuscript workspace maintained for transparent veterinary-parasitology writing.

## Scope

- Reproducible manuscript authoring for a Toxoplasma vaccine review.
- Structured evidence tables for direct studies, support studies, and review literature.
- Lightweight validation scripts for manuscript structure and evidence-table consistency.
- Manubot build configuration for HTML, PDF, DOCX, and citation-aware output.
- Documentation for local setup, submission checks, and workflow maintenance.

## Repository Layout

- `content/`
  Manubot manuscript sections, front matter, study matrices, tables, timeline notes, and supplementary notes.
- `data/`
  Structured evidence CSV files and wording-profile configuration.
- `scripts/`
  Validation, evidence export, literature-search, and local workflow helpers.
- `docs/`
  Public workflow documentation, data dictionaries, manuscript maps, generated evidence tables, and toolchain notes.
- `build/`
  Pandoc, Manubot, template, and build assets.
- `ci/`
  Continuous-integration setup for manuscript building and optional AI-assisted revision workflows.
- `webpage/`
  Generated public manuscript webpage artifacts.
- `output/`
  Placeholder for generated manuscript outputs; most generated files are intentionally ignored.

## Public Data Boundary

The public repository intentionally excludes private contact information and personal academic planning drafts. It is meant to expose the reproducible manuscript workflow, not private planning material.

## Core Manuscript Files

- `content/00.front-matter.md`
- `content/01.abstract.md`
- `content/02.introduction.md`
- `content/03.methods.md`
- `content/04.results.md`
- `content/05.discussion.md`
- `content/06.core-table.md`
- `content/07.timeline.md`
- `content/08.conclusion.md`
- `content/09.study-matrix.md`
- `content/10.supplementary-notes.md`

## Evidence Tables

- `data/cat_toxo_vaccine_direct_studies.csv`
- `data/cat_toxo_vaccine_support_studies.csv`
- `data/cat_toxo_vaccine_reviews.csv`

Field definitions are documented in `docs/evidence-data-dictionary.md`.

## Common Commands

Export structured evidence tables:

```powershell
& ".\.venv\Scripts\python.exe" scripts\export_evidence_tables.py
```

Run manuscript validation:

```powershell
& ".\.venv\Scripts\python.exe" scripts\validate_manuscript.py
```

Run a local Manubot process check:

```powershell
$env:TZ='Etc/UTC'
$env:LC_ALL='en_US.UTF-8'
$env:PATH = ".\.venv\Scripts;" + $env:PATH
& ".\.venv\Scripts\manubot.exe" process --content-directory=content --output-directory=output --cache-directory=ci/cache --skip-citations --log-level=INFO
```

## Maintenance Status

The repository is actively maintained as a research-writing workflow. The current maintenance focus is evidence-table consistency, manuscript validation, CI build reliability, citation consistency, and clearer release/version-control practices for manuscript outputs.

## License

Repository content is licensed under Creative Commons Attribution 4.0 International (`CC-BY-4.0`) unless otherwise noted. See `LICENSE` and `LICENSE.md`.

Some upstream Manubot/rootstock template material is also distributed under `CC0-1.0`; see `LICENSE-CC0.md`.
