#!/usr/bin/env bash
set -e
# Delete only the personal table we created (safer)
sudo nft delete table inet personal_fw || true
echo "Personal firewall removed."
