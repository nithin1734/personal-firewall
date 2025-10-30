#!/usr/bin/env python3
# Minimal alert sender that tails /var/log/firewall.log and posts to a webhook.
import time, re, requests, os, sys

LOG = '/var/log/firewall.log'
WEBHOOK = os.environ.get('FW_WEBHOOK') or 'https://example.com/webhook'  # set to your endpoint
PRIORITY_PREFIXES = ('FW-DROP-SSH', 'FW-DROP-BLOCKEDPORT')

pat = re.compile(r'(FW-[A-Z0-9-]+):.*?SRC=(?P<src>[0-9a-fA-F:\.]+).*?DPT=(?P<dpt>\d+)?', re.I)

def tail_and_send():
    while not os.path.exists(LOG):
        time.sleep(0.5)
    with open(LOG, 'r', errors='replace') as fh:
        fh.seek(0,2)
        while True:
            line = fh.readline()
            if not line:
                time.sleep(0.5)
                continue
            m = pat.search(line)
            if not m:
                continue
            pfx = m.group(1)
            if any(pfx.startswith(pref) for pref in PRIORITY_PREFIXES):
                payload = {'prefix': pfx, 'src': m.group('src'), 'dpt': m.group('dpt') or ''}
                try:
                    requests.post(WEBHOOK, json=payload, timeout=5)
                except Exception:
                    pass

if __name__ == '__main__':
    tail_and_send()
