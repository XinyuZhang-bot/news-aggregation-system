# -*- coding: utf-8 -*-
"""
定时自动爬取：threading 后台轮询，按 news_source 表的 enabled/interval_minutes 触发。

配置优先读数据库 news_source；无库时回退 scheduler_config.json。
与 HTTP GET /spider 同源，通过 run_spider_fn(source_id) 执行。
"""
from __future__ import annotations

import json
import os
import threading
import time
import configparser
from typing import Any, Callable, Dict, Optional

import pandas as pd
from sqlalchemy import create_engine

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scheduler_config.json")
SPIDER_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_INI_PATH = os.path.join(SPIDER_DIR, "config", "config.ini")

DEFAULT_SOURCES: Dict[str, Dict[str, Any]] = {
    "tencent": {"enabled": False, "interval_minutes": 5},
    "people": {"enabled": False, "interval_minutes": 5},
    "xinhuanet": {"enabled": False, "interval_minutes": 5},
    "chinanews": {"enabled": False, "interval_minutes": 5},
}


def _get_engine():
    if not os.path.exists(CONFIG_INI_PATH):
        return None
    parser = configparser.ConfigParser()
    parser.read(CONFIG_INI_PATH, encoding="utf-8")
    if not parser.has_section("db"):
        return None
    try:
        user = parser.get("db", "user")
        password = parser.get("db", "password").replace("!", "%21").replace("@", "%40")
        host = parser.get("db", "host")
        port = parser.get("db", "port")
        database = parser.get("db", "database")
        return create_engine(
            "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)
        )
    except Exception:
        return None


def _load_sources_from_db() -> Optional[Dict[str, Dict[str, Any]]]:
    engine = _get_engine()
    if engine is None:
        return None
    try:
        df = pd.read_sql(
            "SELECT `code`, `enabled`, `interval_minutes` FROM `news_source` ORDER BY `priority` DESC, `news_source_id` ASC",
            engine,
        )
    except Exception:
        return None
    if df.empty:
        return None
    sources = {}
    for _, row in df.iterrows():
        code = str(row.get("code") or "").strip().lower()
        if not code:
            continue
        try:
            interval_minutes = int(row.get("interval_minutes") or 5)
        except Exception:
            interval_minutes = 5
        sources[code] = {
            "enabled": bool(int(row.get("enabled") or 0)),
            "interval_minutes": max(1, interval_minutes),
        }
    return sources or None


def _save_sources_to_db(sources: Dict[str, Dict[str, Any]]) -> None:
    engine = _get_engine()
    if engine is None:
        return
    conn = None
    try:
        conn = engine.raw_connection()
        cur = conn.cursor()
        for sid, meta in (sources or {}).items():
            enabled = 1 if meta.get("enabled") else 0
            try:
                mins = max(1, int(meta.get("interval_minutes") or 5))
            except Exception:
                mins = 5
            cur.execute(
                "UPDATE `news_source` SET `enabled`=%s, `interval_minutes`=%s WHERE `code`=%s",
                (enabled, mins, sid),
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

_lock = threading.RLock()
_run_fn: Optional[Callable[[str], Any]] = None
_last_run_ts: Dict[str, float] = {}
_run_lock = threading.Lock()
_worker_thread: Optional[threading.Thread] = None
_stop = threading.Event()
_TICK_SEC = 15.0  # 轮询间隔（秒），不宜过小以免频繁读盘


def default_config() -> Dict[str, Any]:
    db_sources = _load_sources_from_db()
    if db_sources:
        return {"sources": db_sources}
    return {"sources": {k: dict(v) for k, v in DEFAULT_SOURCES.items()}}


def load_config() -> Dict[str, Any]:
    with _lock:
        db_cfg = default_config()
        if db_cfg.get("sources"):
            return db_cfg
        if not os.path.exists(CONFIG_PATH):
            cfg = default_config()
            save_config(cfg)
            return cfg
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "sources" not in data or not isinstance(data["sources"], dict):
            data = default_config()
            save_config(data)
            return data
        base = default_config()
        for sid, meta in base["sources"].items():
            if sid not in data["sources"]:
                data["sources"][sid] = meta
        for sid in list(data["sources"].keys()):
            if sid not in base["sources"]:
                del data["sources"][sid]
        return data


def save_config(cfg: Dict[str, Any]) -> None:
    with _lock:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        _save_sources_to_db(cfg.get("sources") or {})


def _tick(run_spider_fn: Callable[[str], Any]) -> None:
    cfg = load_config()
    sources = cfg.get("sources") or {}
    now = time.time()

    for sid, meta in sources.items():
        if not isinstance(meta, dict) or not meta.get("enabled"):
            continue
        try:
            mins = int(meta.get("interval_minutes") or 5)
        except (TypeError, ValueError):
            mins = 5
        mins = max(1, mins)
        period = float(mins * 60)
        prev = _last_run_ts.get(sid, 0.0)
        if now - prev < period:
            continue
        with _run_lock:
            try:
                run_spider_fn(sid)
            except Exception as e:
                print(f"[SCHEDULER] 执行失败 source={sid}: {e}")
        _last_run_ts[sid] = time.time()


def _worker_loop() -> None:
    while not _stop.wait(timeout=_TICK_SEC):
        fn = _run_fn
        if fn is None:
            continue
        try:
            _tick(fn)
        except Exception as e:
            print(f"[SCHEDULER] 轮询异常: {e}")


def _ensure_worker_started() -> None:
    global _worker_thread
    if _worker_thread is not None and _worker_thread.is_alive():
        return
    _stop.clear()
    t = threading.Thread(target=_worker_loop, daemon=True, name="news-spider-scheduler")
    t.start()
    _worker_thread = t


def sync_scheduler_jobs(run_spider_fn: Callable[[str], Any]) -> None:
    """
    注册 run_spider_fn 并确保后台线程运行；保存配置后调用即可生效。
    """
    global _run_fn
    _run_fn = run_spider_fn
    _ensure_worker_started()


def init_scheduler_on_startup(run_spider_fn: Callable[[str], Any]) -> None:
    sync_scheduler_jobs(run_spider_fn)
