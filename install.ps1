# تثبيت Project Forge وتشغيله (Windows PowerShell). الاستعمال: سطر واحد، انظر README.
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
$Repo = if ($env:FORGE_REPO) { $env:FORGE_REPO } else { "https://github.com/HakamiDev/ProjectForge" }
$Url  = if ($env:FORGE_URL)  { $env:FORGE_URL }  else { "$Repo/raw/refs/heads/main/Project%20Forge%201.py" }
$Dir  = if ($env:FORGE_DIR)  { $env:FORGE_DIR }  else { Join-Path $HOME "Documents\Project Forge" }
$File = Join-Path $Dir "Project Forge 1.py"

# رسائل التثبيت بلغة FORGE_LANGUAGE إن وُجدت؛ العربية تبقى بالإنجليزية لأن الطرفيات لا تعرض العربية سليمة
$L = "en"
$lv = "$env:FORGE_LANGUAGE"
if ($lv -match "^Español|Spanish") { $L = "es" } elseif ($lv -match "^Македонски|Macedonian") { $L = "mk" } elseif ($lv -match "^Deutsch|German") { $L = "de" } elseif ($lv -match "^中文|Chinese") { $L = "zh" } elseif ($lv -match "^Português|Portuguese") { $L = "pt" } elseif ($lv -match "^Русский|Russian") { $L = "ru" }
$Msg = @{
  "nopyw" = @{ "en" = "Python was not found. Installing Python..."; "es" = "Python no está instalado. Instalando Python..."; "mk" = "Python не е пронајден. Се инсталира Python..."; "de" = "Python wurde nicht gefunden. Python wird installiert..."; "zh" = "未找到 Python，正在安装 Python..."; "pt" = "O Python não foi encontrado. A instalar o Python..."; "ru" = "Python не найден. Устанавливается Python..." }
  "wdone" = @{ "en" = "Installation finished. Close this window, open a new PowerShell window, and run the same command again."; "es" = "Instalación terminada. Cierre esta ventana, abra una nueva ventana de PowerShell y vuelva a ejecutar el mismo comando."; "mk" = "Инсталацијата заврши. Затворете го овој прозорец, отворете нов прозорец на PowerShell и извршете ја истата команда повторно."; "de" = "Installation abgeschlossen. Schließen Sie dieses Fenster, öffnen Sie ein neues PowerShell-Fenster und führen Sie denselben Befehl erneut aus."; "zh" = "安装完成。请关闭此窗口，打开新的 PowerShell 窗口，再次运行同一命令。"; "pt" = "Instalação concluída. Feche esta janela, abra uma nova janela do PowerShell e execute o mesmo comando novamente."; "ru" = "Установка завершена. Закройте это окно, откройте новое окно PowerShell и выполните ту же команду ещё раз." }
  "wgetpy" = @{ "en" = "Install Python from https://www.python.org/downloads (enable Add Python to PATH), then try again."; "es" = "Instale Python desde https://www.python.org/downloads (active Add Python to PATH) e inténtelo de nuevo."; "mk" = "Инсталирајте Python од https://www.python.org/downloads (вклучете Add Python to PATH), па обидете се повторно."; "de" = "Installieren Sie Python von https://www.python.org/downloads (aktivieren Sie Add Python to PATH) und versuchen Sie es erneut."; "zh" = "请从 https://www.python.org/downloads 安装 Python（勾选 Add Python to PATH），然后重试。"; "pt" = "Instale o Python a partir de https://www.python.org/downloads (ative Add Python to PATH) e tente novamente."; "ru" = "Установите Python с https://www.python.org/downloads (включите Add Python to PATH) и повторите попытку." }
  "dl" = @{ "en" = "Downloading Project Forge..."; "es" = "Descargando Project Forge..."; "mk" = "Се презема Project Forge..."; "de" = "Project Forge wird heruntergeladen..."; "zh" = "正在下载 Project Forge..."; "pt" = "A descarregar o Project Forge..."; "ru" = "Загрузка Project Forge..." }
}
function Say($k) { Write-Host $Msg[$k][$L] }

$py = $null
foreach ($c in @("py", "python", "python3")) {
  if (Get-Command $c -ErrorAction SilentlyContinue) { $py = $c; break }
}
if (-not $py) {
  Say "nopyw"
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    Say "wdone"
  } else {
    Say "wgetpy"
  }
  return
}

New-Item -ItemType Directory -Force -Path $Dir | Out-Null
Say "dl"
Invoke-WebRequest -Uri $Url -OutFile $File -UseBasicParsing
Set-Location $Dir
if ($py -eq "py") { & py -3 -I $File @args } else { & $py -I $File @args }
