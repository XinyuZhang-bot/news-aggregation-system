# -*- coding: utf-8 -*-

from app.core.mysql import Service


class News_source(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                "table": "news_source",
                "size": 30,
                "page": 1,
            }
        super(News_source, self).__init__(config_temp)
