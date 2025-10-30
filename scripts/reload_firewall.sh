#!/usr/bin/env bash
set -e
HERE="$(cd "$(dirname "$0")" && pwd)/.."
sudo nft -f "$HERE/myfirewall/my_firewall.nft"
sudo systemctl restart rsyslog || true
echo "Reloaded firewall rules and rsyslog."
