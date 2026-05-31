param()

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$sanitizeScript = Join-Path $PSScriptRoot "sanitize_wording.py"

if (Test-Path $venvPython) {
    & $venvPython $sanitizeScript --profile academic
    exit $LASTEXITCODE
}

& py $sanitizeScript --profile academic
exit $LASTEXITCODE
