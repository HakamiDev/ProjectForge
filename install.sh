#!/bin/bash
# تثبيت Project Forge وتشغيله (macOS وLinux). الاستعمال: سطر واحد في Terminal، انظر README.
REPO="${FORGE_REPO:-https://github.com/hakami-bros/project-forge}"
URL="${FORGE_URL:-$REPO/releases/latest/download/Project.Forge.1.py}"
DIR="${FORGE_DIR:-$HOME/Documents/Project Forge}"
FILE="$DIR/Project Forge 1.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "لم أجد Python على جهازك."
  echo "سيظهر الآن طلب من Apple لتثبيت الأدوات اللازمة: اضغط «تثبيت»، وبعد انتهائه أعد لصق السطر نفسه."
  xcode-select --install 2>/dev/null || echo "ثبّت Python 3 من https://www.python.org/downloads ثم أعد المحاولة."
  exit 1
fi

mkdir -p "$DIR" || exit 1
echo "جارٍ تنزيل الأداة..."
if ! curl -fsSL -o "$FILE" "$URL"; then
  echo "تعذّر التنزيل. تحقق من الاتصال بالإنترنت وأعد المحاولة."
  exit 1
fi
cd "$DIR" || exit 1
export PYTHONUTF8=1
python3 -I "$FILE" "$@"
