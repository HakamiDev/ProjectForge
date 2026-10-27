#!/bin/bash
# انقر مرتين لتشغيل الأداة (macOS). في المرة الأولى: انقر بزر الفأرة الأيمن ثم «فتح».
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "لم أجد Python. سيظهر طلب من Apple لتثبيت الأدوات: اضغط «تثبيت» ثم أعد النقر على هذا الملف."
  xcode-select --install 2>/dev/null
  read -n 1 -s -r -p "اضغط أي مفتاح للإغلاق"
  exit 1
fi
export PYTHONUTF8=1
python3 -I "Project Forge 1.py"
echo
read -n 1 -s -r -p "اضغط أي مفتاح للإغلاق"
