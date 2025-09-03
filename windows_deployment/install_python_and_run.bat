@echo off
REM Pixie Vault - Complete Windows Installation
echo ========================================
echo Pixie Vault - Complete Installation
echo ========================================
echo.

REM Check if Python is already installed
python --version >nul 2>&1
if not errorlevel 1 (
    echo Python is already installed!
    goto :install_deps
)

echo Installing Python 3.11.9...
echo Please follow the installation prompts:
echo - Check "Add Python to PATH"
echo - Choose "Install for all users" (recommended)
echo.
pause

REM Install Python silently with PATH
python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

if errorlevel 1 (
    echo.
    echo Manual installation required. Running installer...
    python-3.11.9-amd64.exe
    echo.
    echo After Python installation completes, run this script again.
    pause
    exit /b 1
)

echo Python installation completed!
echo.

:install_deps
echo Installing Pixie Vault dependencies...
pip install pillow

if errorlevel 1 (
    echo.
    echo Warning: Could not install Pillow automatically
    echo You may need to install it manually: pip install pillow
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run Pixie Vault, use: run_pixie_vault.bat
echo Or manually: python src\app.py
echo.
pause
