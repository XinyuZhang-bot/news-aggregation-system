# -*- coding: utf-8 -*-

from app.core.mysql import Service


class Private_message(Service):
    def __init__(self, *config):
        if config:
            config_temp = config[0]
        else:
            config_temp = {
                "table": "private_message",
                "size": 30,
                "page": 1,
            }
        super(Private_message, self).__init__(config_temp)
