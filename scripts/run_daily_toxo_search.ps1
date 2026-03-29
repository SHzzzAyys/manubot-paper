param(
    [int]$Days = 7
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$scriptPath = Join-Path $PSScriptRoot "daily_toxo_vaccine_search.py"

if (Test-Path $venvPython) {
    & $venvPython $scriptPath --days $Days
    exit $LASTEXITCODE
}

& py $scriptPath --days $Days
exit $LASTEXITCODE
