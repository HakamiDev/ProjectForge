#!/bin/bash
# تثبيت Project Forge وتشغيله (macOS وLinux). الاستعمال: سطر واحد في Terminal، انظر README.
REPO="${FORGE_REPO:-https://github.com/HakamiDev/ProjectForge}"
URL="${FORGE_URL:-$REPO/raw/refs/heads/main/Project%20Forge%201.py}"
DIR="${FORGE_DIR:-$HOME/Documents/Project Forge}"
FILE="$DIR/Project Forge 1.py"

# رسائل التثبيت بلغة FORGE_LANGUAGE إن وُجدت؛ العربية تبقى بالإنجليزية لأن الطرفيات لا تعرض العربية سليمة
case "$FORGE_LANGUAGE" in
  Español*|*[Ss]panish*) L=es ;;
  Македонски*|*[Mm]acedonian*) L=mk ;;
  Deutsch*|*[Gg]erman*) L=de ;;
  中文*|*[Cc]hinese*) L=zh ;;
  Português*|*[Pp]ortuguese*) L=pt ;;
  Русский*|*[Rr]ussian*) L=ru ;;
  *) L=en ;;
esac
msg() {
  case "$L:$1" in
    es:nopy) echo 'Python no está instalado en su equipo.' ;;
    mk:nopy) echo 'Python не е пронајден на вашиот компјутер.' ;;
    de:nopy) echo 'Python wurde auf Ihrem Computer nicht gefunden.' ;;
    zh:nopy) echo '您的电脑上未找到 Python。' ;;
    pt:nopy) echo 'O Python não foi encontrado no seu computador.' ;;
    ru:nopy) echo 'Python не найден на вашем компьютере.' ;;
    es:apple) echo 'Apple le pedirá instalar las herramientas necesarias. Haga clic en Instalar y, cuando termine la instalación, vuelva a ejecutar el mismo comando.' ;;
    mk:apple) echo 'Apple ќе ве праша да ги инсталирате потребните алатки. Кликнете Install, а кога ќе заврши инсталацијата, извршете ја истата команда повторно.' ;;
    de:apple) echo 'Apple fordert Sie auf, die benötigten Werkzeuge zu installieren. Klicken Sie auf Installieren und führen Sie nach Abschluss denselben Befehl erneut aus.' ;;
    zh:apple) echo 'Apple 会提示您安装所需工具。请点击“安装”，安装完成后再次运行同一命令。' ;;
    pt:apple) echo 'A Apple vai pedir-lhe para instalar as ferramentas necessárias. Clique em Instalar e, quando a instalação terminar, execute o mesmo comando novamente.' ;;
    ru:apple) echo 'Apple предложит установить необходимые инструменты. Нажмите «Установить», а после завершения установки выполните ту же команду ещё раз.' ;;
    es:getpy) echo 'Instale Python 3 desde https://www.python.org/downloads e inténtelo de nuevo.' ;;
    mk:getpy) echo 'Инсталирајте Python 3 од https://www.python.org/downloads, па обидете се повторно.' ;;
    de:getpy) echo 'Installieren Sie Python 3 von https://www.python.org/downloads und versuchen Sie es erneut.' ;;
    zh:getpy) echo '请从 https://www.python.org/downloads 安装 Python 3，然后重试。' ;;
    pt:getpy) echo 'Instale o Python 3 a partir de https://www.python.org/downloads e tente novamente.' ;;
    ru:getpy) echo 'Установите Python 3 с https://www.python.org/downloads и повторите попытку.' ;;
    es:dl) echo 'Descargando Project Forge...' ;;
    mk:dl) echo 'Се презема Project Forge...' ;;
    de:dl) echo 'Project Forge wird heruntergeladen...' ;;
    zh:dl) echo '正在下载 Project Forge...' ;;
    pt:dl) echo 'A descarregar o Project Forge...' ;;
    ru:dl) echo 'Загрузка Project Forge...' ;;
    es:dlfail) echo 'La descarga falló. Compruebe su conexión a internet e inténtelo de nuevo.' ;;
    mk:dlfail) echo 'Преземањето не успеа. Проверете ја интернет-врската и обидете се повторно.' ;;
    de:dlfail) echo 'Der Download ist fehlgeschlagen. Prüfen Sie Ihre Internetverbindung und versuchen Sie es erneut.' ;;
    zh:dlfail) echo '下载失败。请检查网络连接后重试。' ;;
    pt:dlfail) echo 'A transferência falhou. Verifique a ligação à internet e tente novamente.' ;;
    ru:dlfail) echo 'Загрузка не удалась. Проверьте подключение к интернету и повторите попытку.' ;;
    es:later) echo 'Para ejecutarlo más tarde:' ;;
    mk:later) echo 'За да го стартувате подоцна:' ;;
    de:later) echo 'Später erneut starten mit:' ;;
    zh:later) echo '以后运行：' ;;
    pt:later) echo 'Para executar mais tarde:' ;;
    ru:later) echo 'Чтобы запустить позже:' ;;
    *:nopy) echo 'Python was not found on your computer.' ;;
    *:apple) echo 'Apple will prompt you to install the required tools. Click Install, then run the same command again when installation finishes.' ;;
    *:getpy) echo 'Install Python 3 from https://www.python.org/downloads, then try again.' ;;
    *:dl) echo 'Downloading Project Forge...' ;;
    *:dlfail) echo 'Download failed. Check your internet connection and try again.' ;;
    *:later) echo 'To run later:' ;;
  esac
}

if ! command -v python3 >/dev/null 2>&1; then
  msg nopy
  msg apple
  xcode-select --install 2>/dev/null || msg getpy
  exit 1
fi

mkdir -p "$DIR" || exit 1
msg dl
if ! curl -fsSL -o "$FILE" "$URL"; then
  msg dlfail
  exit 1
fi
cd "$DIR" || exit 1
export PYTHONUTF8=1
echo "$(msg later) python3 -I \"$FILE\""
python3 -I "$FILE" "$@"
