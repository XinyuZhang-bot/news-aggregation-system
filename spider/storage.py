# -*- coding: utf-8 -*-
"""入库前去重：新闻 URL 规范化（协议/域名/路径统一），用于生成 unique_id。"""

import html
import re
from urllib.parse import urlparse, urlunparse


def normalize_news_url(url: str) -> str:
    """将 URL 规范化为 scheme+host+path+query，便于 MD5 去重。"""
    url = html.unescape((url or "").strip())
    if not url:
        return ""
    if not re.match(r"^https?://", url, re.I):
        url = "http://" + url
    try:
        parsed = urlparse(url)
        scheme = (parsed.scheme or "http").lower()
        netloc = (parsed.netloc or "").lower()
        path = (parsed.path or "").rstrip("/")
        return urlunparse((scheme, netloc, path, "", parsed.query or "", ""))
    except Exception:
        return url.strip().rstrip("/")
