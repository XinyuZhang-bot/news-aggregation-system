# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 点赞
class Praise(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./praise/",
            # Service 名称
            "service": "praise",
            # 唯一判断
            "unique": ["source_table", "source_field", "source_id", "user_id"]
        }
        config_temp = config
        config_temp.update(config_init)
        super(Praise, self).__init__(config_temp)
