# -*- coding: utf-8 -*-
"""站点入口：将根路径 / 重定向到 Vue 前台构建产物。"""
import os

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotFound

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 合并多个配置字典
def obj_update(*config):
    config_temp = {}
    for o in config:
        config_temp.update(o)
    return config_temp


# 首页
class Index(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./user/",
            # Service 名称
            "service": "article",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Index, self).__init__(config_temp)

    # 首页
    def Index(self, ctx):
        # 本项目首页由前端构建产物承载（static/home/dist/index.html）。
        # 这里必须用重定向：index.html 内部的 js/css 多为相对路径，
        # 若直接在 “/” 返回会导致资源路径错误从而白屏。
        index_path = os.path.join(
            settings.BASE_DIR, "static", "home", "dist", "index.html"
        )
        if os.path.exists(index_path):
            return HttpResponseRedirect("/static/home/dist/index.html")

        return HttpResponseNotFound("static/home/dist/index.html not found")
