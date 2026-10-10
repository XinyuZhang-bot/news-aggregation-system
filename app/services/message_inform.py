# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 通知记录服务
class Message_inform(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "message_inform",
                # 分页大小
                "size": 30,
                "page": 1,
            }
        super(Message_inform , self).__init__(config_temp)
