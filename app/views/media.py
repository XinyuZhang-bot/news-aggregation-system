# -*- coding: utf-8 -*-

from app.core import controller

controllerClass = getattr(controller, "Controller")


# 媒体
class Media(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./media/",
            # Service 名称
            "service": "upload",
            "get": ["video", "image", "audio"],
        }
        config_temp = config
        config_temp.update(config_init)
        super(Media, self).__init__(config_temp)

    def Video(self, ctx):
        model = self.model(ctx, {})
        return ctx.render(self.config["tpl"] + "video.html", model)

    def Image(self, ctx):
        model = self.model(ctx, {})
        return ctx.render(self.config["tpl"] + "image.html", model)

    def Audio(self, ctx):
        model = self.model(ctx, {})
        return ctx.render(self.config["tpl"] + "audio.html", model)
