#!/usr/bin/env bash
set -e
if [ -x "$(command -v apt)" ]; then
  sudo apt update
  sudo apt install -y nftables rsyslog python3 python3-pip
else
  echo "This script currently supports apt-based systems. Install nftables, rsyslog, python3 manually for your distro."
fi
sudo pip3 install requests || true
echo "Installed nftables, rsyslog, python3 (if available)."
