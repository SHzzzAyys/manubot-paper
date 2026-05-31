# Reproducibility Guide

This guide documents the public, repeatable workflow for checking the manuscript
workspace. It is intentionally limited to files that are safe to keep public.

## Scope

The repository is meant to make the writing workflow inspectable:

- manuscript source files live in `content/`;
- structured evidence tables live in `data/`;
- validation and export scripts live in `scripts/`;
- CI and build configuration live in `.github/workflows/`, `ci/`, and `build/`;
- generated public documentation lives in `docs/generated/` and `webpage/`.

Private thesis, proposal, defense, weekly-report, local workspace, and personal
contact artifacts are outside the reproducibility boundary.

## Local Environment

Recommended baseline:

- Git
- Python 3.11
- PowerShell on Windows, or Bash on Linux/macOS
- Pandoc when running the full Manubot process locally

Create a local virtual environment on Windows:

```powershell
python -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
& ".\.venv\Scripts\python.exe" -m pip install -r requirements-local.txt
```

Create a local virtual environment on Linux/macOS:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-local.txt
```

## Validation Commands

Run manuscript validation:

```powershell
& ".\.venv\Scripts\python.exe" scripts\validate_manuscript.py
```

Export evidence tables:

```powershell
& ".\.venv\Scripts\python.exe" scripts\export_evidence_tables.py
```

Export the research gap matrix:

```powershell
& ".\.venv\Scripts\python.exe" scripts\export_research_gap_matrix.py
```

Run wording sanitization if manuscript prose has been revised:

```powershell
& ".\.venv\Scripts\python.exe" scripts\sanitize_wording.py --profile academic
```

## Manubot Process Check

For a lightweight local process check that avoids citation-network instability:

```powershell
$env:TZ='Etc/UTC'
$env:LC_ALL='en_US.UTF-8'
$env:PATH = ".\.venv\Scripts;" + $env:PATH
& ".\.venv\Scripts\manubot.exe" process --content-directory=content --output-directory=output --cache-directory=ci/cache --skip-citations --log-level=INFO
```

The full CI workflow may run additional build, citation, artifact, and deployment
steps. Local success does not replace CI, but it catches common manuscript and
data-table errors before a pull request is opened.

## Expected Public Outputs

- `docs/generated/direct-cat-studies.md`
- `docs/generated/support-studies.md`
- `docs/generated/review-studies.md`
- `docs/generated/research-gap-matrix.md`
- `output/` artifacts from local or CI builds
- `webpage/` generated manuscript page artifacts

Generated outputs should be reviewed before release. Do not publish generated
files if they include private paths, private drafts, personal contact details, or
non-public review notes.
