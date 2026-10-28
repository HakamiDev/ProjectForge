#!/bin/bash
# تثبيت Project Forge وتشغيله (macOS وLinux). الاستعمال: سطر واحد في Terminal، انظر README.
REPO="${FORGE_REPO:-https://github.com/HakamiDev/ProjectForge}"
URL="${FORGE_URL:-$REPO/raw/refs/heads/main/Project%20Forge%201.py}"
DIR="${FORGE_DIR:-$HOME/Documents/Project Forge}"
FILE="$DIR/Project Forge 1.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python was not found on your computer."
  echo "Apple will prompt you to install the required tools. Click Install, then run the same command again when installation finishes."
  xcode-select --install 2>/dev/null || echo "Install Python 3 from https://www.python.org/downloads, then try again."
  exit 1
fi

mkdir -p "$DIR" || exit 1
echo "Downloading Project Forge..."
if ! curl -fsSL -o "$FILE" "$URL"; then
  echo "Download failed. Check your internet connection and try again."
  exit 1
fi
cd "$DIR" || exit 1
export PYTHONUTF8=1
echo "To run later: python3 -I \"$FILE\""
python3 -I "$FILE" "$@"
