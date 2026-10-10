# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 关注用户
class Follow(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./follow/",
            # Service 名称
            "service": "follow",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Follow, self).__init__(config_temp)
