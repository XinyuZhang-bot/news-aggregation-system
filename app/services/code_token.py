# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 验证码token
class Code_token(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "code_token",
                # 分页大小
                "size": 10,
            }
        super(Code_token, self).__init__(config_temp)
