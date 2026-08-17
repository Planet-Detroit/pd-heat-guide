#!/usr/bin/env python3
"""Fetches every external http(s) link in index.html (and es/index.html if it exists)
and exits non-zero if any returns an error. Used by the monthly GitHub Action; you can
also run it by hand: python3 tests/check_links.py
"""
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")

urls = set()
for f in [ROOT / "index.html", ROOT / "es" / "index.html"]:
    if f.exists():
        urls |= set(re.findall(r'href="(https?://[^"]+)"', f.read_text()))
urls = {u for u in urls if "googletagmanager" not in u}

bad = []
for u in sorted(urls):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
        with urllib.request.urlopen(req, timeout=30) as r:
            code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:  # DNS failure, timeout, etc.
        code = str(e)[:60]
    ok = code in (200, 202, 301, 302, 303, 307, 308)
    # 403 = the site's bot protection refused us (CDC does this), NOT a dead page.
    # A removed page returns 404, which we still catch. Flag 403 for a manual look.
    if code == 403:
        print(f"  WARN 403  {u}  (blocked automated check — open it in a browser to confirm)")
        continue
    print(f"  {'OK ' if ok else 'BAD'}  {code}  {u}")
    if not ok:
        bad.append((code, u))

print()
if bad:
    print(f"{len(bad)} broken link(s)")
    sys.exit(1)
print("All links OK")
