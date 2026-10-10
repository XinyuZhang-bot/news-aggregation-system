# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 新闻
class News(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./news/",
            # Service 名称
            "service": "news",
            "interact": ["comment", "praise", "score", "collect", "hits"],
        }
        config_temp = config
        config_temp.update(config_init)
        super(News, self).__init__(config_temp)
