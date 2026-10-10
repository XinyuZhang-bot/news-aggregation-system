# -*- coding: utf-8 -*-

from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")

# 通知记录
class Message_inform(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./message_inform/",
            # Service 名称
            "service": "message_inform",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Message_inform , self).__init__(config_temp)





