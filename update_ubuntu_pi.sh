#!/bin/bash
# Ubuntu System Update Script for Raspberry Pi
# Performs full system update and maintenance

echo "🍓 PixieVault - Ubuntu System Update Script for Raspberry Pi"
echo "=========================================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Please run this script as a regular user (not root)"
    exit 1
fi

echo "📦 Updating package lists..."
sudo apt update

echo "⬆️  Upgrading all installed packages..."
sudo apt upgrade -y

echo "🔧 Installing essential development tools..."
sudo apt install -y build-essential git curl wget

echo "🧹 Cleaning up unnecessary packages..."
sudo apt autoremove -y
sudo apt autoclean

echo "🔄 Updating snap packages (if available)..."
if command -v snap &> /dev/null; then
    sudo snap refresh
else
    echo "Snap not installed, skipping snap updates"
fi

echo "🔒 Checking for security updates..."
sudo apt list --upgradable | grep -i security

echo "💾 Checking disk space..."
df -h /

echo "🌡️  Checking system temperature (if available)..."
if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
    temp=$(cat /sys/class/thermal/thermal_zone0/temp)
    temp_c=$((temp/1000))
    echo "CPU Temperature: ${temp_c}°C"
else
    echo "Temperature monitoring not available"
fi

echo "📊 System information:"
echo "Kernel: $(uname -r)"
echo "Ubuntu: $(lsb_release -d | cut -f2)"
echo "Architecture: $(uname -m)"

echo ""
echo "✅ Ubuntu system update completed!"
echo "🔄 Consider rebooting if kernel was updated"
echo "🚀 System is ready for PixieVault!"
