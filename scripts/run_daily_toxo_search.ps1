param(
    [int]$Days = 7
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$searchScript = Join-Path $PSScriptRoot "daily_toxo_vaccine_search.py"
$intelScript = Join-Path $PSScriptRoot "build_literature_intelligence.py"
$hubScript = Join-Path $PSScriptRoot "build_research_hub.py"
$sanitizeScript = Join-Path $PSScriptRoot "sanitize_wording.py"

function Invoke-PythonScript {
    param(
        [string]$PythonExe,
        [string]$ScriptPath,
        [string[]]$Arguments = @()
    )

    & $PythonExe $ScriptPath @Arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

if (Test-Path $venvPython) {
    Invoke-PythonScript -PythonExe $venvPython -ScriptPath $searchScript -Arguments @("--days", $Days)
    Invoke-PythonScript -PythonExe $venvPython -ScriptPath $intelScript
    Invoke-PythonScript -PythonExe $venvPython -ScriptPath $hubScript
    Invoke-PythonScript -PythonExe $venvPython -ScriptPath $sanitizeScript -Arguments @("--profile", "academic")
    exit 0
}

Invoke-PythonScript -PythonExe "py" -ScriptPath $searchScript -Arguments @("--days", $Days)
Invoke-PythonScript -PythonExe "py" -ScriptPath $intelScript
Invoke-PythonScript -PythonExe "py" -ScriptPath $hubScript
Invoke-PythonScript -PythonExe "py" -ScriptPath $sanitizeScript -Arguments @("--profile", "academic")
exit 0
