# Local venv workflow

The repository now prefers a local `.venv` so local execution matches the GitHub Actions workflow more closely.

## Setup

### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_local_env.ps1
```

### Linux / macOS

```bash
bash scripts/setup_local_env.sh
```

## Common commands

### Windows PowerShell

```powershell
& ".\.venv\Scripts\python.exe" scripts\validate_manuscript.py
& ".\.venv\Scripts\python.exe" scripts\export_evidence_tables.py
& ".\.venv\Scripts\python.exe" scripts\export_thesis_assets.py
powershell -ExecutionPolicy Bypass -File scripts\run_manubot_process.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
python scripts/validate_manuscript.py
python scripts/export_evidence_tables.py
python scripts/export_thesis_assets.py
bash scripts/run_manubot_process.sh
```

## Notes

- CI uses `ci/requirements-ci.txt`.
- Local setup uses `requirements-local.txt`, which currently delegates to the same pinned dependency set.
- Local HTML/PDF export still requires `pandoc` to be installed on your machine.
