#!/usr/bin/env python3
"""Ping IndexNow with every URL in urls.txt. Run after a deploy: python3 indexnow.py
Tries several endpoints (submissions are shared between IndexNow engines); succeeds if any accepts."""
import json, sys, urllib.request, urllib.error, yaml
key = yaml.safe_load(open("data/site.yaml"))["indexnow_key"]
urls = [u.strip() for u in open("urls.txt") if u.strip()]
body = json.dumps({"host": "digitalprofitreview.com", "key": key, "keyLocation": f"https://digitalprofitreview.com/{key}.txt", "urlList": urls}).encode()
ok = False
for ep in ["https://api.indexnow.org/indexnow", "https://www.bing.com/indexnow", "https://yandex.com/indexnow"]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(ep, body, {"Content-Type": "application/json; charset=utf-8"}), timeout=60)
        print("IndexNow", ep, r.status, len(urls), "urls"); ok = True; break
    except urllib.error.HTTPError as e:
        print("IndexNow", ep, e.code, e.read()[:200].decode(errors="replace"))
    except Exception as e:
        print("IndexNow", ep, "error", e)
sys.exit(0 if ok else 1)
