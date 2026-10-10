# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 浏览记录
class History(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./history/",
            # Service 名称
            "service": "history",
        }
        config_temp = config
        config_temp.update(config_init)
        super(History, self).__init__(config_temp)
