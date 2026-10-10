# -*- coding: utf-8 -*-
"""
新闻爬虫 Flask 微服务（默认端口 5001）。

职责：
  - 按新闻源抓取列表/详情，清洗、分类后写入 news_resources 表
  - 记录 crawl_run 运行日志，更新 news_source 最近状态
  - 提供 /extract 单篇正文抽取（供后台发布页使用）
  - 启动时挂载 scheduler_jobs 定时任务

与 Django 主服务（:5000）共用 MySQL，需独立运行本文件。
"""
from flask import Flask, request, jsonify, Response, redirect
import os
import sys
import time
import configparser
import requests
import pandas as pd
import json
from sqlalchemy import create_engine
import random
from flask_cors import CORS
import hashlib
import re
from datetime import datetime, timedelta
import uuid
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET
import html
from urllib.parse import urljoin, urlparse
import classify as classify_module
import cleaning as cleaning_module
import sources as sources_module
import storage as storage_module

app=Flask(__name__)
CORS(app)

_SPIDER_ROOT = os.path.dirname(os.path.abspath(__file__))
if _SPIDER_ROOT not in sys.path:
    sys.path.insert(0, _SPIDER_ROOT)


REQUIRED_NEWS_FIELDS = [
    "title",
    "url",
    "origin",
    "release_time",
    "content",
]
MIN_CONTENT_LEN_STRICT = 80
MIN_CONTENT_LEN_RELAXED = 40

# 单次入库条数（演示：每源每次最多写入 5 条；与库内去重后再截取）
CRAWL_LIMIT = 5
RAW_FETCH_LIMIT = 400
MAX_NEWS_AGE_DAYS = 3
# 严格清洗后不足该条数时启用放宽兜底（与 CRAWL_LIMIT 对齐便于演示）
MIN_VALID_NEWS_FALLBACK = 5

# 发布来源别名 → 标准名（与 news_source.name / SPIDER_DEFAULT_SOURCES 一致）。
# 写入 news_resources.origin 前，将页面 meta、RSS 中的简称/变体归一化。
# 仅包含当前已接入的四个源；新增源时在此补充别名。
SOURCE_NAME_MAP = {
    "中国新闻网": "中国新闻网",
    "中新网": "中国新闻网",
    "新华社": "新华社",
    "新华网": "新华社",
    "人民网": "人民网",
    "人民日报": "人民网",
    "腾讯新闻": "腾讯新闻",
    "腾讯": "腾讯新闻",
}

SPIDER_DEFAULT_SOURCES = [
    # code 与 news_source 表、/spider?source= 参数一致
    {"code": "tencent", "name": "腾讯新闻", "enabled": True, "source_type": "builtin", "parser_type": "builtin", "parser_name": "tencent", "interval_minutes": 30, "priority": 90, "base_url": "https://news.qq.com/", "list_urls": "https://news.qq.com/", "extra_json": json.dumps({"origin_name": "腾讯新闻"}, ensure_ascii=False)},
    {"code": "people", "name": "人民网", "enabled": True, "source_type": "builtin", "parser_type": "builtin", "parser_name": "people", "interval_minutes": 30, "priority": 92, "base_url": "http://www.people.com.cn/", "list_urls": "", "extra_json": json.dumps({"origin_name": "人民网", "list_seeds": "", "rss_feeds": "", "people_use_rss": False}, ensure_ascii=False)},
    {"code": "xinhuanet", "name": "新华社", "enabled": True, "source_type": "builtin", "parser_type": "builtin", "parser_name": "xinhuanet", "interval_minutes": 30, "priority": 94, "base_url": "http://www.news.cn/", "list_urls": "http://www.news.cn/", "extra_json": json.dumps({"origin_name": "新华社"}, ensure_ascii=False)},
    {"code": "chinanews", "name": "中国新闻网", "enabled": True, "source_type": "builtin", "parser_type": "builtin", "parser_name": "chinanews", "interval_minutes": 30, "priority": 88, "base_url": "https://www.chinanews.com.cn/", "list_urls": "https://www.chinanews.com.cn/", "extra_json": json.dumps({"origin_name": "中国新闻网"}, ensure_ascii=False)},
]


def _load_db_settings():
    parser = configparser.ConfigParser()
    parser.read(os.path.join(_SPIDER_ROOT, "config", "config.ini"), encoding="utf-8")
    if not parser.has_section("db"):
        return None
    try:
        return {
            "user": parser.get("db", "user"),
            "password": parser.get("db", "password").replace("!", "%21").replace("@", "%40"),
            "host": parser.get("db", "host"),
            "port": parser.get("db", "port"),
            "database": parser.get("db", "database"),
            "table_name": parser.get("db", "table_name"),
        }
    except Exception:
        return None


def _get_db_engine():
    settings = _load_db_settings()
    if not settings:
        return None
    try:
        return create_engine(
            "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                settings["user"], settings["password"], settings["host"], settings["port"], settings["database"]
            )
        )
    except Exception:
        return None


def _safe_json_loads(value, default=None):
    if default is None:
        default = {}
    if not value:
        return default
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else default
    except Exception:
        return default


def _load_source_configs():
    engine = _get_db_engine()
    if engine is not None:
        try:
            df = pd.read_sql(
                "SELECT * FROM `news_source` ORDER BY `priority` DESC, `news_source_id` ASC",
                engine,
            )
            if not df.empty:
                rows = df.replace({pd.NA: None}).to_dict("records")
                for row in rows:
                    row["code"] = str(row.get("code") or "").strip().lower()
                    row["name"] = str(row.get("name") or "").strip()
                    row["enabled"] = bool(int(row.get("enabled") or 0))
                return rows
        except Exception:
            pass
    return [dict(item) for item in SPIDER_DEFAULT_SOURCES]


def _get_source_config(code: str):
    code = (code or "").strip().lower()
    for row in _load_source_configs():
        if (row.get("code") or "").strip().lower() == code:
            return row
    return None


def _configured_feed_urls(source_cfg):
    urls = [x.strip() for x in str(source_cfg.get("list_urls") or "").splitlines() if x.strip()]
    feed_urls = []
    for url in urls:
        low = url.lower()
        if low.endswith(".xml") or "/rss/" in low or "rss." in low or "atom" in low or "feed" in low:
            feed_urls.append(url)
    return feed_urls


def _http_get_ignore_proxy(url, *, headers=None, timeout=15, allow_redirects=True):
    """
    直连 GET，不使用环境变量中的 HTTP(S)_PROXY。
    部分环境下 NO_PROXY 未包含 qq.com，导致腾讯域名仍走失效代理而报错 ProxyError；
    人民网/新华社等常见 http 域名可能未走同一代理规则，表现不一致。
    """
    hdrs = headers if headers is not None else {}
    with requests.Session() as sess:
        sess.trust_env = False
        return sess.get(url, headers=hdrs, timeout=timeout, allow_redirects=allow_redirects)


def _record_crawl_run_start(source_cfg):
    engine = _get_db_engine()
    if engine is None:
        return None
    run_id = "run_" + uuid.uuid4().hex[:16]
    conn = None
    try:
        conn = engine.raw_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO `crawl_run` (`run_id`, `source_code`, `source_name`, `status`, `started_at`, `summary`) "
            "VALUES (%s, %s, %s, %s, NOW(), %s)",
            (
                run_id,
                source_cfg.get("code") or "",
                source_cfg.get("name") or source_cfg.get("code") or "",
                "running",
                "任务已启动",
            ),
        )
        cur.execute(
            "UPDATE `news_source` SET `last_run_at` = NOW(), `last_status` = %s WHERE `code` = %s",
            ("running", source_cfg.get("code") or ""),
        )
        conn.commit()
        return run_id
    except Exception:
        try:
            if conn is not None:
                conn.rollback()
        except Exception:
            pass
        return None
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass


def _record_crawl_run_finish(run_id, source_cfg, status, stats):
    engine = _get_db_engine()
    if engine is None or not run_id:
        return
    conn = None
    try:
        conn = engine.raw_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE `crawl_run` SET `status`=%s, `fetched_count`=%s, `written_count`=%s, `dropped_count`=%s, "
            "`error_message`=%s, `summary`=%s, `finished_at`=NOW() WHERE `run_id`=%s",
            (
                status,
                int(stats.get("fetched_count") or 0),
                int(stats.get("written_count") or 0),
                int(stats.get("dropped_count") or 0),
                str(stats.get("error_message") or "")[:1000],
                str(stats.get("summary") or "")[:1000],
                run_id,
            ),
        )
        cur.execute(
            "UPDATE `news_source` SET `last_run_at` = NOW(), `last_status` = %s WHERE `code` = %s",
            (status, source_cfg.get("code") or ""),
        )
        conn.commit()
    except Exception:
        try:
            if conn is not None:
                conn.rollback()
        except Exception:
            pass
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass


def _purge_invalid_news_rows(engine, table_name: str, max_age_days: int):
    """
    清理数据库中不符合规则的数据：
    - 超出最近天数
    - 视频稿（通过 url/content 特征命中）
    - 正文过短
    """
    if engine is None or not table_name:
        return

    try:
        cols = set(
            pd.read_sql(f"SHOW COLUMNS FROM `{table_name}`", engine)["Field"]
            .astype(str)
            .tolist()
        )
    except Exception:
        cols = set()

    required = {"release_time", "url", "img", "content"}
    if not required.issubset(cols):
        return

    threshold = datetime.now() - timedelta(days=int(max_age_days))
    threshold_str = threshold.strftime("%Y-%m-%d %H:%M:%S")

    video_conditions = [
        "url LIKE '%/VIDEO%.shtml%'",
        "url LIKE '%v.qq.com%'",
        "url LIKE '%live.qq.com%'",
        "content LIKE '%mp4%'",
        "content LIKE '%m3u8%'",
        "content LIKE '%htmlVideoCode%'",
        "content LIKE '%newPlayer%'",
        "content LIKE '%观看详细视频%'",
        "content LIKE '%播放器%'",
        "content LIKE '%video/%'",
        "content LIKE '%videoplayer%'",
        "content LIKE '%begin:htmlVideoCode%'",
    ]

    invalid_conditions = [
        f"(release_time IS NULL OR release_time='' OR release_time < '{threshold_str}')",
        "(content IS NULL OR content='' OR CHAR_LENGTH(content) < 40)",
        "(" + " OR ".join(video_conditions) + ")",
    ]

    where_sql = " OR ".join(invalid_conditions)
    sql = f"DELETE FROM `{table_name}` WHERE {where_sql}"

    conn = None
    try:
        conn = engine.raw_connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Exception:
        try:
            if conn is not None:
                conn.rollback()
        except Exception:
            pass
    finally:
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# HTTP 路由
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    """根路径重定向到 Django 管理后台登录页。"""
    return redirect("http://127.0.0.1:5000/static/admin/dist/index.html#/login", code=302)

