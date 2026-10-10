# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 视频类
class Video(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./video/",
            # Service 名称
            "service": "video",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Video, self).__init__(config_temp)

    def Index(self, ctx):
        query = dict(ctx.query)
        query["type"] = "video"
        config_plus = {}
        if "field" in query:
            field = query.pop("field")
            config_plus["field"] = field
        if "page" in query:
            page = query.pop("page")
            config_plus["page"] = page
        if "size" in query:
            size = query.pop("size")
            config_plus["size"] = size

        config_temp = self.config
        config_temp.update(config_plus)
        obj = self.service.Get_obj(query, config_temp)
        name_arr = obj["name"].split(".")
        obj["extension"] = name_arr[len(name_arr) - 1]
        result_dict = {"obj": obj}
        model = self.model(ctx, result_dict)
        return ctx.render(self.config["tpl"] + "index" + ".html", model)
