# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 敏感词
class Sensitive_vocabulary(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./sensitive_vocabulary/",
            # Service 名称
            "service": "sensitive_vocabulary",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Sensitive_vocabulary, self).__init__(config_temp)
