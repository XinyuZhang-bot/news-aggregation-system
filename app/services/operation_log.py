# -*- coding: utf-8 -*-

from app.core.mysql import Service

# 操作日志
class Operation_log(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "operation_log",
                # 分页大小
                "size": 10,
            }
        super(Operation_log, self).__init__(config_temp)
