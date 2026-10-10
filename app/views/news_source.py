# -*- coding: utf-8 -*-
"""新闻源配置 API：返回已启用的新闻源列表（供前端/调度器使用）。"""
from app.core import controller

controllerClass = getattr(controller, "Controller")


class News_source(controllerClass):
    def __init__(self, config={}):
        config_init = {
            "tpl": "./news_source/",
            "service": "news_source",
            "get_api": ["enabled_list"],
            "post_api": [],
        }
        config_temp = config
        config_temp.update(config_init)
        super(News_source, self).__init__(config_temp)

    def Enabled_list(self, ctx):
        service = self.service
        rows = service.run(
            "SELECT * FROM `news_source` "
            "WHERE `enabled` = 1 "
            "ORDER BY `priority` DESC, `interval_minutes` ASC, `news_source_id` ASC"
        ) or []
        return {"result": {"list": rows, "count": len(rows)}}
