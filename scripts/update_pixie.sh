#!/bin/bash
# Pixie Vault Update Script for Raspberry Pi
# Updates the application from git repository

echo "🧚‍♀️ Pixie Vault Update Script"
echo "================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "Please run this script from the PixieVault directory"
    exit 1
fi

# Check for internet connection
if ! ping -c 1 github.com &> /dev/null; then
    echo "❌ Error: No internet connection"
    echo "Cannot update from repository"
    exit 1
fi

echo "📡 Checking for updates..."

# Fetch latest changes
git fetch origin

# Check if updates are available
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "✅ Already up to date!"
    exit 0
fi

echo "📥 Updates available. Downloading..."

# Backup current data
echo "💾 Backing up data..."
cp -r data/ data_backup_$(date +%Y%m%d_%H%M%S)/

# Pull updates
git pull origin main

if [ $? -eq 0 ]; then
    echo "✅ Update successful!"
    echo ""
    echo "🔄 Restart Pixie Vault to see changes"
    echo "   - Close the application"
    echo "   - Run: python3 src/app.py"
    echo ""
    echo "📁 Data backup created in case of issues"
else
    echo "❌ Update failed!"
    echo "Your data is safe in the backup folder"
    exit 1
fi
