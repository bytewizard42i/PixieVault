#!/usr/bin/env bash
set -e
sudo apt-get update
sudo apt-get install -y python3-pip python3-tk mpv
pip3 install --user --upgrade pip
# No heavy deps by default. If you want optional encryption later:
# pip3 install --user cryptography
echo "Done."
