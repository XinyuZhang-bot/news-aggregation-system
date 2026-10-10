# -*- coding: utf-8 -*-

from app.core import controller
from django.http import FileResponse
from django.utils.encoding import escape_uri_path

controllerClass = getattr(controller, "Controller")


# 下载
class Download(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./download/",
            # Service 名称
            "service": "upload",
        }
        config_temp = {}
        config_temp.update(config)
        config_temp.update(config_init)
        super(Download, self).__init__(config_temp)

    # 下载文件
    def Index(self, ctx):
        src = ctx.query["src"]
        name = src.split("/")[-1]
        filename = open("static" + src, "rb")
        response = FileResponse(filename)
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = "attachment; filename*=utf-8''{}".format(escape_uri_path(name))
        return response
