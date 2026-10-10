# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 导航
class Nav(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./nav/",
            # Service 名称
            "service": "nav",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Nav, self).__init__(config_temp)
