#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, etc.) with every URL in urls.txt. Run after a deploy: python3 indexnow.py"""
import json, urllib.request, yaml
key = yaml.safe_load(open("data/site.yaml"))["indexnow_key"]
urls = [u.strip() for u in open("urls.txt") if u.strip()]
body = json.dumps({"host": "digitalprofitreview.com", "key": key, "keyLocation": f"https://digitalprofitreview.com/{key}.txt", "urlList": urls}).encode()
r = urllib.request.urlopen(urllib.request.Request("https://api.indexnow.org/indexnow", body, {"Content-Type": "application/json; charset=utf-8"}))
print("IndexNow", r.status, len(urls), "urls")
