# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 普通用户服务
class Ordinary_user(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "ordinary_user",
                # 分页大小
                "size": 30,
                "page": 1,
            }
        super(Ordinary_user , self).__init__(config_temp)
