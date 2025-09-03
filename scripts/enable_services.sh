#!/usr/bin/env bash
set -e
sudo cp services/pixie-boot.service /etc/systemd/system/
sudo cp services/pixie-app.service  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pixie-boot.service
sudo systemctl enable pixie-app.service
echo "Enabled Pixie boot and app services."
