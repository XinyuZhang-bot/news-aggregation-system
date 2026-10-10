# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 新闻资源服务
class News_resources(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "news_resources",
                # 分页大小
                "size": 30,
                "page": 1,
            }
        super(News_resources , self).__init__(config_temp)
