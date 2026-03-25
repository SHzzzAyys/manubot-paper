$ErrorActionPreference = "Stop"

$repoRoot = "C:\Users\zheng shang\manubot-paper"
$ghExe = "C:\Program Files\GitHub CLI\gh.exe"
$repoSlug = "shangzheng666/manubot-paper"

Write-Host "Checking GitHub CLI authentication..."
& $ghExe auth status

Write-Host ""
Write-Host "Creating GitHub repository and pushing main..."
& $ghExe repo create $repoSlug --private --source $repoRoot --remote origin --push
