# Research Hub Workflow

This workflow summarizes public literature-search outputs, repository literature notes, and structured data inventories. It is intended for reproducible project maintenance and does not include private academic planning drafts.

## Entry Points

Refresh the daily Toxoplasma literature search and rebuild the public research hub:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_daily_toxo_search.ps1
```

Refresh only the literature intelligence layer and research hub:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_research_hub.ps1
```

## Generated Hub Files

The hub generator writes a compact set of Markdown and JSON files to the configured local output directory:

- `00-dashboard.md`
  Snapshot of recent daily-search reports and repository literature notes.
- `01-daily-search-log.md`
  Daily-search report index.
- `02-literature-note-log.md`
  Literature-note registry view.
- `03-data-assets-log.md`
  Data-table and output-folder inventory.
- `research-hub.json`
  Machine-readable summary for downstream automation.

## Wording Sanitizer

The wording sanitizer applies configured substitutions to public manuscript and workflow files:

```powershell
& ".\.venv\Scripts\python.exe" scripts\sanitize_wording.py --profile academic
& ".\.venv\Scripts\python.exe" scripts\sanitize_wording.py --profile daily
& ".\.venv\Scripts\python.exe" scripts\sanitize_wording.py --profile academic --dry-run
```

Default targets include:

- `content/`
- `docs/intelligence/`
- `docs/daily-toxo-search-workflow.md`
- `docs/research-hub-workflow.md`
- configured local daily-search outputs
- configured local research-hub outputs

## Boundary

- The hub summarizes existing public workflow outputs; it does not decide which evidence should be accepted into the manuscript.
- Private academic planning material should stay outside the public repository and outside generated public hub files.
- The wording sanitizer performs rule-based replacement only. It does not judge scientific nuance, so replacements still need human review.
