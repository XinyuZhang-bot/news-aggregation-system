# -*- coding: utf-8 -*-
"""人民网链接探测脚本，仅供手动调试，不参与线上服务。"""
import re
import requests

UA = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0"}
URLS = [
    "http://politics.people.com.cn/",
    "http://world.people.com.cn/",
    "http://finance.people.com.cn/",
    "http://www.people.com.cn/",
]
pat = re.compile(r"https?://[a-z0-9.]+\.people\.com\.cn/n1/\d{4}/\d{4}/[^\"'<> ]+\.html", re.I)

for u in URLS:
    try:
        r = requests.get(u, headers=UA, timeout=20)
        t = r.text
        links = list(dict.fromkeys(pat.findall(t)))
        years = {}
        for lk in links:
            m = re.search(r"/n1/(\d{4})/(\d{4})/", lk)
            if m:
                years.setdefault(m.group(1), 0)
                years[m.group(1)] += 1
        print(u, r.status_code, "unique_n1", len(links), "years", sorted(years.items(), key=lambda x: -x[1])[:5])
        if links:
            print("  first3:", links[:3])
    except Exception as e:
        print(u, e)
