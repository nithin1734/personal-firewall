# Personal Firewall (nftables) — GitHub-ready project

Self-contained, on-demand personal firewall using **nftables** with IPv4/IPv6 support, logging, and a terminal UI (TUI).
You can load it when needed and remove it without altering system defaults.

## Quickstart (Ubuntu/Debian)

1. Unzip the project and `cd` into the folder.
2. Inspect `myfirewall/my_firewall.nft` and adjust blocked ports if needed.
3. Install deps:
```bash
sudo bash scripts/install_deps.sh
```
4. Install the rsyslog conf (required for `/var/log/firewall.log`):
```bash
sudo cp rsyslog/30-firewall.conf /etc/rsyslog.d/30-firewall.conf
sudo systemctl restart rsyslog
```
5. Start the personal firewall (on-demand):
```bash
sudo nft -f myfirewall/my_firewall.nft
```
6. Run the TUI to monitor logs:
```bash
sudo python3 tui/firewall_tui.py
```
7. Stop the firewall when finished:
```bash
sudo bash scripts/stop_firewall.sh
```

**WARNING:** Test locally (VM) before using on remote systems to avoid locking yourself out.
