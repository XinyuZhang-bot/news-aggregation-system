# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 关注用户
class Follow(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "follow",
                # 分页大小
                "size": 10,
            }
        super(Follow, self).__init__(config_temp)
