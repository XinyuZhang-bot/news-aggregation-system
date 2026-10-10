# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 操作日志
class Operation_log(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./operation_log/",
            # Service 名称
            "service": "operation_log",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Operation_log, self).__init__(config_temp)
