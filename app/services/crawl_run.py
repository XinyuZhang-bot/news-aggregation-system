# -*- coding: utf-8 -*-

from app.core.mysql import Service


class Crawl_run(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                "table": "crawl_run",
                "size": 30,
                "page": 1,
            }
        super(Crawl_run, self).__init__(config_temp)
