# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 轮播图
class Slides(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./slides/",
            # Service 名称
            "service": "slides",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Slides, self).__init__(config_temp)
