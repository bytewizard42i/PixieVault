# Pixie Vault - Windows 10 Airgapped Deployment Guide

## Prerequisites for Airgapped Windows 10

### 1. Python Installation (Offline)
Download these files on a connected machine, then transfer via USB:

**Python 3.11+ Installer:**
- Download: `python-3.11.x-amd64.exe` from https://www.python.org/downloads/windows/
- Choose "Add Python to PATH" during installation
- Install for all users (recommended)

### 2. Required Python Packages (Offline)
Download these wheel files on a connected machine:

```bash
# On connected machine, download packages:
pip download pillow tkinter-page
# This creates .whl files you can transfer
```

**Required packages:**
- `Pillow` (for image handling)
- `tkinter` (usually included with Python)

### 3. Transfer Files to Airgapped Machine
Copy these to USB drive:
- `PixieVault-Pi-Deploy.zip` (from this repository)
- `python-3.11.x-amd64.exe`
- Downloaded `.whl` files for dependencies

## Installation Steps

### Step 1: Install Python
1. Copy Python installer to airgapped machine
2. Run `python-3.11.x-amd64.exe` as Administrator
3. Check "Add Python to PATH"
4. Complete installation

### Step 2: Extract Pixie Vault
1. Extract `PixieVault-Pi-Deploy.zip` to `C:\PixieVault\`
2. Open Command Prompt as Administrator
3. Navigate to: `cd C:\PixieVault`

### Step 3: Install Dependencies (Offline)
```cmd
# Install from wheel files (if needed)
pip install pillow-x.x.x-py3-none-any.whl --no-index --find-links .

# Verify tkinter is available
python -c "import tkinter; print('tkinter OK')"
```

### Step 4: Run Pixie Vault
```cmd
cd C:\PixieVault\src
python app.py
```

## Alternative: Portable Python Setup

### Option 1: WinPython (Recommended for Airgapped)
1. Download WinPython from https://winpython.github.io/ (on connected machine)
2. Transfer portable Python to airgapped machine
3. Extract and run from any folder
4. No installation required

### Option 2: Python Embedded Distribution
1. Download Python embedded zip from python.org
2. Extract to `C:\PixieVault\python\`
3. Run: `C:\PixieVault\python\python.exe src\app.py`

## Troubleshooting

### Common Issues:

**"tkinter not found":**
- Reinstall Python with "tcl/tk and IDLE" option checked

**"PIL/Pillow not found":**
- Install Pillow: `pip install pillow` (if internet available)
- Or use offline wheel file method above

**"Permission denied":**
- Run Command Prompt as Administrator
- Check Windows Defender/antivirus exclusions

### File Locations:
- **Data storage:** `C:\PixieVault\data\vault.json`
- **Configuration:** `C:\PixieVault\data\config.json`
- **Logs:** Check Command Prompt output

## Security Notes for Airgapped Environment

1. **Data Encryption:** Vault data is stored in JSON format (consider additional encryption)
2. **Backup:** Regularly backup `data\vault.json` to external media
3. **Updates:** Manual transfer required for any updates
4. **Dependencies:** All required packages must be pre-installed offline

## Quick Start Commands

```cmd
# Navigate to Pixie Vault
cd C:\PixieVault

# Run the application
python src\app.py

# Or if using portable Python:
python-portable\python.exe src\app.py
```

## Features Available Offline

✅ **Full functionality:**
- Password storage and retrieval
- Search and filtering
- Entry management
- Data export/import
- Pixie UI elements

❌ **Not available:**
- Automatic updates
- Online synchronization
- Cloud backup

---

**Note:** This guide assumes Windows 10 with standard user permissions. Adjust paths and commands based on your specific Windows configuration.
