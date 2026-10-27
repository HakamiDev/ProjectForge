@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -I "Project Forge 1.py"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    python -I "Project Forge 1.py"
  ) else (
    echo Python is not installed. Install it from https://www.python.org/downloads
    echo and tick "Add Python to PATH", then double-click this file again.
  )
)
echo.
pause
