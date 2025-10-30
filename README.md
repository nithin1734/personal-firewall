# 🔥 Personal Firewall — Linux Security Project  

A **lightweight, on-demand personal firewall** built using **nftables** and **Python**.  
This project allows you to block unwanted ports (like SSH), monitor live logs, view activity in a **Terminal GUI (TUI)**, and receive alerts — all without modifying your system’s default firewall.

---

## 📘 About the Project  

The **Personal Firewall** is designed for developers, ethical hackers, and cybersecurity learners who want to understand how Linux packet filtering and real-time alerting work.

Unlike system firewalls (like `ufw`), this one runs **on-demand** — meaning you can activate and deactivate it anytime.  
It includes:
- nftables ruleset for IPv4 & IPv6
- Logging & alerting via rsyslog
- A Python-based TUI dashboard
- Optional webhook alert sender

---

## 🧰 Development Environment & Tools  

| Category | Tools/Technologies |
|-----------|--------------------|
| 💻 **OS** | Linux (Kali, Ubuntu, Debian) |
| 🧱 **Firewall Engine** | nftables |
| 🐍 **Programming Language** | Python 3 |
| 📡 **Logging System** | rsyslog |
| 🎨 **Interface** | Terminal GUI (Python curses) |
| 🪣 **Version Control** | Git & GitHub |
| 🧾 **Automation Scripts** | Bash shell scripts |
| ⚙️ **Optional Monitoring** | logrotate, systemd services |

---
## ✨ Features  

✅ **On-demand firewall loading** — no permanent system changes  
✅ **Blocks SSH (port 22) and customizable open ports**  
✅ **Supports both IPv4 & IPv6**  
✅ **Logs dropped packets with clear prefixes**  
✅ **Interactive Terminal GUI (TUI)** showing live access attempts  
✅ **Alert system** for SSH or suspicious traffic  
✅ **Simple start/stop/reload scripts**  
✅ **Safe for testing** — does not conflict with UFW or iptables  

---

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


## ✨ Authors
- nithin1734 — repository owner

