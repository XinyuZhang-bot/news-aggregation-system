# -*- coding: utf-8 -*-
"""
新闻页面解析辅助：meta 标签提取、正文容器定位、URL 日期推断、请求头构造。
"""

import html
import re
from email.utils import parsedate_to_datetime
from urllib.parse import urljoin, urlparse


EXTRACT_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def get_meta_content_global(html_text: str, attr_name: str, attr_value: str) -> str:
    if not html_text:
        return ""
    rx = re.compile(
        rf'<meta[^>]+{attr_name}=["\']{re.escape(attr_value)}["\'][^>]*content=["\']([^"\']+)["\']',
        re.I,
    )
    match = rx.search(html_text)
    return match.group(1).strip() if match else ""


def build_article_fetch_headers(page_url: str) -> dict:
    headers = dict(EXTRACT_BROWSER_HEADERS)
    page_url = (page_url or "").strip()
    if page_url.startswith("http"):
        try:
            parsed = urlparse(page_url)
            if parsed.scheme and parsed.netloc:
                headers["Referer"] = f"{parsed.scheme}://{parsed.netloc}/"
        except Exception:
            pass
    return headers


def get_meta_property_flexible(html_text: str, prop: str) -> str:
    if not html_text:
        return ""
    value = get_meta_content_global(html_text, "property", prop)
    if value:
        return value.strip()
    rx = re.compile(
        rf'<meta\s[^>]*content=["\']([^"\']+)["\'][^>]*\bproperty=["\']{re.escape(prop)}["\']',
        re.I,
    )
    match = rx.search(html_text)
    return match.group(1).strip() if match else ""


def infer_release_time_from_news_url(url: str) -> str:
    """
    从常见中文新闻 URL 路径提取稿件日期（RSS 的 pubDate 常滞后或不更新时用链接纠偏）。
    返回 YYYY-MM-DD HH:MM:SS；无法识别时返回空。
    """
    u = (url or "").strip()
    if not u:
        return ""
    # 人民网：.../n1/2026/0509/c100286-....html
    m = re.search(r"/n1/(\d{4})/(\d{4})/", u, re.I)
    if m:
        y, md = m.group(1), m.group(2)
        if len(md) == 4 and md.isdigit():
            mo, d = md[:2], md[2:4]
            if 1 <= int(mo) <= 12 and 1 <= int(d) <= 31:
                return f"{y}-{mo}-{d} 12:00:00"
    # 中国新闻网等：.../2026/05-09/10617825.shtml
    m = re.search(r"/(\d{4})/(\d{2})-(\d{2})/", u)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)} 12:00:00"
    # 新华网等：/20260509/ 或路径中含八位日期
    m = re.search(r"/(\d{4})(\d{2})(\d{2})/", u)
    if m:
        y, mo, d = m.group(1), m.group(2), m.group(3)
        if 1 <= int(mo) <= 12 and 1 <= int(d) <= 31:
            return f"{y}-{mo}-{d} 12:00:00"
    m = re.search(r"/(\d{4})-(\d{2})-(\d{2})/", u)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)} 12:00:00"
    return ""


def _date_key_for_compare(s: str) -> str:
    """YYYY-MM-DD 或空，用于比较哪一侧日期更新。"""
    s = (s or "").strip()
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    try:
        dt = parsedate_to_datetime(s)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return ""


def coalesce_release_time_with_url(page_url: str, release_time: str) -> str:
    """
    合并页面 / RSS 给出的时间与 URL 推断时间：若 URL 日期更晚，采用 URL（缓解人民网等 RSS pubDate 长期不刷新）。
    """
    inferred = infer_release_time_from_news_url(page_url)
    r = (release_time or "").strip()
    if not inferred:
        return r
    if not r:
        return inferred
    ki, kr = _date_key_for_compare(inferred), _date_key_for_compare(r)
    if ki and kr and ki > kr:
        return inferred
    return r


def extract_video_url_from_html(html_text: str, page_url: str) -> str:
    if not html_text:
        return ""
    candidates = []
    for prop in ("og:video:url", "og:video:secure_url", "og:video"):
        url = get_meta_content_global(html_text, "property", prop)
        if url:
            candidates.append(url)
    match = re.search(r'<video[^>]+src=["\']([^"\']+)["\']', html_text, re.I)
    if match:
        candidates.append(match.group(1))
    match = re.search(r'<source[^>]+src=["\']([^"\']+)["\'][^>]+type=["\']video/', html_text, re.I)
    if match:
        candidates.append(match.group(1))
    match = re.search(r'"(?:videoUrl|video_url|playUrl|play_url)"\s*:\s*"([^"]+)"', html_text)
    if match:
        candidates.append(match.group(1))
    for raw in candidates:
        url = (raw or "").strip()
        if not url:
            continue
        if url.startswith("//"):
            url = "https:" + url
        elif url.startswith("/"):
            url = urljoin(page_url, url)
        elif not re.match(r"^https?://", url, flags=re.I):
            url = urljoin(page_url, url)
        if re.search(r"\.(m3u8|mp4|flv|webm)(\?|#|$)", url, re.I):
            return url
        if "video" in url.lower() or "m3u8" in url.lower() or "vod" in url.lower():
            return url
    return ""


def extract_balanced_div_from_index(html_text: str, start_index: int) -> str:
    if not html_text or start_index < 0 or start_index >= len(html_text):
        return ""
    token_re = re.compile(r"</?div\b[^>]*>", re.I)
    depth = 0
    start = -1
    for match in token_re.finditer(html_text, pos=start_index):
        tag = match.group(0)
        is_close = tag.startswith("</")
        if not is_close:
            if start == -1:
                start = match.start()
            depth += 1
        elif start != -1:
            depth -= 1
            if depth <= 0:
                return html_text[start:match.end()]
    return ""


def extract_paragraph_block_from_scripts(html_text: str) -> str:
    if not html_text:
        return ""
    scripts = re.findall(r"<script[^>]*>([\s\S]*?)</script>", html_text, re.I)
    best = ""
    best_score = 0
    for script_text in scripts:
        if "<p" not in script_text.lower():
            continue
        blocks = re.findall(r"((?:<p[^>]*>[\s\S]*?</p>\s*){2,})", script_text, re.I)
        for block in blocks:
            cleaned = re.sub(r"<[^>]+>", " ", block)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            score = len(html.unescape(cleaned))
            if score > best_score and score >= 120:
                best_score = score
                best = block
    return best