@app.route("/sources", methods=["GET"])
def sources():
    return jsonify(
        {
            "sources": [
                {
                    "id": row.get("code"),
                    "name": row.get("name") or row.get("code"),
                    "enabled": bool(row.get("enabled")),
                    "parser_name": row.get("parser_name") or row.get("code"),
                    "source_type": row.get("source_type") or "builtin",
                }
                for row in _load_source_configs()
            ]
        }
    )


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    # 避免浏览器请求 favicon 时产生 404 日志
    return Response(status=204)

@app.route("/extract", methods=["GET"])
def extract():
    """
    Extract original article link, html content (with images), and images list.
    Used by admin publish page to generate "阅读原文" and keep images in body.
    """
    url = (request.args.get("url") or "").strip()
    if not url:
        return jsonify({"ok": False, "error": "missing url"}), 400

    def _clean_text_local(s: str) -> str:
        if s is None:
            return ""
        s = html.unescape(str(s))
        s = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def _strip_html_local(s: str) -> str:
        if not s:
            return ""
        # keep <br> as newline placeholders
        s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
        s = re.sub(r"<script[^>]*>[\\s\\S]*?</script>", "", s, flags=re.I)
        s = re.sub(r"<style[^>]*>[\\s\\S]*?</style>", "", s, flags=re.I)
        s = re.sub(r"<[^>]+>", "", s)
        # normalize spaces but keep newlines
        s = s.replace("\r", "\n")
        lines = [re.sub(r"\s+", " ", ln).strip() for ln in s.split("\n")]
        lines = [ln for ln in lines if ln]
        return "\n".join(lines).strip()

    def _normalize_media_url_local(u: str) -> str:
        u = _clean_text_local(u)
        if not u:
            return ""
        if u.startswith("//"):
            return "https:" + u
        # relative -> absolute
        if u.startswith("/"):
            return urljoin(resp.url, u)
        if not re.match(r"^https?://", u, flags=re.I):
            # handle relative like ./a.jpg or a.jpg
            return urljoin(resp.url, u)
        return u

    try:
        # 与腾讯等 https 源一致：避免环境 HTTP(S)_PROXY 指向失效代理导致拉取失败
        resp = _http_get_ignore_proxy(
            url,
            headers=sources_module.build_article_fetch_headers(url),
            timeout=28,
            allow_redirects=True,
        )
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        text = cleaning_module.strip_html_comments(resp.text or "")
        # 先清理站点常见的 htmlVideoCode 视频占位块，避免误判
        text = cleaning_module.strip_html_video_code_blocks(text)
        if not text.strip():
            return jsonify({"ok": False, "error": "empty response"}), 502
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502

    # 真实文章链接：如果被重定向到图片资源（如 share.png），则回退到原始 url
    final_url = resp.url or url
    ct = (resp.headers.get("content-type") or "").lower()
    if ("image/" in ct) or re.search(r"\.(png|jpe?g|gif|webp)(\?|#|$)", final_url, re.I):
        final_url = url

    try:
        final_host = (urlparse(final_url).netloc or "").lower()
    except Exception:
        final_host = ""
    is_chinanews = "chinanews.com.cn" in final_host

    def looks_like_video_html(html_text: str, page_url: str) -> bool:
        """
        尽量用“页面原始 HTML 特征”判断是否为视频稿。
        用于阻止 /extract 返回含视频播放器的 body_html，避免前台展示视频。
        """
        u = (page_url or "").strip()
        if cleaning_module.is_video_news_url(u):
            return True
        t = (html_text or "").lower()
        # 只把“高置信度真实视频”判为视频：
        # - <video 标签
        # - mp4/m3u8 媒体资源
        # - 常见视频播放器标识（videoplayer/video_url）
        # 注意：如 htmlVideoCode/newPlayer 这类标记在部分站点可能也用于“非视频模块”占位，
        # 已有 strip_html_video_code_blocks(body_html) 的兜底，因此这里避免因为这些误判而让 extract 失败。
        high_confidence = [
            "<video",
            ".mp4",
            ".m3u8",
            "m3u8",
            "videoplayer",
        ]
        if any(p in t for p in high_confidence):
            return True

        # iframe/embed 携带明确视频资源时才判定
        if "iframe" in t and (".mp4" in t or ".m3u8" in t or "videoplayer" in t):
            return True

        return False

    # 若疑似视频稿：让 extract 失败（ok:false），由后台兜底不写入含视频的正文。
    if looks_like_video_html(text, final_url):
        return jsonify({"ok": False, "error": "video content filtered"}), 200

    # 解析标题
    title = ""
    m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    if m:
        title = _strip_html_local(m.group(1))
    og_title = sources_module.get_meta_property_flexible(text, "og:title")
    if og_title and len(og_title.strip()) >= 8:
        title = _strip_html_local(og_title)

    # 解析发布时间
    release_time = (
        sources_module.get_meta_content_global(text, "property", "article:published_time")
        or sources_module.get_meta_content_global(text, "name", "pubdate")
        or sources_module.get_meta_content_global(text, "name", "publishdate")
        or ""
    )
    if not release_time:
        m = re.search(
            r"(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}(?:日)?(?:\s+\d{1,2}:\d{1,2}(?::\d{1,2})?)?)",
            text,
        )
        if m:
            release_time = m.group(1)
    release_time = release_time.replace("年", "-").replace("月", "-").replace("日", " ")
    release_time = release_time.replace("/", "-").strip()
    release_time = sources_module.coalesce_release_time_with_url(final_url, release_time)

    # 解析封面图（兼容 meta 属性顺序；协议相对 // 需补全）
    primary_img = ""
    og_img = sources_module.get_meta_property_flexible(text, "og:image")
    if og_img:
        primary_img = _normalize_media_url_local(og_img)
    if not primary_img:
        for im in re.finditer(r"<img\b[^>]*(?:/>|>)", text[:180000], re.I):
            u = cleaning_module.pick_best_image_url_from_img_tag(im.group(0))
            if u:
                primary_img = _normalize_media_url_local(u)
                break

    # 尝试定位正文主容器，避免把导航/版权/客户端下载等广告块拼进正文
    main_html = ""

    # chinanews.com.cn：使用“left_zw 起点 + 结束标记”切片，避免用正则匹配 </div> 被内部嵌套提前截断
    if is_chinanews:
        idx = text.find('class="left_zw"')
        if idx != -1:
            start = text.rfind("<div", 0, idx)
            if start == -1:
                start = max(idx - 50, 0)
            end_candidates = []
            for mk in ("<!--channel start-->", "<!--正文end-->", "<div class=\"clear\"></div>"):
                j = text.find(mk, idx)
                if j != -1:
                    end_candidates.append(j)
            end = min(end_candidates) if end_candidates else -1
            if end != -1 and end > start:
                main_html = text[start:end]
    main_patterns = [
        # chinanews.com.cn: prefer explicit body markers to avoid regex stopping at inner </div>
        r'(<!--[^>]*正文start[^>]*-->[\s\S]*?<!--[^>]*正文end[^>]*-->)',
        # people.com.cn
        r'(<div[^>]+class=["\'][^"\']*(?:rm_txt_con|article-content|content\s*txt|art_content)[^"\']*["\'][\s\S]*?</div>)',
        # common article containers
        r'(<div[^>]+class=["\'][^"\']*(?:content_area|content|cnt_bd|article-content)[^"\']*["\'][\s\S]*?</div>)',
        # sohu/netease/qq (generic)
        r'(<article[^>]*>[\s\S]*?</article>)',
    ]
    if not main_html:
        # 先按 class/id 锚点提取完整 div，避免正则在嵌套 div 场景下截断正文。
        anchor_patterns = [
            r'<div[^>]+class=["\'][^"\']*(?:content_area|article-content|cnt_bd|rm_txt_con|left_zw|content|detail|main-content|news_txt|trs_editor_view|rich_text|article-detail|artical|text_con|main_txt|article_wrapper)[^"\']*["\']',
            r'<div[^>]+id=["\'][^"\']*(?:content_area|content|detail|article|newsContent|articalContent|main)[^"\']*["\']',
        ]
        for rx in anchor_patterns:
            mm = re.search(rx, text, re.I)
            if mm:
                picked = sources_module.extract_balanced_div_from_index(text, mm.start())
                if picked and len(_strip_html_local(picked)) > 80:
                    main_html = picked
                    break
    if not main_html:
        for rx in main_patterns:
            mm = re.search(rx, text, re.I)
            if mm:
                main_html = mm.group(1)
                break
    if not main_html:
        main_html = text

    # 从正文段落组装 HTML（保留段内图片）
    main_html = cleaning_module.strip_html_comments(main_html)
    main_html = cleaning_module.strip_html_video_code_blocks(main_html)
    main_html = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", main_html, flags=re.I)
    main_html = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", main_html, flags=re.I)
    main_html = cleaning_module.rewrite_img_tags_in_html(main_html, final_url)
    combined_blocks = re.findall(
        r"(?:<p\b[^>]*>[\s\S]*?</p>|<figure\b[^>]*>[\s\S]*?</figure>)",
        main_html,
        re.I,
    )
    if not combined_blocks:
        combined_blocks = re.findall(
            r"<(?:p|div)\b[^>]*>[\s\S]*?<img\b[^>]*>[\s\S]*?</(?:p|div)>",
            main_html,
            re.I,
        )
    if combined_blocks:
        p_blocks = combined_blocks
    else:
        p_blocks = re.findall(r"<p[^>]*>(.*?)</p>", main_html, re.I | re.S)
    html_blocks = []
    images = []
    added_texts = set()
    stop_phrases = [
        "分享让更多人看到",
        "相关新闻",
        "推荐阅读",
        "责任编辑",
        "原标题",
        "声明",
        "免责声明",
        "版权",
        "Copyright",
        "ICP备",
        "客户端",
        "返回顶部",
        "关于人民网",
        "联系我们",
        "广告服务",
        "分享到",
        "字体：",
        "新闻频道 >",
        # 注意：勿用「来源：」——稿首来源行可能误触发截断，导致正文极短、拉取失败
    ]
    # 中国新闻网正文末尾常带“责任编辑/编辑”等信息；不应导致正文被提前截断
    if is_chinanews:
        stop_phrases = [ph for ph in stop_phrases if ph not in ("责任编辑", "客户端")]
    for p_html in p_blocks[:80]:
        imgs = []
        for src_m in re.finditer(r'<source[^>]+srcset=["\\\']([^"\\\']+)["\\\']', p_html, re.I):
            ss = src_m.group(1) or ""
            part = ss.split(",")[0].strip().split()[0].strip() if ss else ""
            if part:
                imgs.append(part)
        for img_m in re.finditer(r"<img\b[^>]*(?:/>|>)", p_html, re.I):
            u = cleaning_module.pick_best_image_url_from_img_tag(img_m.group(0))
            if u:
                imgs.append(u)

        imgs = [_normalize_media_url_local(u) for u in imgs if u]
        imgs = [u for u in imgs if u]
        for u in imgs:
            if u not in images:
                images.append(u)
        p_text = _strip_html_local(p_html)
        p_text = cleaning_module.strip_player_promo_noise(p_text)
        p_text = cleaning_module.strip_inline_media_captions(p_text)
        if not p_text and not imgs:
            continue
        # 跳过明显的代码/脚本/样式残留段落
        low = p_text.lower()
        if (
            "document." in low
            or "window." in low
            or "function(" in low
            or "var " in low
            or ("{" in p_text and "}" in p_text and ";" in p_text)
        ):
            continue
        # 遇到明显的页脚/导航/广告语就截断
        if any(ph in p_text for ph in stop_phrases):
            break
        img_tags = "".join([f'<p><img src="{u}" style="max-width:100%;height:auto;" referrerpolicy="no-referrer" /></p>' for u in imgs])
        if p_text:
            ck = _clean_text_local(p_text)
            # 站点常重复输出同一 <p>（如摘要区与正文区），或此前逻辑已收录同一段
            if len(ck) >= 12 and ck in added_texts:
                continue
            # keep paragraph formatting; p_text already normalized with newlines
            safe_text = p_text.replace("\n", "<br/>")
            html_blocks.append(img_tags + f"<p>{safe_text}</p>")
            added_texts.add(ck)
        else:
            html_blocks.append(img_tags)

    # 无 <p> 标签时的兜底
    if not html_blocks:
        # 用正文容器兜底而不是整页，避免导航/脚本污染
        plain = _strip_html_local(main_html)
        if plain:
            plain = cleaning_module.strip_player_promo_noise(plain)
            # 同样做一次页脚截断
            for ph in stop_phrases:
                idx = plain.find(ph)
                if idx != -1 and idx > 50:
                    plain = plain[:idx]
                    break
            html_blocks = [f"<p>{_clean_text_local(plain[:2000])}</p>"]

    body_html = "\n".join(html_blocks)
    # 兜底：若正文过短，尝试从全文提取段落，避免出现“新闻频道 > 国际新闻”这类导航文本。
    if len(_strip_html_local(body_html)) < 80:
        page_p_blocks = re.findall(r"<p[^>]*>(.*?)</p>", text, re.I | re.S)
        retry_blocks = []
        retry_seen = set()
        for p_html in page_p_blocks[:120]:
            p_text = _strip_html_local(p_html)
            p_text = cleaning_module.strip_player_promo_noise(p_text)
            if len(p_text) < 18:
                continue
            if any(ph in p_text for ph in stop_phrases):
                break
            ck = _clean_text_local(p_text)
            if len(ck) >= 18 and ck in retry_seen:
                continue
            retry_seen.add(ck)
            retry_blocks.append(f"<p>{p_text.replace(chr(10), '<br/>')}</p>")
        if retry_blocks:
            body_html = "\n".join(retry_blocks)
            body_html = cleaning_module.inject_images_before_body(
                body_html,
                cleaning_module.collect_content_image_urls(main_html, final_url, 25),
                max_n=10,
            )
    body_html = cleaning_module.strip_html_video_code_blocks(body_html or "")
    # 去掉重复的「阅读原文」提示段（含标准句与变体），再按需只保留一段
    body_html = re.sub(
        r"<p[^>]*>\s*" + re.escape(cleaning_module.VIDEO_READ_ORIGINAL_NOTICE) + r"\s*</p>\s*",
        "",
        body_html,
        flags=re.I,
    )
    body_html = re.sub(
        r"<p[^>]*>\s*观看详细视频请点击\s*[「""'『]?阅读原文[」""'』]?\s*跳转后查看。?\s*</p>\s*",
        "",
        body_html,
        flags=re.I,
    ).strip()
    plain_body = cleaning_module.strip_all_video_read_notices(_strip_html_local(body_html))
    if (
        cleaning_module.is_video_news_url(final_url)
        and cleaning_module.VIDEO_READ_ORIGINAL_NOTICE not in plain_body
    ):
        body_html = f"<p>{cleaning_module.VIDEO_READ_ORIGINAL_NOTICE}</p>\n" + body_html
    if primary_img and primary_img not in images:
        images.insert(0, primary_img)
    if primary_img and cleaning_module.is_generic_site_logo_or_brand_img_url(primary_img):
        chosen = ""
        for candidate in images:
            if candidate and not cleaning_module.is_generic_site_logo_or_brand_img_url(candidate):
                chosen = candidate
                break
        if chosen:
            primary_img = chosen
        else:
            for im in re.finditer(r"<img\b[^>]*(?:/>|>)", main_html[:200000], re.I):
                u = cleaning_module.pick_best_image_url_from_img_tag(im.group(0))
                if u:
                    u = _normalize_media_url_local(u)
                    if u and not cleaning_module.is_generic_site_logo_or_brand_img_url(u):
                        primary_img = u
                        break

    loose_imgs = cleaning_module.collect_content_image_urls(main_html, final_url, 40)
    for u in loose_imgs:
        if u and u not in images:
            images.append(u)
    if (not primary_img or cleaning_module.is_generic_site_logo_or_brand_img_url(primary_img)) and loose_imgs:
        for u in loose_imgs:
            if u and not cleaning_module.is_generic_site_logo_or_brand_img_url(u):
                primary_img = u
                break
    body_html = cleaning_module.inject_images_before_body(body_html, loose_imgs, max_n=12)

    return jsonify(
        {
            "ok": True,
            "url": url,
            "final_url": final_url,
            "title": title,
            "primary_img": primary_img,
            "release_time": release_time,
            "images": images[:30],
            "body_html": body_html,
        }
    )


