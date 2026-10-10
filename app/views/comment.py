# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 评论
class Comment(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./comment/",
            # Service 名称
            "service": "comment",
			"like": False
        }
        config_temp = config
        config_temp.update(config_init)
        super(Comment, self).__init__(config_temp)
