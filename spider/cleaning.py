# -*- coding: utf-8 -*-
"""
爬虫正文清洗：去 HTML 噪声、视频占位、广告段落，规范化图片 URL。
供 app.py 的 /spider 与 /extract 共用。
"""

import html
import re
from urllib.parse import urljoin


def collect_content_image_urls(html_frag: str, base_url: str, limit: int = 40) -> list:
    if not html_frag:
        return []
    out = []
    for im in re.finditer(r"<img\b[^>]*(?:/>|>)", html_frag[:500000], re.I):
        url = pick_best_image_url_from_img_tag(im.group(0))
        if not url:
            continue
        url = normalize_media_url_with_base(base_url or "", url)
        if not url or is_trivial_or_placeholder_img_url(url) or is_generic_site_logo_or_brand_img_url(url):
            continue
        if url not in out:
            out.append(url)
        if len(out) >= int(limit):
            break
    return out


def inject_images_before_body(body_html: str, image_urls: list, max_n: int = 12) -> str:
    if not image_urls:
        return body_html or ""
    body_html = body_html or ""
    if re.search(r"<img\b", body_html, re.I):
        return body_html
    chunks = []
    for url in image_urls[:max_n]:
        esc = html.escape(url, quote=True)
        chunks.append(
            f'<p><img src="{esc}" style="max-width:100%;height:auto;" '
            f'referrerpolicy="no-referrer" loading="lazy" alt="" /></p>'
        )
    return ("\n".join(chunks) + "\n" + body_html).strip()


def strip_html_comments(html_text: str) -> str:
    if not html_text:
        return ""
    text = re.sub(r"<!--[\s\S]*?-->", "", html_text)
    text = re.sub(r"(?m)^\s*-->\s*$", "", text)
    return text


