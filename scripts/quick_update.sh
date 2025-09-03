#!/bin/bash
# Quick update script - downloads only source files
echo "🧚‍♀️ Quick Pixie Update"
echo "======================"

# Create temp directory
mkdir -p /tmp/pixie_update
cd /tmp/pixie_update

# Download latest source files only
echo "📥 Downloading latest source..."
curl -L https://raw.githubusercontent.com/bytewizard42i/PixieVault/main/src/app.py -o app.py
curl -L https://raw.githubusercontent.com/bytewizard42i/PixieVault/main/src/storage.py -o storage.py  
curl -L https://raw.githubusercontent.com/bytewizard42i/PixieVault/main/src/search.py -o search.py

# Check if downloads succeeded
if [ -f "app.py" ] && [ -f "storage.py" ] && [ -f "search.py" ]; then
    echo "✅ Downloaded successfully"
    
    # Go back to pixie directory
    cd - > /dev/null
    
    # Backup current files
    echo "💾 Backing up current files..."
    cp src/app.py src/app.py.backup.$(date +%Y%m%d_%H%M%S)
    cp src/storage.py src/storage.py.backup.$(date +%Y%m%d_%H%M%S)
    cp src/search.py src/search.py.backup.$(date +%Y%m%d_%H%M%S)
    
    # Copy new files
    echo "📝 Installing updates..."
    cp /tmp/pixie_update/*.py src/
    
    # Cleanup
    rm -rf /tmp/pixie_update
    
    echo "✅ Update complete!"
    echo "🔄 Restart Pixie Vault to see changes"
else
    echo "❌ Download failed - check internet connection"
    rm -rf /tmp/pixie_update
    exit 1
fi
