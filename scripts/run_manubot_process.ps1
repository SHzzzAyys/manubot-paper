$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$venvScripts = Join-Path $repoRoot ".venv\Scripts"
$manubotExe = Join-Path $venvScripts "manubot.exe"

if (-not (Test-Path $manubotExe)) {
    throw "Local .venv is missing Manubot. Run scripts\setup_local_env.ps1 first."
}

$env:TZ = "Etc/UTC"
$env:LC_ALL = "en_US.UTF-8"
$env:PATH = "$venvScripts;$env:PATH"

Set-Location $repoRoot

& $manubotExe process `
  --content-directory=content `
  --output-directory=output `
  --cache-directory=ci/cache `
  --skip-citations `
  --log-level=INFO
