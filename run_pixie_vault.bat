@echo off
REM Pixie Vault Windows Launcher
echo Starting Pixie Vault...
cd /d "%~dp0src"
python app.py
if errorlevel 1 (
    echo.
    echo Error: Python not found or Pixie Vault failed to start
    echo Please ensure Python 3.11+ is installed and in your PATH
    echo.
    pause
)
