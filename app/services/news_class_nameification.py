# -*- coding: utf-8 -*-

from app.core.mysql import Service


# 新闻分类服务
class News_class_nameification(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                # 操作的表
                "table": "news_class_nameification",
                # 分页大小
                "size": 30,
                "page": 1,
            }
        super(News_class_nameification , self).__init__(config_temp)
