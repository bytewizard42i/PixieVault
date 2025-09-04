#!/bin/bash
# Python3 Update Script for Raspberry Pi
# Updates Python3 to latest available version

echo "🐍 PixieVault - Python3 Update Script for Raspberry Pi"
echo "=================================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Please run this script as a regular user (not root)"
    exit 1
fi

echo "📦 Updating package lists..."
sudo apt update

echo "🔍 Checking current Python3 version..."
python3 --version

echo "⬆️  Upgrading Python3 and related packages..."
sudo apt upgrade -y python3 python3-pip python3-dev python3-venv

echo "🔧 Installing additional Python3 tools..."
sudo apt install -y python3-setuptools python3-wheel

echo "📋 Installing/updating pip..."
python3 -m pip install --upgrade pip

echo "🧪 Installing PixieVault dependencies..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt
else
    echo "Installing common dependencies..."
    python3 -m pip install pillow cryptography
fi

echo "✅ Python3 update completed!"
echo "📊 Current Python3 version:"
python3 --version
echo "📊 Current pip version:"
python3 -m pip --version

echo ""
echo "🚀 Python3 is now updated and ready for PixieVault!"
