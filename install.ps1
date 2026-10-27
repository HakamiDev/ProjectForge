# تثبيت Project Forge وتشغيله (Windows PowerShell). الاستعمال: سطر واحد، انظر README.
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
$Repo = if ($env:FORGE_REPO) { $env:FORGE_REPO } else { "https://github.com/hakami-bros/project-forge" }
$Url  = if ($env:FORGE_URL)  { $env:FORGE_URL }  else { "$Repo/releases/latest/download/Project.Forge.1.py" }
$Dir  = if ($env:FORGE_DIR)  { $env:FORGE_DIR }  else { Join-Path $HOME "Documents\Project Forge" }
$File = Join-Path $Dir "Project Forge 1.py"

$py = $null
foreach ($c in @("py", "python", "python3")) {
  if (Get-Command $c -ErrorAction SilentlyContinue) { $py = $c; break }
}
if (-not $py) {
  Write-Host "لم أجد Python. جارٍ تثبيته..."
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    Write-Host "تم التثبيت. أغلق هذه النافذة وافتح PowerShell جديدة ثم أعد لصق السطر نفسه."
  } else {
    Write-Host "ثبّت Python من https://www.python.org/downloads (فعّل خيار Add Python to PATH) ثم أعد المحاولة."
  }
  return
}

New-Item -ItemType Directory -Force -Path $Dir | Out-Null
Write-Host "جارٍ تنزيل الأداة..."
Invoke-WebRequest -Uri $Url -OutFile $File -UseBasicParsing
Set-Location $Dir
if ($py -eq "py") { & py -3 -I $File @args } else { & $py -I $File @args }