@app.route('/spider', methods=['post', 'get'])
def fun():
    """
    核心抓取入口。参数：source=新闻源编码（tencent/people/xinhuanet/chinanews 等）。
    流程：拉取列表 → 补全详情 → 过滤/分类 → 去重入库 news_resources。
    """
    api_return = ''

    def md5_hex(s: str) -> str:
        return hashlib.md5(s.encode("utf-8")).hexdigest()

    def clean_text(s: str) -> str:
        if s is None:
            return ""
        s = html.unescape(str(s))
        s = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def clean_text_keep_lines(s: str) -> str:
        """
        Like clean_text(), but preserves newline structure.
        """
        if s is None:
            return ""
        s = html.unescape(str(s))
        s = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", s)
        s = s.replace("\r", "\n")
        out_lines = []
        for ln in s.split("\n"):
            ln = re.sub(r"\s+", " ", ln).strip()
            if ln:
                out_lines.append(ln)
        return "\n".join(out_lines).strip()

    def normalize_media_url(u: str, base_url: str = "") -> str:
        u = clean_text(u)
        if not u:
            return ""
        return cleaning_module.normalize_media_url_with_base(base_url or "", u)

    def clean_news_text(s: str) -> str:
        if not s:
            return ""
        text = strip_html(str(s))
        text = html.unescape(text)
        # 去广告/无关信息
        text = re.sub(r"(责任编辑[:：].*?$|原标题[:：].*?$|点击进入专题.*?$)", "", text, flags=re.M)
        text = re.sub(r"[^\w\u4e00-\u9fff，。！？；：、“”‘’（）《》【】—\-.,!?;:()%/\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return cleaning_module.strip_inline_media_captions(text)

    def strip_html_keep_lines(s: str) -> str:
        """
        Strip HTML while keeping line breaks roughly aligned with <p>/<br>.
        """
        if not s:
            return ""
        s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
        s = re.sub(r"</p\s*>", "\n", s, flags=re.I)
        s = re.sub(r"<p[^>]*>", "", s, flags=re.I)
        s = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", s, flags=re.I)
        s = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s, flags=re.I)
        s = re.sub(r"<[^>]+>", "", s)
        return clean_text_keep_lines(s)

    def clean_news_text_keep_lines(s: str) -> str:
        """
        Clean content but preserve paragraph/newline formatting.
        """
        if not s:
            return ""
        txt = strip_html_keep_lines(str(s))
        if not txt:
            return ""
        # remove common footer/ads per line
        drop_line = re.compile(r"(责任编辑[:：]|原标题[:：]|点击进入专题|免责声明|版权|Copyright|ICP备|返回顶部)", re.I)
        lines = []
        for ln in txt.split("\n"):
            if drop_line.search(ln):
                continue
            # filter abnormal chars but keep punctuation
            ln = re.sub(r"[^\w\u4e00-\u9fff，。！？；：、“”‘’（）《》【】—\-.,!?;:()%/\s]", " ", ln)
            ln = re.sub(r"\s+", " ", ln).strip()
            if ln:
                lines.append(ln)
        joined = "\n".join(lines).strip()
        joined = cleaning_module.strip_html_video_code_blocks(joined)
        joined = cleaning_module.strip_player_promo_noise(joined)
        joined = cleaning_module.dedupe_consecutive_lines(joined)
        return cleaning_module.strip_inline_media_captions(joined)

    def normalize_source_name(s: str, fallback: str = "") -> str:
        """将 origin 字段归一化为 news_source 表中的标准来源名。"""
        s = clean_text(s or fallback)
        if not s:
            return clean_text(fallback)
        canonical = {src["name"] for src in SPIDER_DEFAULT_SOURCES}
        if s in canonical:
            return s
        # 长键优先，避免短别名误匹配
        for k in sorted(SOURCE_NAME_MAP.keys(), key=len, reverse=True):
            if k in s:
                return SOURCE_NAME_MAP[k]
        return s

    def normalize_datetime_str(s: str) -> str:
        s = clean_text(s)
        if not s:
            return ""
        # 兼容 RSS 常见时间格式：Sat, 18 Apr 2026 10:28:34 GMT
        try:
            dt_rss = parsedate_to_datetime(s)
            if dt_rss is not None:
                return dt_rss.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
        s = s.replace("年", "-").replace("月", "-").replace("日", " ")
        s = s.replace("/", "-").replace("T", " ")
        s = re.sub(r"\.\d+Z?$", "", s)
        m = re.search(r"\d{4}-\d{1,2}-\d{1,2}(?:\s+\d{1,2}:\d{1,2}(?::\d{1,2})?)?", s)
        if m:
            candidate = m.group(0)
            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
                try:
                    dt = datetime.strptime(candidate, fmt)
                    if fmt == "%Y-%m-%d":
                        return dt.strftime("%Y-%m-%d 00:00:00")
                    if fmt == "%Y-%m-%d %H:%M":
                        return dt.strftime("%Y-%m-%d %H:%M:00")
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass
        return ""

    def parse_datetime_loose(s: str):
        s = clean_text(s)
        if not s:
            return None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                continue
        return None

    def is_fresh_release_time(release_time: str, max_age_days: int = MAX_NEWS_AGE_DAYS) -> bool:
        dt = parse_datetime_loose(release_time)
        if dt is None:
            return False
        now = datetime.now()
        # 异常未来时间（容忍 1 天）也过滤，避免脏数据
        if (dt - now).total_seconds() > 86400:
            return False
        age_days = (now - dt).total_seconds() / 86400.0
        return age_days <= float(max_age_days)

    def is_invalid_news_text(title: str, content: str) -> bool:
        title = clean_text(title)
        content = clean_text(content)
        if len(title) < 6 or len(content) < 12:
            return True
        bad_signs = ["404", "not found", "访问过于频繁", "验证码", "javascript", "cookie"]
        merged = (title + " " + content).lower()
        return any(b in merged for b in bad_signs)

    def is_low_quality_content(title: str, content: str, min_len: int = MIN_CONTENT_LEN_STRICT) -> bool:
        t = clean_text(title)
        c = clean_text(content)
        if not c:
            return True
        if len(c) < int(min_len):
            return True
        # 正文和标题完全一致，通常是详情提取失败后的兜底，不应入库为“完整新闻”
        if t and c == t:
            return True
        return False

    def is_video_news_row(row: dict) -> bool:
        """
        仅保留图文新闻：若 URL/视频字段/正文特征命中视频稿，则判定为视频新闻并过滤。
        """
        page_url = clean_text(row.get("url"))
        if cleaning_module.is_video_news_url(page_url):
            return True
        video_url = clean_text(row.get("video_url"))
        if video_url:
            return True
        content_text = clean_text_keep_lines(row.get("content"))
        # content_text 可能已被清洗成“保留换行的文本”，因此以关键字命中为主
        if re.search(
            r"begin:htmlVideoCode|htmlVideoCode|newPlayer|播放器|观看详细视频|mp4|m3u8|videoplayer|video_url|video/",
            content_text,
            re.I,
        ):
            return True
        return False

    def classify_category(title: str, content: str, url: str = "", origin: str = "") -> str:
        return classify_module.classify_news_category(title or "", content or "", url or "", origin or "")

    def extract_keywords(title: str, content: str, topn: int = 6):
        text = clean_news_text(f"{title} {content}")
        tokens = re.findall(r"[\u4e00-\u9fff]{2,6}|[A-Za-z]{3,20}", text)
        # 标签提取保留较短停用表，避免与分类长停用表一致导致标签全被滤空
        stop_words = {
            "我们",
            "你们",
            "他们",
            "这个",
            "那个",
            "进行",
            "有关",
            "表示",
            "记者",
            "新闻",
            "中国",
            "一个",
            "可以",
            "没有",
            "这样",
            "什么",
            "如何",
            "怎么",
            "目前",
            "相关",
        }
        freq = {}
        for t in tokens:
            if t in stop_words:
                continue
            freq[t] = freq.get(t, 0) + 1
        ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [k for k, _ in ranked[:topn]]

    def generate_summary(content: str, n: int = 120) -> str:
        txt = clean_news_text(content)
        if len(txt) <= n:
            return txt
        return txt[:n] + "..."

    def strip_html(s: str) -> str:
        if not s:
            return ""
        s = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", s, flags=re.I)
        s = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s, flags=re.I)
        s = re.sub(r"<[^>]+>", "", s)
        return re.sub(r"\s+", " ", s).strip()

    def get_meta_content(html_text: str, attr_name: str, attr_value: str):
        # support: <meta name="xxx" content="..."> / <meta property="xxx" content="...">
        rx = re.compile(
            rf'<meta[^>]+{attr_name}=["\']{re.escape(attr_value)}["\'][^>]*content=["\']([^"\']+)["\']',
            re.I,
        )
        m = rx.search(html_text)
        return m.group(1).strip() if m else ""

    def extract_article_detail(url: str):
        """
        Fetch article detail page and extract missing fields as best effort.
        """
        try:
            resp = requests.get(
                url,
                headers=sources_module.build_article_fetch_headers(url),
                timeout=28,
                allow_redirects=True,
            )
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding or "utf-8"
            text = cleaning_module.strip_html_comments(resp.text or "")
            text = cleaning_module.strip_html_video_code_blocks(text)
            if not text.strip():
                return {}
        except Exception:
            return {}

        # 解析标题（兼容 og:title）
        title = sources_module.get_meta_property_flexible(text, "og:title")
        if not title:
            m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
            if m:
                title = strip_html(m.group(1))

        # publish time
        release_time = (
            get_meta_content(text, "property", "article:published_time")
            or get_meta_content(text, "name", "pubdate")
            or ""
        )
        if not release_time:
            head_m = re.search(r"<head[^>]*>([\s\S]*?)</head>", text, re.I)
            head = head_m.group(1) if head_m else text[:12000]
            m = re.search(
                r"(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{1,2}(:\d{1,2})?)",
                head,
            )
            if m:
                release_time = m.group(1)
        release_time = sources_module.coalesce_release_time_with_url(url, release_time)

        # source
        source = get_meta_content(text, "name", "source") or get_meta_content(
            text, "property", "article:author"
        )

        # content: prefer article body container -> paragraphs
        content_html = text
        try:
            host = (urlparse(url).netloc or "").lower()
        except Exception:
            host = ""

        def pick_main_container(html_text: str, page_url: str, page_host: str) -> str:
            if not html_text:
                return ""
            # chinanews: slice from left_zw to end markers to avoid nested div truncation
            if "chinanews.com.cn" in page_host:
                idx = html_text.find('class="left_zw"')
                if idx != -1:
                    start = html_text.rfind("<div", 0, idx)
                    if start == -1:
                        start = max(idx - 50, 0)
                    end_candidates = []
                    for mk in ("<!--channel start-->", "<!--正文end-->", "<div class=\"clear\"></div>"):
                        j = html_text.find(mk, idx)
                        if j != -1:
                            end_candidates.append(j)
                    end = min(end_candidates) if end_candidates else -1
                    if end != -1 and end > start:
                        return html_text[start:end]

            # 优先按锚点提取完整 div，避免 regex 在嵌套 div 下截断正文
            anchor_patterns = [
                r'<div[^>]+class=["\'][^"\']*(?:content_area|article-content|cnt_bd|rm_txt_con|left_zw|content|detail|main-content|xl_content|con|news_txt|trs_editor_view|rich_text|article-detail|artical)[^"\']*["\']',
                r'<div[^>]+id=["\'][^"\']*(?:content_area|content|detail|article|p-detail|newsContent|articalContent)[^"\']*["\']',
            ]
            for rx in anchor_patterns:
                mm = re.search(rx, html_text, re.I)
                if mm:
                    picked = sources_module.extract_balanced_div_from_index(html_text, mm.start())
                    if picked and len(strip_html_keep_lines(picked)) > 100:
                        return picked

            patterns = [
                # people.com.cn
                r'(<div[^>]+class=["\'][^"\']*(?:rm_txt_con|article-content|content\s*txt|art_content)[^"\']*["\'][\s\S]*?</div>)',
                # common article containers
                r'(<div[^>]+class=["\'][^"\']*(?:content_area|content|cnt_bd|article-content)[^"\']*["\'][\s\S]*?</div>)',
                # xinhuanet.com common containers
                r'(<div[^>]+id=["\']?(?:detail|content|p-detail|article)[^"\']*["\']?[\s\S]*?</div>)',
                r'(<div[^>]+class=["\'][^"\']*(?:detail|content|article|main-content|xl_content|con|cnt)[^"\']*["\'][\s\S]*?</div>)',
                # generic article tag
                r'(<article[^>]*>[\s\S]*?</article>)',
            ]
            for rx in patterns:
                m = re.search(rx, html_text, re.I)
                if m:
                    return m.group(1)
            return html_text

        content_html = pick_main_container(text, url, host)

        def extract_paragraph_texts(html_text: str, max_blocks: int = 150):
            blocks = re.findall(r"<p[^>]*>(.*?)</p>", html_text or "", re.I | re.S)
            out = []
            seen_fp = set()
            for b in blocks:
                t = strip_html_keep_lines(b)
                if len(clean_text(t)) < 10:
                    continue
                if len(t) >= 18:
                    fp = cleaning_module.paragraph_fingerprint(t)
                    if fp in seen_fp:
                        continue
                    seen_fp.add(fp)
                out.append(t)
                if len(out) >= max_blocks:
                    break
            return out

        paragraph_texts = extract_paragraph_texts(content_html, max_blocks=150)
        content = "\n\n".join(paragraph_texts).strip()
        content = cleaning_module.dedupe_paragraph_body(content, min_len=20)

        # Some sites mix plain text nodes outside <p>; supplement from stripped lines.
        if (not content) or (len(clean_text(content)) < 500):
            plain = strip_html_keep_lines(content_html)
            # truncate extremely long pages
            if len(plain) > 40000:
                plain = plain[:40000]
            # merge: append lines not already present
            if plain:
                merged = []
                seen = set()
                for ln in plain.split("\n"):
                    key = clean_text(ln)
                    if len(key) < 8:
                        continue
                    if key in seen:
                        continue
                    seen.add(key)
                    merged.append(ln.strip())
                if merged:
                    content = "\n".join(merged).strip()
                    content = cleaning_module.dedupe_paragraph_body(content, min_len=20)

        # If container-matched content is still too short, fallback to full-page paragraph extraction.
        # This avoids site-specific container mismatch causing severe truncation.
        if len(clean_text(content)) < 500:
            all_page_paragraphs = extract_paragraph_texts(text, max_blocks=220)
            if all_page_paragraphs:
                # keep the longer one
                candidate = "\n\n".join(all_page_paragraphs).strip()
                candidate = cleaning_module.dedupe_paragraph_body(candidate, min_len=20)
                if len(clean_text(candidate)) > len(clean_text(content)):
                    content = candidate

        content = cleaning_module.dedupe_paragraph_body(content, min_len=20)

        if content:
            content = "\n\n".join(
                cleaning_module.strip_inline_media_captions(p.strip())
                for p in content.split("\n\n")
                if p.strip()
            )
        content = cleaning_module.strip_player_promo_noise(content)
        content = cleaning_module.ensure_video_read_notice_once_plain(content, url)
        content = cleaning_module.strip_all_image_markup(content)

        video_url = sources_module.extract_video_url_from_html(text, url)

        return {
            "title": clean_text(title),
            "img": "",
            "release_time": clean_text(release_time),
            "origin": clean_text(source),
            "content": clean_text_keep_lines(content),
            "video_url": clean_text(video_url),
        }

    def parse_first_img(html: str, base_url: str = "") -> str:
        """爬虫不再解析 RSS/正文中的封面图，固定返回空。"""
        return ""

    def sanitize_rss_xml(xml_text: str) -> str:
        text = xml_text or ""
        if not text:
            return ""
        # Strip illegal XML control chars but keep tab/newline/carriage return.
        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)
        # Some feeds contain naked '&' inside text nodes.
        text = re.sub(r"&(?!#?\w+;)", "&amp;", text)
        return text

    def parse_rss_items_loose(xml_text: str):
        items = []
        text = xml_text or ""
        for block in re.findall(r"<item\b[\s\S]*?</item>", text, flags=re.I):
            def _pick(tag):
                m = re.search(rf"<{tag}\b[^>]*>([\s\S]*?)</{tag}>", block, flags=re.I)
                return html.unescape((m.group(1) if m else "").strip())

            title = _pick("title")
            link = _pick("link")
            pub = _pick("pubDate")
            desc = _pick("description")
            if not link or not title:
                continue
            release_time = pub
            try:
                if pub:
                    dt = parsedate_to_datetime(pub)
                    release_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
            items.append(
                {
                    "title": title,
                    "url": link,
                    "img": "",
                    "release_time": release_time,
                    "content": strip_html(desc),
                }
            )
        return items

    def parse_rss_items(xml_text: str):
        """
        Parse RSS/Atom minimal fields from xml.
        Returns list of dicts with: title, url, img（固定为空）, release_time, content
        """
        items = []
        xml_text = sanitize_rss_xml(xml_text)
        try:
            root = ET.fromstring(xml_text)
        except Exception:
            loose_items = parse_rss_items_loose(xml_text)
            if loose_items:
                return loose_items
            raise

        # RSS: <rss><channel><item>...
        channel = root.find("channel")
        if channel is not None:
            for it in channel.findall("item"):
                title = (it.findtext("title") or "").strip()
                link = (it.findtext("link") or "").strip()
                pub = (it.findtext("pubDate") or "").strip()
                desc = (it.findtext("description") or "").strip()

                release_time = pub
                try:
                    if pub:
                        dt = parsedate_to_datetime(pub)
                        release_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass

                items.append(
                    {
                        "title": title,
                        "url": link,
                        "img": "",
                        "release_time": release_time,
                        "content": strip_html(desc),
                    }
                )
            return items

        # Atom: <feed><entry>...
        # namespaces are common; match by suffix
        def find_text_any(elem, tag_suffix):
            for child in list(elem):
                if child.tag.endswith(tag_suffix):
                    return (child.text or "").strip()
            return ""

        for entry in root.findall(".//"):
            if not entry.tag.endswith("entry"):
                continue
            title = find_text_any(entry, "title")
            link = ""
            for child in list(entry):
                if child.tag.endswith("link"):
                    href = child.attrib.get("href")
                    if href:
                        link = href
                        break
            updated = find_text_any(entry, "updated") or find_text_any(entry, "published")
            summary = find_text_any(entry, "summary")
            content = find_text_any(entry, "content") or summary
            items.append(
                {
                    "title": title,
                    "url": link,
                    "img": "",
                    "release_time": updated,
                    "content": strip_html(content),
                }
            )
        return items

    # 读取 config 文件
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(parent_dir, './config/config.ini'), encoding="utf-8")
    db_settings = _load_db_settings() or {}

    user = db_settings.get("user", "")
    password = db_settings.get("password", "")
    host = db_settings.get("host", "")
    port = db_settings.get("port", "")
    database = db_settings.get("database", "")
    table_name = db_settings.get("table_name", "news_resources")

    # 选择新闻源与解析器
    source = request.args.get("source", default="tencent")
    source = (source or "tencent").strip().lower()
    source_cfg = _get_source_config(source) or {"code": source, "name": source}
    parser_name = (source_cfg.get("parser_name") or source_cfg.get("code") or source).strip().lower()
    source_extra = _safe_json_loads(source_cfg.get("extra_json"))
    ignore_disabled = bool(int(request.args.get("ignore_disabled", 0) or 0))
    if source_cfg.get("enabled") is False and not ignore_disabled:
        return jsonify({"ok": False, "error": "source disabled"}), 400
    # 强制最近几天规则：忽略前端传参，统一使用当前版本固定值
    max_age_days = MAX_NEWS_AGE_DAYS

    # 爬取前清库：删除超期/视频/正文过短数据
    engine = _get_db_engine()
    if engine is not None:
        _purge_invalid_news_rows(engine, table_name, max_age_days)

    size=CRAWL_LIMIT

    output_csv=config.getboolean('option','output_csv')
    write_database=config.getboolean('option','write_database')
    run_stats = {
        "fetched_count": 0,
        "qualified_count": 0,
        "written_count": 0,
        "dropped_count": 0,
        "duplicate_count": 0,
        "summary": "",
        "error_message": "",
    }

    def build_visible_summary():
        return (
            f"近{max_age_days}天；抓取{int(run_stats.get('fetched_count') or 0)}条；"
            f"保留{int(run_stats.get('qualified_count') or 0)}条；"
            f"入库{int(run_stats.get('written_count') or 0)}条；"
            f"过滤{int(run_stats.get('dropped_count') or 0)}条；"
            f"重复跳过{int(run_stats.get('duplicate_count') or 0)}条"
        )

    def is_non_article_index_url(link: str) -> bool:
        """栏目/专题索引页，非单篇新闻；抓取后常出现久远日期或无效正文。"""
        u = (link or "").strip()
        if not u:
            return True
        low = u.lower()
        parsed = urlparse(u)
        path = (parsed.path or "").lower()
        # 人民网：/GB/8/22/index.html、「记者遍全球」等聚合页
        if "people.com.cn" in low or "people.cn" in low:
            if re.search(r"/gb/\d+/\d+/index\.html", path):
                return True
            if re.search(r"/rmhw/index\.html$", path) or "记者遍全球" in u:
                return True
        # 纯频道首页
        if re.search(r"/(channel|list|catalog)/[^/]+/index\.html$", path):
            return True
        return False

    def json_spider_result(ok: bool, http_code: int = 200):
        """供管理端 fmt=json 展示「抓取 / 保留 / 入库」。"""
        payload = {
            "ok": ok,
            "fetched": int(run_stats.get("fetched_count") or 0),
            "kept": int(run_stats.get("qualified_count") or 0),
            "inserted": int(run_stats.get("written_count") or 0),
            "dropped": int(run_stats.get("dropped_count") or 0),
            "duplicate_skipped": int(run_stats.get("duplicate_count") or 0),
            "summary": (run_stats.get("summary") or "").strip(),
            "error": (run_stats.get("error_message") or "").strip(),
        }
        return jsonify(payload), http_code

    def write_to_db_df(df: pd.DataFrame, origin_name: str):
        """
        Normalize columns to match `news_resources` table and write to MySQL.
        Uses `unique_id` for de-duplication.
        """
        nonlocal api_return

        if df is None or df.empty:
            run_stats["qualified_count"] = 0
            run_stats["summary"] = "no data"
            return "no data"

        df = df.copy()
        # 打乱候选顺序，避免每次爬取总是同一批链接排在队首；配合库内去重后更易每次入库不同稿件
        if len(df) > 1:
            rs = int(time.time() * 1000) % (2**31 - 1)
            df = df.sample(frac=1.0, random_state=rs).reset_index(drop=True)
        df = df.head(RAW_FETCH_LIMIT)
        run_stats["fetched_count"] = int(len(df))
        df["origin"] = normalize_source_name(origin_name, origin_name)

        # fill required columns
        for col in [
            "title",
            "url",
            "img",
            "read_num",
            "origin",
            "release_time",
            "content",
            "comment_num",
            "comment",
            "video_url",
            "unique_id",
            "extra",
        ]:
            if col not in df.columns:
                df[col] = ""

        # 丢弃空行，并按规范化 URL 生成 unique_id（多源合并、http/https、尾斜杠等同源只保留一条）
        df["url"] = df["url"].astype(str).str.strip()
        df = df[(df["url"].str.len() > 0) & (df["title"].astype(str).str.len() > 0)]
        df["_url_norm"] = df["url"].map(storage_module.normalize_news_url)
        df = df[df["_url_norm"].str.len() > 0]
        df["unique_id"] = df["_url_norm"].map(md5_hex)
        df = df.drop_duplicates(subset=["unique_id"], keep="first")
        df = df.drop(columns=["_url_norm"])
        df = df[~df["url"].astype(str).map(is_non_article_index_url)]
        if df.empty:
            run_stats["fetched_count"] = 0
            run_stats["qualified_count"] = 0
            run_stats["summary"] = "no rows after filtering channel/index urls"
            return "no rows after filtering channel/index urls"

        # Enrich each row via detail page if key fields are missing.
        records = df.to_dict("records")
        enriched = []
        dropped = 0
        seen_fingerprints = set()
        for row in records:
            row["origin"] = normalize_source_name(row.get("origin"), origin_name)
            row["title"] = clean_news_text(row.get("title"))
            row["url"] = clean_text(row.get("url"))
            base_u = row.get("url") or ""
            row["img"] = ""
            row["release_time"] = normalize_datetime_str(
                sources_module.coalesce_release_time_with_url(
                    row.get("url") or "",
                    str(row.get("release_time") or ""),
                )
            )
            row["content"] = clean_news_text_keep_lines(row.get("content"))
            row["comment_num"] = ""
            row["comment"] = ""
            row["video_url"] = clean_text(row.get("video_url"))

            # 腾讯新闻 API/列表常给摘要；当内容过短也强制抓详情页补全正文
            content_too_short = len(clean_text(row.get("content"))) < 200
            missing_before = [
                k for k in ["release_time", "content", "video_url"] if not row.get(k)
            ]
            if missing_before or content_too_short:
                release_before_detail = clean_text(row.get("release_time"))
                detail = extract_article_detail(row["url"])
                # 详情页字段合并策略：
                # - 缺失字段直接补
                # - 标题/正文过短时，用详情页更长内容覆盖（而不是仅在空值时补）
                for k in ["title", "release_time", "origin", "video_url"]:
                    if not row.get(k) and detail.get(k):
                        row[k] = detail[k]
                detail_title = clean_news_text(detail.get("title"))
                if detail_title and (not row.get("title") or len(clean_text(row.get("title"))) < 8):
                    row["title"] = detail_title
                detail_content = clean_news_text_keep_lines(detail.get("content"))
                cur_content = clean_news_text_keep_lines(row.get("content"))
                if detail_content and (
                    len(clean_text(cur_content)) < MIN_CONTENT_LEN_STRICT
                    or len(clean_text(detail_content)) > len(clean_text(cur_content))
                ):
                    row["content"] = detail_content
                # 发布时间优先采用详情页提取结果，保证“源发布时间”准确。
                detail_release_time = normalize_datetime_str(detail.get("release_time"))
                if detail_release_time:
                    row["release_time"] = detail_release_time
                elif (
                    detail_content
                    and len(clean_text(detail_content)) >= MIN_CONTENT_LEN_STRICT
                    and not release_before_detail
                ):
                    # 列表页未给时间、详情有正文但解析不到发布时间：不通过近 N 天校验（避免误用伪造时间）
                    row["release_time"] = ""

            # 二次清洗 + 规范化（再次用 URL 纠偏 RSS/详情时间）
            row["origin"] = normalize_source_name(row.get("origin"), origin_name)
            row["title"] = clean_news_text(row.get("title"))
            row["content"] = clean_news_text_keep_lines(row.get("content"))
            row["img"] = ""
            row["release_time"] = normalize_datetime_str(
                sources_module.coalesce_release_time_with_url(
                    row.get("url") or "",
                    str(row.get("release_time") or ""),
                )
            )
            row["comment_num"] = ""
            row["comment"] = ""
            row["video_url"] = clean_text(row.get("video_url"))
            row["content"] = cleaning_module.strip_all_video_read_notices(
                row.get("content") or ""
            )
            row["content"] = cleaning_module.strip_all_image_markup(row.get("content") or "")

            if is_invalid_news_text(row["title"], row["content"]):
                dropped += 1
                continue
            if is_video_news_row(row):
                dropped += 1
                continue
            if is_low_quality_content(row["title"], row["content"], min_len=MIN_CONTENT_LEN_STRICT):
                dropped += 1
                continue
            # 仅保留近期新闻，避免抓取发布时间过久远的历史稿件。
            if not is_fresh_release_time(row["release_time"], max_age_days=max_age_days):
                dropped += 1
                continue

            category = classify_category(
                row["title"],
                row["content"],
                row.get("url") or "",
                row.get("origin") or "",
            )
            kws = extract_keywords(row["title"], row["content"], topn=6)
            summary = generate_summary(row["content"], n=120)

            extra_obj = {
                "category": category,
                "tags": kws,
                "summary": summary,
                "video_url": clean_text(row.get("video_url")),
            }
            row["extra"] = json.dumps(extra_obj, ensure_ascii=False)

            # 站内去重（同URL + 高相似文本）
            fingerprint_base = clean_news_text((row["title"] + " " + summary).lower())
            if not fingerprint_base:
                dropped += 1
                continue
            fingerprint = md5_hex(fingerprint_base)
            if fingerprint in seen_fingerprints:
                dropped += 1
                continue
            seen_fingerprints.add(fingerprint)

            # 完整性校验（关键字段必须齐全）
            if any(not clean_text(row.get(k)) for k in REQUIRED_NEWS_FIELDS):
                dropped += 1
                continue
            row["unique_id"] = md5_hex(storage_module.normalize_news_url(row.get("url") or ""))
            enriched.append(row)

        if dropped:
            print(f"[FILTER] dropped incomplete news: {dropped}")
        run_stats["dropped_count"] = int(dropped)

        # 兜底策略：有效数据尽量多，但若严格清洗后不足 MIN_VALID_NEWS_FALLBACK 条，则放宽过滤。
        if len(enriched) < MIN_VALID_NEWS_FALLBACK:
            relaxed = []
            have_norm = {
                storage_module.normalize_news_url(r.get("url") or "")
                for r in enriched
                if storage_module.normalize_news_url(r.get("url") or "")
            }
            for row in records:
                row = dict(row)
                row["origin"] = normalize_source_name(row.get("origin"), origin_name)
                row["title"] = clean_news_text(row.get("title"))
                row["url"] = clean_text(row.get("url"))
                if not row["title"] or not row["url"]:
                    continue
                nu = storage_module.normalize_news_url(row["url"])
                if not nu:
                    continue
                if nu in have_norm:
                    continue
                row["img"] = ""
                row["release_time"] = normalize_datetime_str(
                    sources_module.coalesce_release_time_with_url(
                        row.get("url") or "",
                        str(row.get("release_time") or ""),
                    )
                )
                row["content"] = clean_news_text_keep_lines(row.get("content"))
                row["comment_num"] = ""
                row["comment"] = ""
                row["video_url"] = clean_text(row.get("video_url"))
                row["content"] = cleaning_module.strip_all_video_read_notices(
                    row.get("content") or ""
                )
                row["content"] = cleaning_module.strip_all_image_markup(row.get("content") or "")
                if is_video_news_row(row):
                    continue
                if is_low_quality_content(row["title"], row["content"], min_len=MIN_CONTENT_LEN_RELAXED):
                    continue
                if not is_fresh_release_time(row["release_time"], max_age_days=max_age_days):
                    continue

                category = classify_category(
                    row["title"],
                    row["content"],
                    row.get("url") or "",
                    row.get("origin") or "",
                )
                kws = extract_keywords(row["title"], row["content"], topn=6)
                summary = generate_summary(row["content"], n=120)
                row["extra"] = json.dumps(
                    {
                        "category": category,
                        "tags": kws,
                        "summary": summary,
                        "video_url": clean_text(row.get("video_url")),
                    },
                    ensure_ascii=False,
                )

                if any(not clean_text(row.get(k)) for k in REQUIRED_NEWS_FIELDS):
                    continue
                row["unique_id"] = md5_hex(storage_module.normalize_news_url(row.get("url") or ""))
                relaxed.append(row)
                if nu:
                    have_norm.add(nu)
                if len(relaxed) >= RAW_FETCH_LIMIT:
                    break
            # 合并并再截取
            enriched = (enriched + relaxed)[:RAW_FETCH_LIMIT]
            if len(enriched) < MIN_VALID_NEWS_FALLBACK:
                run_stats["qualified_count"] = len(enriched)
                run_stats["summary"] = f"no enough valid data (<{MIN_VALID_NEWS_FALLBACK}), valid_count={len(enriched)}"
                return f"no enough valid data (<{MIN_VALID_NEWS_FALLBACK})"

        run_stats["qualified_count"] = len(enriched)
        if not enriched:
            run_stats["summary"] = "no complete data"
            return "no complete data"
        df = pd.DataFrame(enriched)

        engine = create_engine(
            "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                user, password, host, port, database
            )
        )
        try:
            db_columns = (
                pd.read_sql(f"SHOW COLUMNS FROM {table_name}", engine)["Field"]
                .astype(str)
                .tolist()
            )
        except Exception:
            db_columns = list(df.columns)

        df["unique_id"] = df["url"].astype(str).map(lambda u: md5_hex(storage_module.normalize_news_url(str(u))))
        df = df.drop_duplicates(subset=["unique_id"], keep="first")

        # 与历史库按 unique_id 去重：已存在的稿件不再插入（避免重复爬取产生重复行）
        id_list = [str(x).strip() for x in df["unique_id"].tolist() if str(x).strip()]
        existing_ids: set = set()
        for i in range(0, len(id_list), 400):
            chunk = id_list[i : i + 400]
            if not chunk:
                continue
            ph = ",".join(["%s"] * len(chunk))
            try:
                q = f"SELECT unique_id FROM `{table_name}` WHERE unique_id IN ({ph})"
                sub = pd.read_sql(q, engine, params=chunk)
                for v in sub["unique_id"].astype(str).tolist():
                    existing_ids.add(str(v).strip())
            except Exception as ex:
                print(f"[DB] duplicate lookup failed: {ex}")
        before_rows = len(df)
        df = df[~df["unique_id"].astype(str).isin(existing_ids)]
        skipped_db = before_rows - len(df)
        run_stats["duplicate_count"] = int(skipped_db)
        if skipped_db:
            print(f"[DB] skip {skipped_db} rows already in database (unique_id)")
        # 关键修正：先和历史库去重，再截取写入上限。
        # 否则会出现“前50条全是历史重复，导致本次无新增”的假象，
        # 扩大 max_age_days 时尤其明显（更早新闻常排在后面被提前截断）。
        df = df.head(CRAWL_LIMIT)
        if df.empty:
            run_stats["summary"] = "no new data (all duplicates in database or filtered empty)"
            return "no new data (all duplicates in database or filtered empty)"

        # write csv
        if output_csv:
            out_path = f"./result_{source}.csv"
            if os.path.exists(out_path):
                df.to_csv(out_path, header=False, index=False, encoding="utf-8", mode="a")
            else:
                df.to_csv(out_path, header=True, index=False, encoding="utf-8")
            api_return = (api_return + "   " if api_return else "") + "write csv success!"

        # write database
        if write_database:
            try:
                # 仅写入数据库表中已存在的列，避免因字段不一致导致整批失败
                write_cols = [c for c in df.columns if c in db_columns]
                if "unique_id" in db_columns and "unique_id" not in write_cols:
                    write_cols.append("unique_id")
                if not write_cols:
                    run_stats["summary"] = "no writable columns"
                    return "no writable columns"

                # 为降低锁冲突，分批写入并对锁超时做自动重试
                write_df = df[write_cols]
                chunk_size = 20
                for start in range(0, len(write_df), chunk_size):
                    part = write_df.iloc[start:start + chunk_size]
                    ok = False
                    for attempt in range(4):
                        try:
                            pd.io.sql.to_sql(part, table_name, engine, if_exists="append", index=False)
                            ok = True
                            break
                        except Exception as e:
                            err_msg = str(e).lower()
                            retryable = (
                                "lock wait timeout exceeded" in err_msg
                                or "deadlock found" in err_msg
                                or "(1205" in err_msg
                                or "(1213" in err_msg
                            )
                            if retryable and attempt < 3:
                                time.sleep(0.35 * (attempt + 1))
                                continue
                            raise
                    if not ok:
                        raise RuntimeError("database write failed after retries")
                api_return = (api_return + "   " if api_return else "") + "write database success!"
                run_stats["written_count"] = int(len(df))
            except Exception as e:
                print(f"错误信息: {e}")
                api_return = (api_return + "   " if api_return else "") + "write database fail!"
                run_stats["error_message"] = str(e)

        run_stats["summary"] = f"{build_visible_summary()}   {api_return or 'ok'}"
        return run_stats["summary"]

    def crawl_rss(feed_url: str, origin_name: str, return_df_only: bool = False):
        resp = requests.get(
            feed_url,
            headers={
                "user-agent": "Mozilla/5.0",
                "accept": "application/xml,text/xml,*/*",
            },
            timeout=15,
            allow_redirects=True,
        )
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        text = (resp.text or "").strip()
        if not text:
            raise ValueError("empty rss response")
        if not text.startswith("<"):
            # 通常是被站点重定向到非 XML 页
            raise ValueError("non-xml response")
        try:
            items = parse_rss_items(text)
        except Exception:
            items = parse_rss_items_loose(sanitize_rss_xml(text))
            if not items:
                raise
        df = pd.DataFrame(items)
        if return_df_only:
            return df
        return write_to_db_df(df, origin_name)

    def crawl_rss_with_fallback(
        feed_urls,
        origin_name: str,
        return_df_only: bool = False,
        ignore_env_proxy: bool = False,
    ):
        last_err = ""
        merged = []
        safe_origin_name = (origin_name or "").encode("unicode_escape").decode("ascii")
        for feed_url in feed_urls:
            try:
                print(f"[SOURCE] {safe_origin_name} trying: {feed_url}")
                rss_headers = {"user-agent": "Mozilla/5.0", "accept": "application/xml,text/xml,*/*"}
                if ignore_env_proxy:
                    resp = _http_get_ignore_proxy(
                        feed_url,
                        headers=rss_headers,
                        timeout=15,
                        allow_redirects=True,
                    )
                else:
                    resp = requests.get(
                        feed_url,
                        headers=rss_headers,
                        timeout=15,
                        allow_redirects=True,
                    )
                resp.raise_for_status()
                resp.encoding = resp.apparent_encoding or "utf-8"
                text = (resp.text or "").strip()
                if not text or not text.startswith("<"):
                    raise ValueError("non-xml response")
                try:
                    items = parse_rss_items(text)
                except Exception:
                    items = parse_rss_items_loose(sanitize_rss_xml(text))
                    if not items:
                        raise
                merged.extend(items)
                if len(merged) >= RAW_FETCH_LIMIT:
                    break
            except Exception as e:
                last_err = str(e)
                print(f"[SOURCE] {safe_origin_name} failed: {feed_url} -> {last_err}")
                continue
        if not merged:
            raise ValueError(f"{origin_name} rss all failed: {last_err}")
        merged_df = pd.DataFrame(merged)
        if return_df_only:
            return merged_df
        return write_to_db_df(merged_df, origin_name)

    def crawl_tencent_web(limit=RAW_FETCH_LIMIT, return_df_only: bool = False):
        """
        Tencent fallback crawler (HTML-based).
        Used when RSS endpoints are unavailable.
        """
        url = "https://news.qq.com"
        tencent_headers = dict(sources_module.build_article_fetch_headers(url))
        resp = _http_get_ignore_proxy(
            url,
            headers=tencent_headers,
            timeout=15,
            allow_redirects=True,
        )
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        text = resp.text or ""
        if not text.strip():
            raise ValueError("tencent homepage empty")

        # Extract anchor links and titles.
        pattern = re.compile(
            r"<a[^>]+href=[\"'](https?://[^\"']+)[\"'][^>]*>(.*?)</a>",
            re.I | re.S,
        )
        items = []
        seen = set()
        for link, title_html in pattern.findall(text):
            if "qq.com" not in link:
                continue
            title = re.sub(r"<[^>]+>", "", title_html)
            title = html.unescape(re.sub(r"\s+", " ", title)).strip()
            if len(title) < 8:
                continue
            if link in seen:
                continue
            seen.add(link)
            items.append(
                {
                    "title": title,
                    "url": link,
                    "img": "",
                    "read_num": "",
                    "origin": "腾讯新闻",
                    "release_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "content": "",
                    "comment_num": "",
                    "comment": "",
                    "unique_id": md5_hex(link),
                }
            )
            if len(items) >= limit:
                break

        if not items:
            raise ValueError("tencent homepage parse empty")

        print(f"[SOURCE] 腾讯新闻 html fallback items: {len(items)}")
        out_df = pd.DataFrame(items)
        if return_df_only:
            return out_df
        return write_to_db_df(out_df, "腾讯新闻")

    def crawl_site_links(
        base_url: str,
        host_keywords,
        origin_name: str,
        limit=RAW_FETCH_LIMIT,
        return_df_only: bool = False,
        people_strict_n1: bool = False,
        max_pages: int = 12,
    ):
        """
        Generic homepage link crawler for news sites.
        people_strict_n1: 仅保留人民网 /n1/年/MMDD/ 形态正文链接（默认关闭，与新华社同源首页策略一致）。
        """
        def is_probable_article_url(link: str) -> bool:
            link = (link or "").strip()
            if not link:
                return False
            if is_non_article_index_url(link):
                return False
            low = link.lower()
            # 排除明显非详情页
            if any(x in low for x in ["javascript:", "mailto:", "/search.", "search.php", "/video/index", "/live", "/special"]):
                return False
            if people_strict_n1 and ("people.com.cn" in low or "people.cn" in low):
                if not re.search(r"/n1/\d{4}/\d{4}/", link, re.I):
                    return False
            return bool(re.search(r"\.(shtml|html)(\?|#|$)", link, re.I))

        pattern = re.compile(r"<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.I | re.S)
        page_queue = [base_url]
        visited_page = set()
        section_candidates = []
        items = []
        seen = set()
        mp = max(3, int(max_pages or 12))

        while page_queue and len(visited_page) < mp and len(items) < limit:
            cur_page = page_queue.pop(0)
            if cur_page in visited_page:
                continue
            visited_page.add(cur_page)
            try:
                resp = requests.get(
                    cur_page,
                    headers=sources_module.build_article_fetch_headers(cur_page),
                    timeout=15,
                    allow_redirects=True,
                )
                resp.raise_for_status()
                resp.encoding = resp.apparent_encoding or "utf-8"
                text = resp.text or ""
            except Exception:
                continue
            if not text.strip():
                continue

            for href, title_html in pattern.findall(text):
                href = (href or "").strip()
                if not href or href.startswith("#") or href.lower().startswith("javascript:"):
                    continue
                link = urljoin(cur_page, href)
                host = (urlparse(link).netloc or "").lower()
                if not any(k in host for k in host_keywords):
                    continue
                title = re.sub(r"<[^>]+>", "", title_html)
                title = html.unescape(re.sub(r"\s+", " ", title)).strip()
                if len(title) < 6:
                    continue

                # 疑似栏目页，入队继续抓，扩大候选池
                if re.search(
                    r"/(index|list|channel|news|yaowen|politics|world|china|society|tech|finance|mil|military)/",
                    link,
                    re.I,
                ) and link not in visited_page:
                    if link not in section_candidates:
                        section_candidates.append(link)

                if not is_probable_article_url(link):
                    continue

                if link in seen:
                    continue
                seen.add(link)
                items.append(
                    {
                        "title": title,
                        "url": link,
                        "img": "",
                        "read_num": "",
                        "origin": origin_name,
                        # 优先从 URL 路径解析日期；缺失则留空由详情页补全
                        "release_time": sources_module.infer_release_time_from_news_url(link),
                        "content": "",
                        "comment_num": "",
                        "comment": "",
                        "unique_id": md5_hex(link),
                    }
                )
                if len(items) >= limit:
                    break
            if len(items) < limit and section_candidates:
                page_queue.extend(section_candidates[:3])
                section_candidates = section_candidates[3:]

        if not items:
            raise ValueError(f"{origin_name} homepage parse empty")

        print(f"[SOURCE] {origin_name} homepage items: {len(items)}")
        out_df = pd.DataFrame(items)
        if return_df_only:
            return out_df
        return write_to_db_df(out_df, origin_name)

    def crawl_tencent_api(page_size=RAW_FETCH_LIMIT, return_df_only: bool = False):
        """
        Tencent primary crawler via public JSON API.
        """
        api_url = f"https://r.inews.qq.com/gw/event/hot_ranking_list?page_size={int(page_size)}"
        api_headers = dict(sources_module.build_article_fetch_headers(api_url))
        api_headers["Accept"] = "application/json,text/plain,*/*"
        resp = _http_get_ignore_proxy(
            api_url,
            headers=api_headers,
            timeout=15,
            allow_redirects=True,
        )
        resp.raise_for_status()
        data = resp.json()
        idlist = data.get("idlist") or []
        if not idlist:
            raise ValueError("tencent api idlist empty")
        newslist = idlist[0].get("newslist") or []
        if not newslist:
            raise ValueError("tencent api newslist empty")

        items = []
        for n in newslist:
            title = (n.get("title") or n.get("longtitle") or "").strip()
            link = (n.get("url") or n.get("surl") or n.get("short_url") or "").strip()
            if not title or not link:
                continue
            items.append(
                {
                    "title": title,
                    "url": link,
                    "img": "",
                    "read_num": "",
                    "origin": "腾讯新闻",
                    "release_time": (n.get("time") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    "content": (n.get("abstract") or ""),
                    "comment_num": "",
                    "comment": "",
                    "unique_id": md5_hex(str(n.get("id") or link)),
                }
            )
        if not items:
            raise ValueError("tencent api parsed empty")
        print(f"[SOURCE] 腾讯新闻 api items: {len(items)}")
        out_df = pd.DataFrame(items)
        if return_df_only:
            return out_df
        return write_to_db_df(out_df, "腾讯新闻")

    run_id = None
    try:
        run_id = _record_crawl_run_start(source_cfg)
        # --- 按 parser_name 分发到各新闻源抓取策略 ---
        if parser_name == "tencent":
            merged = []
            try:
                merged.append(crawl_tencent_api(page_size=RAW_FETCH_LIMIT, return_df_only=True))
            except Exception as api_err:
                print(f"[SOURCE] 腾讯新闻 api failed: {api_err}")
            custom_feed = request.args.get("feed")
            configured_feeds = _configured_feed_urls(source_cfg)
            feeds = [custom_feed] if custom_feed else (configured_feeds or [
                "https://news.qq.com/newsgn/rss_newsgn.xml",
                "https://news.qq.com/newsgn/rss_newssh.xml",
                "https://news.qq.com/newsgn/rss_newsfina.xml",
            ])
            try:
                merged.append(
                    crawl_rss_with_fallback(
                        feeds,
                        source_cfg.get("name") or "腾讯新闻",
                        return_df_only=True,
                        ignore_env_proxy=True,
                    )
                )
            except Exception as rss_err:
                print(f"[SOURCE] 腾讯新闻 rss fallback exhausted: {rss_err}")
            try:
                merged.append(crawl_tencent_web(limit=RAW_FETCH_LIMIT, return_df_only=True))
            except Exception as web_err:
                print(f"[SOURCE] 腾讯新闻 web fallback failed: {web_err}")
            merged = [m for m in merged if m is not None and not m.empty]
            if not merged:
                raise ValueError("腾讯新闻 all sources empty")
            api_return = write_to_db_df(pd.concat(merged, ignore_index=True), source_cfg.get("name") or "腾讯新闻")
        elif parser_name == "people":
            # 人民网 RSS 的 pubDate 与条目链接常为陈旧年份；随机抽样会淹没首页真实近稿。
            # 策略：多入口首页链（人民网首页 / 国际 / 财经，多为当年稿件），默认不走批量 RSS；可选 extra_json 开启。
            merged = []
            extra_lines = [x.strip() for x in str((source_extra or {}).get("list_seeds") or "").splitlines() if x.strip()]
            primary = (source_cfg.get("base_url") or "http://www.people.com.cn/").strip()
            if extra_lines:
                seed_urls = list(dict.fromkeys(extra_lines))
            else:
                seed_urls = list(
                    dict.fromkeys(
                        [
                            primary,
                            "http://world.people.com.cn/",
                            "http://finance.people.com.cn/",
                        ]
                    )
                )
            per_seed_limit = max(90, int(RAW_FETCH_LIMIT // max(1, len(seed_urls))))
            for su in seed_urls:
                try:
                    merged.append(
                        crawl_site_links(
                            base_url=su,
                            host_keywords=["people.com.cn", "people.cn"],
                            origin_name=source_cfg.get("name") or "人民网",
                            limit=per_seed_limit,
                            return_df_only=True,
                            people_strict_n1=False,
                            max_pages=16,
                        )
                    )
                except Exception as web_err:
                    print(f"[SOURCE] 人民网 seed={su} failed: {web_err}")

            custom_feed = request.args.get("feed")
            configured_feeds = _configured_feed_urls(source_cfg)
            extra_rss = [
                x.strip()
                for x in str((source_extra or {}).get("rss_feeds") or "").splitlines()
                if x.strip()
            ]
            people_use_rss = bool((source_extra or {}).get("people_use_rss"))
            if custom_feed or configured_feeds or extra_rss or people_use_rss:
                default_people_rss = [
                    "http://www.people.com.cn/rss/politics.xml",
                    "http://www.people.com.cn/rss/world.xml",
                    "http://www.people.com.cn/rss/finance.xml",
                    "http://www.people.com.cn/rss/society.xml",
                ]
                if custom_feed:
                    feeds = [custom_feed]
                else:
                    feeds = list(dict.fromkeys(extra_rss + configured_feeds + default_people_rss))
                try:
                    merged.append(crawl_rss_with_fallback(feeds, source_cfg.get("name") or "人民网", return_df_only=True))
                except Exception as rss_err:
                    print(f"[SOURCE] 人民网 rss fallback exhausted: {rss_err}")

            merged = [m for m in merged if m is not None and not m.empty]
            if not merged:
                raise ValueError("人民网 all sources empty")
            people_df = pd.concat(merged, ignore_index=True)
            if not people_df.empty and "url" in people_df.columns:
                people_df["_norm_u"] = people_df["url"].astype(str).map(storage_module.normalize_news_url)
                people_df = people_df.drop_duplicates(subset=["_norm_u"], keep="first").drop(columns=["_norm_u"])
            api_return = write_to_db_df(people_df, source_cfg.get("name") or "人民网")
        elif parser_name == "xinhuanet":
            merged = []
            try:
                merged.append(crawl_site_links(
                    base_url=source_cfg.get("base_url") or "https://www.news.cn/",
                    host_keywords=["news.cn", "xinhuanet.com"],
                    origin_name=source_cfg.get("name") or "新华社",
                    limit=RAW_FETCH_LIMIT,
                    return_df_only=True,
                ))
            except Exception as web_err:
                print(f"[SOURCE] 新华社 homepage failed: {web_err}")
            custom_feed = request.args.get("feed")
            configured_feeds = _configured_feed_urls(source_cfg)
            feeds = [custom_feed] if custom_feed else (configured_feeds or [
                "http://www.xinhuanet.com/politics/news_politics.xml",
                "http://www.xinhuanet.com/world/news_world.xml",
                "http://www.xinhuanet.com/fortune/news_fortune.xml",
                "http://www.xinhuanet.com/tech/news_tech.xml",
            ])
            try:
                merged.append(crawl_rss_with_fallback(feeds, source_cfg.get("name") or "新华社", return_df_only=True))
            except Exception as rss_err:
                print(f"[SOURCE] 新华社 rss fallback exhausted: {rss_err}")
            merged = [m for m in merged if m is not None and not m.empty]
            if not merged:
                raise ValueError("新华社 all sources empty")
            api_return = write_to_db_df(pd.concat(merged, ignore_index=True), source_cfg.get("name") or "新华社")
        elif parser_name == "chinanews":
            custom_feed = request.args.get("feed")
            configured_feeds = _configured_feed_urls(source_cfg)
            feeds = [custom_feed] if custom_feed else (configured_feeds or [
                "http://www.chinanews.com.cn/rss/scroll-news.xml",
                "http://www.chinanews.com.cn/rss/china.xml",
                "http://www.chinanews.com.cn/rss/world.xml",
                "http://www.chinanews.com.cn/rss/finance.xml",
                "http://www.chinanews.com.cn/rss/it.xml",
            ])
            api_return = crawl_rss_with_fallback(feeds, source_cfg.get("name") or "中国新闻网")
        elif (source_cfg.get("source_type") or "").lower() == "rss":
            custom_feed = request.args.get("feed")
            configured_feeds = [x.strip() for x in str(source_cfg.get("list_urls") or "").splitlines() if x.strip()]
            feeds = [custom_feed] if custom_feed else configured_feeds
            if not feeds:
                raise ValueError("rss source missing list_urls")
            api_return = crawl_rss_with_fallback(feeds, source_cfg.get("name") or source_cfg.get("code") or "新闻源")
        elif (source_cfg.get("source_type") or "").lower() == "list":
            extra = source_extra or {}
            host_keywords = extra.get("host_keywords") or []
            if isinstance(host_keywords, str):
                host_keywords = [host_keywords]
            base_url = source_cfg.get("base_url") or ""
            if not base_url:
                list_urls = [x.strip() for x in str(source_cfg.get("list_urls") or "").splitlines() if x.strip()]
                base_url = list_urls[0] if list_urls else ""
            if not base_url:
                raise ValueError("list source missing base_url")
            api_return = crawl_site_links(
                base_url=base_url,
                host_keywords=host_keywords or [urlparse(base_url).netloc],
                origin_name=source_cfg.get("name") or source_cfg.get("code") or "新闻源",
                limit=RAW_FETCH_LIMIT,
                return_df_only=False,
            )
        else:
            run_stats["error_message"] = "unknown source"
            if request.args.get("fmt") == "json":
                return json_spider_result(False, 400)
            return (
                "unknown source. use /sources to list supported sources"
                + "   "
                + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )

        _record_crawl_run_finish(run_id, source_cfg, "success", run_stats)
        # 爬取完成后再清理一遍：确保库内只保留符合“最近几天+图文+非视频”的数据
        if engine is not None:
            _purge_invalid_news_rows(engine, table_name, max_age_days)
        tail = "   " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        plain = run_stats.get("summary", api_return or "ok") + tail
        if request.args.get("fmt") == "json":
            run_stats["summary"] = plain
            return json_spider_result(True, 200)
        return plain
    except Exception as e:
        print(f"错误信息: {e}")
        run_stats["error_message"] = str(e)
        run_stats["summary"] = f"{build_visible_summary()}   {api_return or 'no more data'}"
        _record_crawl_run_finish(run_id, source_cfg, "failed", run_stats)
        if engine is not None:
            _purge_invalid_news_rows(engine, table_name, max_age_days)
        tail = "   " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        plain = run_stats["summary"] + tail
        if request.args.get("fmt") == "json":
            run_stats["summary"] = plain
            return json_spider_result(False, 500)
        return plain


def run_spider_by_source(source_id: str):
    """
    与手动请求 GET /spider?search_word=1&source=... 同源逻辑（供后台定时线程调用）。
    """
    sid = (source_id or "").strip().lower()
    with app.test_request_context("/spider", query_string={"search_word": "1", "source": sid}):
        return fun()


@app.route("/scheduler/config", methods=["GET", "POST"])
def scheduler_config_api():
    from scheduler import load_config, save_config, sync_scheduler_jobs

    if request.method == "GET":
        return jsonify(load_config())
    payload = request.get_json(force=True, silent=True)
    if not isinstance(payload, dict):
        return jsonify({"ok": False, "error": "invalid json"}), 400
    save_config(payload)
    try:
        sync_scheduler_jobs(run_spider_by_source)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    return jsonify({"ok": True})


if __name__=='__main__':
    # Flask debug 重载器会启动父子进程；仅在子进程或关闭 debug 时挂载调度器，避免重复任务。
    _should_start_scheduler = (not app.debug) or (os.environ.get("WERKZEUG_RUN_MAIN") == "true")
    if _should_start_scheduler:
        try:
            from scheduler import init_scheduler_on_startup

            init_scheduler_on_startup(run_spider_by_source)
        except Exception as e:
            print(f"[SCHEDULER] 未启动定时任务: {e}")
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
    )