def strip_all_image_markup(text: str) -> str:
    """
    Remove image / embedded media markup from stored article text so crawled news
    stays text-first (aligned with portal policy); strips picture/figure/video/etc.
    """
    if not text:
        return ""
    s = text
    for pat in (
        r"<picture\b[^>]*>[\s\S]*?</picture>",
        r"<figure\b[^>]*>[\s\S]*?</figure>",
        r"<video\b[^>]*>[\s\S]*?</video>",
        r"<audio\b[^>]*>[\s\S]*?</audio>",
        r"<iframe\b[^>]*>[\s\S]*?</iframe>",
        r"<object\b[^>]*>[\s\S]*?</object>",
        r"<svg\b[^>]*>[\s\S]*?</svg>",
    ):
        s = re.sub(pat, "", s, flags=re.I)
    s = re.sub(r"<iframe\b[^>]*/>", "", s, flags=re.I)
    s = re.sub(r"<embed\b[^>]*/?>", "", s, flags=re.I)
    s = re.sub(r"<img\b[^>]*(?:/>|>)", "", s, flags=re.I)
    s = re.sub(r"<image\b[^>]*(?:/>|>)", "", s, flags=re.I)
    s = re.sub(r"<source\b[^>]*(?:/>|>)", "", s, flags=re.I)
    s = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", s)
    s = re.sub(r"<p>\s*(?:<br\s*/?>|\s)*</p>", "", s, flags=re.I)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def paragraph_fingerprint(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", "", text)
    return text[:800]


def dedupe_paragraph_body(body: str, min_len: int = 20) -> str:
    if not (body and body.strip()):
        return body or ""
    parts = re.split(r"\n\s*\n+", body.strip())
    seen = set()
    out = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if len(part) >= min_len:
            fp = paragraph_fingerprint(part)
            if fp in seen:
                continue
            seen.add(fp)
        out.append(part)
    return "\n\n".join(out).strip()


def collapse_duplicate_title_echo(body: str, title: str) -> str:
    if not body or not title:
        return body
    core = re.sub(r"^\[[^\]]+\]\s*", "", (title or "").strip())
    if len(core) < 10:
        core = (title or "").strip()
    if len(core) < 10:
        return body
    first = body.find(core)
    if first == -1:
        return body
    second = body.find(core, first + len(core))
    if second == -1:
        return body
    between = body[first + len(core) : second].strip()
    if len(between) > 100:
        return body
    return (body[:second] + body[second + len(core) :]).strip()


def dedupe_cn_sentence_runs(body: str) -> str:
    if not body:
        return body
    frags = re.split(r"(?<=[。！？!?])", body)
    seen = set()
    out = []
    for frag in frags:
        frag = frag.strip()
        if not frag:
            continue
        fp = paragraph_fingerprint(frag)
        if len(frag) >= 16 and fp in seen:
            continue
        if len(frag) >= 16:
            seen.add(fp)
        out.append(frag)
    return "".join(out).strip()


def is_trivial_or_placeholder_img_url(url: str) -> bool:
    if not url:
        return True
    url = (url or "").strip()
    if len(url) < 6:
        return True
    low = url.lower()
    if low.startswith(("javascript:", "about:blank", "#")):
        return True
    if low.startswith("data:") and "image/svg" in low:
        return True
    bad_frag = (
        "placeholder",
        "lazyload",
        "loading.gif",
        "blank.gif",
        "space.gif",
        "pixel.gif",
        "spacer.gif",
        "1x1",
        "grey.gif",
        "gray.gif",
        "blank.png",
        "base64,",
    )
    return any(item in low for item in bad_frag)


def normalize_media_url_with_base(base_url: str, url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    url = html.unescape(url).strip()
    url = url.split()[0].strip()
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        try:
            return urljoin(base_url or "", url)
        except Exception:
            return url
    if not re.match(r"^https?://", url, flags=re.I):
        try:
            return urljoin(base_url or "", url)
        except Exception:
            return url
    return url


_IMG_ATTR_PRIORITY = (
    "data-original",
    "data-original-src",
    "data-actualsrc",
    "data-actual-src",
    "data-src",
    "data-lazy",
    "data-lazyload",
    "data-lazy-srcset",
    "data-srcset",
    "data-echo",
    "data-img",
    "data-image",
    "data-lazy-src",
    "data-url",
    "data-newsapp-pic",
    "data-pb-zdx",
    "data-imgs",
    "src",
)


def pick_best_image_url_from_img_tag(tag: str) -> str:
    if not tag:
        return ""
    attrs = {}
    for match in re.finditer(
        r'\b([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s"\'=<>`]+))',
        tag,
    ):
        attrs[match.group(1).lower()] = (
            match.group(2) or match.group(3) or match.group(4) or ""
        ).strip()
    for key in _IMG_ATTR_PRIORITY:
        if key not in attrs:
            continue
        url = html.unescape(attrs[key] or "").strip().split()[0]
        if not url or is_trivial_or_placeholder_img_url(url):
            continue
        return url
    srcset = attrs.get("srcset", "") or attrs.get("data-srcset", "") or attrs.get("data-lazy-srcset", "")
    if srcset:
        part = srcset.split(",")[0].strip().split()[0].strip()
        if part and not is_trivial_or_placeholder_img_url(part):
            return html.unescape(part)
    return ""


def strip_inline_media_captions(text: str) -> str:
    if not text:
        return text
    for pattern in (
        r"[（(]\s*受访者供图\s*[）)]",
        r"受访者供图",
        r"图由受访者提供",
        r"图片由受访者提供",
        r"[（(]本文图片除标注外均为[^）]+[）)]",
        r"[（(]图片来源[:：][^）]+[）)]",
        r"\(本文图片[^)]+\)",
        r"（本文图片[^）]+）",
    ):
        text = re.sub(pattern, "", text, flags=re.I)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+([。，、；：！？])", r"\1", text)
    return text.strip()


VIDEO_READ_ORIGINAL_NOTICE = "观看详细视频请点击「阅读原文」跳转后查看。"

_VIDEO_READ_NOTICE_PATTERN = re.compile(
    r"观看详细视频请点击\s*[「\"'『]?阅读原文[」\"'』]?\s*跳转后查看。?",
    re.M,
)


def strip_html_video_code_blocks(text: str) -> str:
    if not text:
        return ""
    # 部分站点用非标准注释包裹 htmlVideoCode 占位块，需单独模式覆盖。
    text = re.sub(
        r"!?\-\-\s*begin:htmlVideoCode\s*\-\-[\s\S]*?!?\-\-\s*end:htmlVideoCode\s*\-\-",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<!--\s*begin:htmlVideoCode\s*-->[\s\S]*?<!--\s*end:htmlVideoCode\s*-->",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"!?-?-?\s*begin:htmlVideoCode\s*-?-?>[\s\S]*?!?-?-?\s*end:htmlVideoCode\s*-?-?>",
        "",
        text,
        flags=re.I,
    )
    return text.strip()


def dedupe_consecutive_lines(text: str) -> str:
    if not text:
        return ""
    out = []
    prev_nonempty = None
    for line in text.replace("\r\n", "\n").split("\n"):
        key = line.strip()
        if key and key == prev_nonempty:
            continue
        out.append(line)
        if key:
            prev_nonempty = key
    return "\n".join(out).strip()


def strip_all_video_read_notices(text: str) -> str:
    if not text:
        return ""
    text = _VIDEO_READ_NOTICE_PATTERN.sub("", text)
    text = re.sub(re.escape(VIDEO_READ_ORIGINAL_NOTICE) + r"[\s\u3000]*", "", text)
    text = re.sub(
        r"(<p[^>]*>\s*)" + re.escape(VIDEO_READ_ORIGINAL_NOTICE) + r"\s*</p>",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def ensure_video_read_notice_once_plain(text: str, page_url: str) -> str:
    text = strip_html_video_code_blocks(text or "")
    text = strip_all_video_read_notices(text)
    text = dedupe_consecutive_lines(text)
    text = strip_player_promo_noise(text).strip()
    if is_video_news_url(page_url or ""):
        if not text:
            return VIDEO_READ_ORIGINAL_NOTICE
        return text + "\n\n" + VIDEO_READ_ORIGINAL_NOTICE
    return text


def strip_player_promo_noise(text: str) -> str:
    if not text:
        return ""
    out_lines = []
    for raw in text.replace("\r\n", "\n").split("\n"):
        line = raw.strip()
        if not line:
            continue
        if re.match(
            r"^(正在播放|即将播放|正在直播|节目单|选集|倍速|画中画|新闻直播间|新闻联播|朝闻天下|焦点访谈|新闻30分|新闻周刊|环球视线)\S*",
            line,
        ):
            continue
        line = re.sub(
            r"^(新闻直播间|新闻联播|朝闻天下|焦点访谈|新闻30分|新闻周刊|环球视线|午夜新闻|晚间新闻|中国新闻)\s+",
            "",
            line,
        )
        line = re.sub(r"(正在播放|即将播放|正在直播|精彩看点|节目预告).*$", "", line)
        line = re.sub(r"\s{2,}", " ", line).strip()
        if line:
            out_lines.append(line)
    joined = "\n".join(out_lines).strip()
    joined = re.sub(r"(正在播放|即将播放|正在直播).{0,160}$", "", joined, flags=re.M)
    return re.sub(r"\s{2,}", " ", joined).strip()


def is_video_news_url(url: str) -> bool:
    url = (url or "").strip().lower()
    if not url:
        return False
    if "v.qq.com" in url or "live.qq.com" in url:
        return True
    if "video" in url and ("people.com.cn" in url or "xinhuanet.com" in url or "chinanews.com.cn" in url):
        return True
    return False


def is_generic_site_logo_or_brand_img_url(url: str) -> bool:
    if not url:
        return True
    low = url.lower()
    keys = (
        "logo",
        "/icon",
        "favicon",
        "share.png",
        "share.jpg",
        "qrcode",
        "二维码",
        "avatar",
        "program",
        "客户端",
        "download",
        "sprite",
        "placeholder",
    )
    return any(key in low for key in keys)


def rewrite_img_tags_in_html(html_text: str, base_url: str) -> str:
    if not html_text or "<img" not in html_text.lower():
        return html_text

    def repl(match):
        tag = match.group(0)
        url = pick_best_image_url_from_img_tag(tag)
        if not url:
            return ""
        url = normalize_media_url_with_base(base_url, url)
        if not url or is_trivial_or_placeholder_img_url(url):
            return ""
        esc = html.escape(url, quote=True)
        return (
            f'<img src="{esc}" loading="lazy" referrerpolicy="no-referrer" '
            f'style="max-width:100%;height:auto;" alt="" />'
        )

    return re.sub(r"<img\b[^>]*(?:/>|>)", repl, html_text, flags=re.I)


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
        else:
            if start != -1:
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
            score = len(cleaned)
            if score > best_score and score >= 120:
                best_score = score
                best = block
    return best
