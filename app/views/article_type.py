# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 论坛类型
class Article_type(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./article_type/",
            # Service 名称
            "service": "article_type"
        }
        config_temp = config
        config_temp.update(config_init)
        super(Article_type, self).__init__(config_temp)
