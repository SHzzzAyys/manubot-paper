param(
    [string]$Python = "py -3.11"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $repoRoot ".venv"
$requirementsPath = Join-Path $repoRoot "requirements-local.txt"

Write-Host "Repository root: $repoRoot"
Write-Host "Virtual environment: $venvPath"

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating local virtual environment..."
    Invoke-Expression "$Python -m venv `"$venvPath`""
}

$pythonExe = Join-Path $venvPath "Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    throw "Python executable was not created at $pythonExe"
}

Write-Host "Upgrading pip, setuptools, and wheel..."
& $pythonExe -m pip install --upgrade pip setuptools wheel

Write-Host "Installing local requirements..."
& $pythonExe -m pip install -r $requirementsPath

Write-Host "Checking Pandoc..."
try {
    $pandocVersion = & pandoc --version | Select-Object -First 1
    Write-Host "Pandoc detected: $pandocVersion"
}
catch {
    Write-Warning "Pandoc is not on PATH. Local HTML/PDF export will fail until Pandoc is installed."
}

Write-Host ""
Write-Host "Local environment is ready."
Write-Host "Use it with:"
Write-Host "  & `"$pythonExe`" scripts\validate_manuscript.py"
Write-Host "  & `"$pythonExe`" scripts\export_evidence_tables.py"
