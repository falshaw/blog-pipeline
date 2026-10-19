#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Naver, Seznam, ...) with newly published URLs. Stdlib only.

The key must already be live at https://<host>/<key>.txt (file content = the key).

Usage:
  INDEXNOW_KEY=abc123 python indexnow-ping.py example.com https://example.com/blog/a/ https://example.com/de/blog/b/
  python indexnow-ping.py --key abc123 example.com <url> [<url> ...]
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("host")
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--key", default=os.environ.get("INDEXNOW_KEY"))
    ap.add_argument("--endpoint", default="https://api.indexnow.org/indexnow")
    a = ap.parse_args()
    if not a.key:
        sys.exit("No key: pass --key or set INDEXNOW_KEY.")
    bad = [u for u in a.urls if f"//{a.host}/" not in u]
    if bad:
        sys.exit(f"URLs not on host {a.host}: {bad}")
    payload = {"host": a.host, "key": a.key, "keyLocation": f"https://{a.host}/{a.key}.txt", "urlList": a.urls}
    req = urllib.request.Request(a.endpoint, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"IndexNow {r.status} for {len(a.urls)} URL(s)")
    except urllib.error.HTTPError as e:
        # 200/202 = accepted; 403 = key not found at keyLocation; 422 = URL/host mismatch; 429 = too many requests
        sys.exit(f"IndexNow HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


if __name__ == "__main__":
    main()
