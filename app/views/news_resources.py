# -*- coding: utf-8 -*-

from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")

# 新闻资源
class News_resources(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./news_resources/",
            # 注册API
            "get_api": [],
            # POST API 路由
            "post_api": [],
            # Service 名称
            "service": "news_resources",
        }
        config_temp = config
        config_temp.update(config_init)
        super(News_resources , self).__init__(config_temp)





