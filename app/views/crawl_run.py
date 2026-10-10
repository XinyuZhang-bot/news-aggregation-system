# -*- coding: utf-8 -*-
"""抓取运行记录：供管理端展示每次爬虫任务的成功/失败与统计。"""
from app.core import controller


controllerClass = getattr(controller, "Controller")


class Crawl_run(controllerClass):
    def __init__(self, config={}):
        config_init = {
            "tpl": "./crawl_run/",
            "service": "crawl_run",
            "get_api": ["summary"],
            "post_api": [],
        }
        config_temp = config
        config_temp.update(config_init)
        super(Crawl_run, self).__init__(config_temp)

    def Summary(self, ctx):
        service = self.service

        def _run(sql):
            try:
                return service.run(sql) or []
            except Exception:
                return []

        total = _run("SELECT COUNT(*) AS cnt FROM `crawl_run`")
        success = _run("SELECT COUNT(*) AS cnt FROM `crawl_run` WHERE `status` = 'success'")
        failed = _run("SELECT COUNT(*) AS cnt FROM `crawl_run` WHERE `status` = 'failed'")
        today = _run(
            "SELECT COUNT(*) AS cnt FROM `crawl_run` "
            "WHERE DATE(`started_at`) = CURDATE()"
        )
        source_rank = _run(
            "SELECT COALESCE(NULLIF(TRIM(`source_name`), ''), COALESCE(NULLIF(TRIM(`source_code`), ''), '未知来源')) AS name, "
            "COUNT(*) AS cnt "
            "FROM `crawl_run` GROUP BY name ORDER BY cnt DESC LIMIT 10"
        )
        error_rank = _run(
            "SELECT COALESCE(NULLIF(TRIM(`error_message`), ''), '未知错误') AS name, COUNT(*) AS cnt "
            "FROM `crawl_run` WHERE `status` = 'failed' "
            "GROUP BY name ORDER BY cnt DESC LIMIT 10"
        )
        return {
            "result": {
                "total": int(total[0].get("cnt") or 0) if total else 0,
                "success": int(success[0].get("cnt") or 0) if success else 0,
                "failed": int(failed[0].get("cnt") or 0) if failed else 0,
                "today": int(today[0].get("cnt") or 0) if today else 0,
                "source_rank": source_rank,
                "error_rank": error_rank,
            }
        }
