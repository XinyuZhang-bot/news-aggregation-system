# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 权限
class Auth(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "auth",
                # 分页大小
                "size": 100
            }
        super(Auth, self).__init__(config_temp)
