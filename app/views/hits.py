# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 导航
class Hits(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./hits/",
            # Service 名称
            "service": "hits",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Hits, self).__init__(config_temp)
