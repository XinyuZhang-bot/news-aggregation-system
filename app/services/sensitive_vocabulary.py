# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 敏感词
class Sensitive_vocabulary(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "sensitive_vocabulary",
                # 分页大小
                "size": 10,
            }
        super(Sensitive_vocabulary, self).__init__(config_temp)
