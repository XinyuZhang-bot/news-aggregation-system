# -*- coding: utf-8 -*-

from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")

# 授权
class Auth(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./auth/",
            # Service 名称
            "service": "auth",
			"like": False
        }
        config_temp = config
        config_temp.update(config_init)
        super(Auth, self).__init__(config_temp)
