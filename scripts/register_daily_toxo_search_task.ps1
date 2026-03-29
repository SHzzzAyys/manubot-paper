param(
    [string]$TaskName = "DailyToxoVaccineSearch",
    [string]$Time = "08:30",
    [int]$Days = 7
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $PSScriptRoot "run_daily_toxo_search.ps1"
$action = "powershell -ExecutionPolicy Bypass -File `"$runner`" -Days $Days"

schtasks /Create /F /SC DAILY /TN $TaskName /TR $action /ST $Time
