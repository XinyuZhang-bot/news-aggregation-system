# -*- coding: utf-8 -*-

from app.core.mysql import Service

# 浏览记录
class History(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "history",
                # 分页大小
                "size": 10,
            }
        super(History, self).__init__(config_temp)
