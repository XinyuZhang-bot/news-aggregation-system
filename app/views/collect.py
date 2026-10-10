# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 收藏
class Collect(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./collect/",
            # Service 名称
            "service": "collect",
            # 唯一判断
            "unique": ["source_table", "source_field", "source_id", "user_id"]
        }
        config_temp = config
        config_temp.update(config_init)
        super(Collect, self).__init__(config_temp)

    # 增
    def Add(self, ctx):
        check_obj = self.service.Get_obj(ctx.body, self.config)
        if not check_obj is None:
            return {"result": "已收藏"}
        result = self.service.Add(ctx.body, self.config)
        if self.service.error:
            return {"error": self.service.error}
        return {"result": result}