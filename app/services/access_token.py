# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 临时访问牌
class Access_token(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "access_token",
                # 分页大小
                "size": 10,
            }
        super(Access_token, self).__init__(config_temp)
