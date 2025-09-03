@echo off
REM Install Pixie Vault Dependencies for Windows
echo Installing Pixie Vault dependencies...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    echo Please install Python 3.11+ first
    echo Download from: https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

echo Python found, installing dependencies...
pip install pillow

if errorlevel 1 (
    echo.
    echo Warning: Failed to install Pillow online
    echo For airgapped systems, use offline wheel files
    echo See WINDOWS_DEPLOYMENT.md for instructions
) else (
    echo.
    echo Dependencies installed successfully!
)

echo.
echo You can now run Pixie Vault with: run_pixie_vault.bat
pause
