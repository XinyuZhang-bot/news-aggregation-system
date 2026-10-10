# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 导航
class Nav(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "nav",
                # 分页大小
                "size": 0,
            }
        super(Nav, self).__init__(config_temp)
