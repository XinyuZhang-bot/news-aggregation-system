# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 轮播图
class User_group(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./user_group/",
            # Service 名称
            "service": "user_group",
        }
        config_temp = config
        config_temp.update(config_init)
        super(User_group, self).__init__(config_temp)
