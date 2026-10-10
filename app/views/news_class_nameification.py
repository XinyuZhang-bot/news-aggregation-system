# -*- coding: utf-8 -*-

from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")

# 新闻分类
class News_class_nameification(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./news_class_nameification/",
            # 注册API
            "get_api": [],
            # POST API 路由
            "post_api": [],
            # Service 名称
            "service": "news_class_nameification",
        }
        config_temp = config
        config_temp.update(config_init)
        super(News_class_nameification , self).__init__(config_temp)





