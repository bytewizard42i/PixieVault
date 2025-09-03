# Pixie Vault - Windows Quick Start

## Easy Installation (Python Included!)

1. **Extract** this zip file to `C:\PixieVault\`
2. **Run** `install_python_and_run.bat` (double-click) - Installs Python + dependencies
3. **Launch** `run_pixie_vault.bat` (double-click)

## Alternative Installation

1. **Extract** this zip file to `C:\PixieVault\`
2. **Install Python manually** - Run `python-3.11.9-amd64.exe`
   - ✅ Check "Add Python to PATH" during installation
3. **Run** `install_dependencies.bat` (double-click)
4. **Launch** `run_pixie_vault.bat` (double-click)

## Files Included

- `python-3.11.9-amd64.exe` - Python 3.11.9 installer (25MB)
- `install_python_and_run.bat` - One-click Python + dependencies installer
- `run_pixie_vault.bat` - Launch Pixie Vault
- `install_dependencies.bat` - Install required packages only
- `WINDOWS_DEPLOYMENT.md` - Full deployment guide
- `src/` - Application source code
- `data/` - Data storage (vault.json, config.json)
- `media/` - Pixie images and assets

## For Airgapped Systems

See `WINDOWS_DEPLOYMENT.md` for complete offline installation instructions.

## Troubleshooting

**"Python not found":**
- Install Python from python.org
- Restart Command Prompt after installation

**"Pillow not found":**
- Run `install_dependencies.bat`
- Or manually: `pip install pillow`

**Permission errors:**
- Run batch files as Administrator
- Check antivirus exclusions

## Quick Commands

```cmd
# Manual launch
cd C:\PixieVault\src
python app.py

# Install dependencies manually
pip install pillow
```

🧚‍♀️ **Enjoy your secure password vault!**
