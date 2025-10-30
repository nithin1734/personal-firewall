#!/usr/bin/env python3
"""
firewall_tui.py
A simple curses TUI that tails /var/log/firewall.log and shows alerts + stats.
Requires Python 3.8+.
"""

import curses
import time
import re
import threading
from collections import Counter, deque, defaultdict
import os
import sys

LOGFILE = "/var/log/firewall.log"
MAX_EVENTS = 200

# Regex to extract basic nft log info
LOG_RE = re.compile(r'(?P<prefix>FW-[A-Z0-9-]+):.*?\bSRC=(?P<src>[0-9a-fA-F:\\.]+)\b.*?\bDST=(?P<dst>[0-9a-fA-F:\\.]+)\b.*?(?:SPT=(?P<spt>\d+))?.*?(?:DPT=(?P<dpt>\d+))?.*?\bPROTO=(?P<proto>\d+|\w+)?', re.IGNORECASE)
PROTO_MAP = {"6": "TCP", "17": "UDP", "1": "ICMP"}

class Tailer(threading.Thread):
    def __init__(self, filepath, callback):
        super().__init__(daemon=True)
        self.filepath = filepath
        self.callback = callback
        self._stop = threading.Event()

    def run(self):
        # Wait for file to exist
        while not os.path.exists(self.filepath):
            time.sleep(0.5)
            if self._stop.is_set():
                return
        with open(self.filepath, 'r', errors='replace') as f:
            f.seek(0, os.SEEK_END)
            while not self._stop.is_set():
                line = f.readline()
                if not line:
                    time.sleep(0.2)
                    continue
                self.callback(line.strip())

    def stop(self):
        self._stop.set()

class FirewallTUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.events = deque(maxlen=MAX_EVENTS)
        self.counters = Counter()
        self.src_counter = Counter()
        self.lock = threading.Lock()
        self.tailer = Tailer(LOGFILE, self.on_line)
        self.tailer.start()

    def on_line(self, line):
        m = LOG_RE.search(line)
        prefix = None
        src = None
        dst = None
        dpt = None
        proto = None
        if m:
            prefix = m.group('prefix') or "FW-LOG"
            src = m.group('src') or "-"
            dst = m.group('dst') or "-"
            dpt = m.group('dpt') or m.group('spt') or "-"
            proto_raw = m.group('proto') or ""
            proto = PROTO_MAP.get(proto_raw, proto_raw or "-")
        else:
            if "FW-DROP" in line or "FW-ALLOW" in line:
                parts = line.split()
                prefix = parts[0].strip(':') if parts else "FW-LOG"
                src = dst = dpt = proto = "-"
            else:
                return
        event = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "prefix": prefix,
            "src": src,
            "dst": dst,
            "dpt": dpt,
            "proto": proto,
            "raw": line
        }
        with self.lock:
            self.events.appendleft(event)
            self.counters[prefix] += 1
            self.src_counter[src] += 1

    def draw(self):
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        while True:
            self.stdscr.erase()
            h, w = self.stdscr.getmaxyx()

            # header
            try:
                self.stdscr.addstr(0, 1, "Personal Firewall — live alerts (press 'q' to quit, 'c' clear counts)", curses.A_BOLD)
            except curses.error:
                pass

            # summary area
            with self.lock:
                total_events = sum(self.counters.values())
                top_prefixes = self.counters.most_common(6)
                top_srcs = self.src_counter.most_common(6)
                events_snapshot = list(self.events)[:min(80, h-8)]

            try:
                self.stdscr.addstr(2, 1, f"Total events: {total_events}")
            except curses.error:
                pass
            for idx, (pfx, cnt) in enumerate(top_prefixes):
                try:
                    self.stdscr.addstr(3 + idx, 1, f"{pfx:<20} {cnt:>6}")
                except curses.error:
                    pass

            # srcs
            src_base_row = 3
            try:
                self.stdscr.addstr(2, 40, "Top Source IPs")
            except curses.error:
                pass
            for i, (ip, c) in enumerate(top_srcs):
                try:
                    self.stdscr.addstr(src_base_row + i, 40, f"{ip:<30} {c:>6}")
                except curses.error:
                    pass

            # recent events list
            ev_start_row = max(10, 3 + len(top_prefixes) + 2)
            try:
                self.stdscr.addstr(ev_start_row - 1, 1, "-" * (w - 2))
                self.stdscr.addstr(ev_start_row, 1, f"{'TIME':19}  {'PREFIX':18} {'SRC':22} {'DPT':5} {'PROTO':5}")
            except curses.error:
                pass
            for i, ev in enumerate(events_snapshot[:(h - ev_start_row - 3)]):
                row = ev_start_row + 1 + i
                t = ev['time']
                p = ev['prefix'][:18]
                s = ev['src'][:21]
                dpt = str(ev['dpt'])[:5]
                proto = str(ev['proto'])[:5]
                try:
                    self.stdscr.addstr(row, 1, f"{t:19}  {p:18} {s:22} {dpt:5} {proto:5}")
                except curses.error:
                    pass

            # footer
            footer = "Commands: q=quit  c=clear counters  e=export snapshot"
            try:
                self.stdscr.addstr(h - 1, 1, footer[:w - 2])
            except curses.error:
                pass

            self.stdscr.refresh()

            try:
                ch = self.stdscr.getch()
                if ch == ord('q'):
                    break
                if ch == ord('c'):
                    with self.lock:
                        self.counters.clear()
                        self.src_counter.clear()
                if ch == ord('e'):
                    fname = f"/tmp/firewall_snapshot_{int(time.time())}.log"
                    with open(fname, "w") as fh:
                        with self.lock:
                            for ev in list(self.events):
                                fh.write(ev['raw'] + "\\n")
                    self.stdscr.addstr(h - 2, 1, f"Snapshot saved to {fname}"[:w-2])
                    self.stdscr.refresh()
                    time.sleep(0.9)
            except Exception:
                pass

            time.sleep(0.25)

        self.tailer.stop()

def main(stdscr):
    tui = FirewallTUI(stdscr)
    tui.draw()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("It's recommended to run the TUI as root (to access /var/log/firewall.log).")
    curses.wrapper(main)
