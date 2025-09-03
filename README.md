# Pixie Vault – Pi Password Manager

A touch-friendly password manager designed for Raspberry Pi with a beautiful boot animation and air-gap security.

## Features

- **Touch-Friendly UI**: Large buttons and inputs optimized for touchscreen interaction
- **Dynamic Custom Fields**: Add any custom fields with individual remove buttons (× to delete)
- **Smart Search**: Search across all fields with dynamic field filtering
- **Multiple Sort Modes**: A→Z, Recently Added, Recently Updated, Most Used
- **Intuitive Field Order**: User data first (Name, Protocol, Website, Username, Password, Notes), metadata last (ID, Created, Last Accessed)
- **Boot Animation**: Plays your Sora Pixie MP4 full-screen at startup
- **Air-Gap Friendly**: No network dependencies, local JSON storage
- **Optional Encryption**: Toggle-able AES/Fernet encryption for data at rest

## Directory Structure

```
pixie-vault/
├── README.md
├── assets/
│   ├── pixie_boot.mp4        # Your Sora animation (rename to this)
│   └── pixie_icon.png
├── data/
│   ├── vault.json            # Entries (encrypted if enabled)
│   └── config.json           # App config + UI preferences
├── src/
│   ├── app.py                # Main Tkinter application
│   ├── storage.py            # JSON storage with optional encryption
│   ├── search.py             # Search/filter/sort helpers
│   └── model.py              # Data models & validation
├── services/
│   ├── pixie-boot.service    # Boot video service
│   └── pixie-app.service     # Main app service
└── scripts/
    ├── install_deps.sh       # Install dependencies
    └── enable_services.sh    # Enable systemd services
```

## Data Model

Each password entry contains:

```json
{
  "id": "uuid4-string",
  "name": "GitHub – Work",
  "protocol": "https",
  "website": "github.com",
  "username": "johnny",
  "password": "•••",
  "notes": "2FA in Authy",
  "custom": {
    "Environment": "Prod",
    "Category": "Dev",
    "Owner": "John"
  },
  "created_at": 1735822800,
  "updated_at": 1735822800,
  "access_count": 0,
  "last_access_at": null
}
```

## Setup Instructions

### 1. Copy to Raspberry Pi

```bash
# Copy the entire folder to your Pi
scp -r pixie-vault/ pi@your-pi-ip:/home/pi/
```

### 2. Install Dependencies

```bash
cd /home/pi/pixie-vault/scripts
chmod +x install_deps.sh
bash install_deps.sh
```

### 3. Add Your Boot Animation

Place your Sora animation MP4 file at:
```bash
/home/pi/pixie-vault/assets/pixie_boot.mp4
```

### 4. Enable Services

```bash
cd /home/pi/pixie-vault/scripts
chmod +x enable_services.sh
bash enable_services.sh
```

### 5. Reboot

```bash
sudo reboot
```

## Usage

### Adding Entries
1. Click **Add Entry**
2. Fill in the base fields (Name, Protocol, Website, Username, Password, Notes)
3. Click **Add field** to create custom fields like Category, Environment, etc.
4. Use the **×** button to remove unwanted custom field rows
5. Click **Save**

### Field Display Order
**Detail Panel**: Name → Protocol → Website → Username → Password → Notes → Custom Fields → ID → Created → Last Accessed

**TreeView Columns**: Name, Protocol, Website, Username, ID, Created, Last Access

### Searching
- Use the search bar to find entries across all fields
- Select a specific field from the dropdown to narrow your search
- Choose sort mode: A→Z, Recently Added, Recently Updated, or Most Used

### Managing Entries
- Click an entry to view full details in the right panel
- Use **Edit Entry** to modify selected entries (with × buttons for custom fields)
- **Delete** removes the selected entry (with confirmation)
- **Refresh** reloads the entry list

## Configuration

Edit `data/config.json` to customize:

```json
{
  "encryption_enabled": false,
  "kdf": "sha256",
  "ui": {
    "theme": "dark",
    "font_scale": 1.2
  },
  "boot": {
    "play_pixie_video": true,
    "video_path": "assets/pixie_boot.mp4",
    "skip_if_debug": false
  }
}
```

## Future Enhancements

- RFID/Fingerprint/Face unlock authentication
- Data-only USB support with isolated power
- Enhanced encryption options
- Backup and sync capabilities

## Dependencies

- Python 3 (with tkinter)
- mpv (for boot animation)
- Optional: cryptography (for encryption)

## Security Notes

- Designed for air-gap operation (no network required)
- Passwords stored in plain text by default (enable encryption in config)
- All data stored locally in JSON format
- No external dependencies for core functionality

---

**Pixie Vault** - Your little guardian for password security ✨
