# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 编辑人员服务
class Compileors(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "compileors",
                # 分页大小
                "size": 30,
                "page": 1,
            }
        super(Compileors , self).__init__(config_temp)
