#!/usr/bin/env bash
set -e
HERE="$(cd "$(dirname "$0")" && pwd)/.."
# copy rsyslog conf if not present
if [ ! -f /etc/rsyslog.d/30-firewall.conf ]; then
  echo "Installing rsyslog conf..."
  sudo cp "$HERE/rsyslog/30-firewall.conf" /etc/rsyslog.d/30-firewall.conf
  sudo systemctl restart rsyslog
fi
# Load the nftables ruleset (from repo root)
sudo nft -f "$HERE/myfirewall/my_firewall.nft"
echo "Personal firewall loaded. Use 'sudo nft list ruleset' to inspect."
