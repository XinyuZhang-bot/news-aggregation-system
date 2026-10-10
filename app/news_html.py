# -*- coding: utf-8 -*-
"""新闻富文本字段清洗：仅保留文字与常规排版标签，移除图片与嵌入式媒体。"""
import re


def strip_news_media_markup(html: str) -> str:
    if not html:
        return ""
    s = str(html)
    block_patterns = (
        r"<picture\b[^>]*>[\s\S]*?</picture>",
        r"<figure\b[^>]*>[\s\S]*?</figure>",
        r"<video\b[^>]*>[\s\S]*?</video>",
        r"<audio\b[^>]*>[\s\S]*?</audio>",
        r"<iframe\b[^>]*>[\s\S]*?</iframe>",
        r"<object\b[^>]*>[\s\S]*?</object>",
        r"<svg\b[^>]*>[\s\S]*?</svg>",
    )
    for pat in block_patterns:
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
