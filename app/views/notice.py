# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 公告
class Notice(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./notice/",
            # Service 名称
            "service": "notice",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Notice, self).__init__(config_temp)
