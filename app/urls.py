# -*- coding: utf-8 -*-
"""
Django URL 自动注册：扫描 app/views/ 下每个模块，按 Controller.config 注册路由。

路由规则示例（模块 news_information）：
  GET  /news_information/list      → List()
  GET  /api/news_information/get_list → Get_list()
  POST /api/news_information/add     → Add()
"""
from django.urls import path
from app.router import router

import importlib
import os

urlpatterns = []

controller_dir = os.path.join(os.getcwd(), "app", "views")
arr = []


def foreach_file(path_name):
    for root, dirs, files in os.walk(path_name):
        for f in files:
            arr.append(os.path.join(root, f))


def loadModule(f):
    route_path = os.path.splitext(os.path.basename(f))[0]
    mod = importlib.import_module("app.views." + route_path)
    cs_controller = getattr(mod, route_path.capitalize())
    controller = cs_controller()
    if route_path == "index":
        loadRoute(controller, "")
    else:
        loadRoute(controller, route_path)


def loadRoute(controller, route_path):
    get = controller.config["get"]
    post = controller.config["post"]
    get_api = controller.config["get_api"]
    post_api = controller.config["post_api"]

    def append_urlpatterns(req_method, route_path_plus, action):
        router_method = router(req_method, getattr(controller, action))
        urlpatterns.append(path(route_path_plus, router_method))

    if hasattr(controller, "Index"):
        append_urlpatterns("all", route_path, "Index")
    if hasattr(controller, "Api"):
        append_urlpatterns("all", "api" + "/" + route_path, "Api")
    for action in get:
        if action == "index":
            append_urlpatterns("get", action, action.capitalize())
        elif not route_path == "":
            append_urlpatterns("get", route_path + "/" + action, action.capitalize())
    for action in post:
        if action == "index":
            append_urlpatterns("post", action, action.capitalize())
        else:
            append_urlpatterns("post", route_path + "/" + action, action.capitalize())
    for action in get_api:
        if action == "index":
            append_urlpatterns("get", "api" + "/" + route_path, action.capitalize())
        else:
            append_urlpatterns("get", "api" + "/" + route_path + "/" + action, action.capitalize())

    for action in post_api:
        if action == "index":
            append_urlpatterns("post", "api" + "/" + route_path, action.capitalize())
        else:
            append_urlpatterns("post", "api" + "/" + route_path + "/" + action, action.capitalize())


foreach_file(controller_dir)

for f in arr:
    if f.find(".pyc") == -1 and f.find("__init__") == -1:
        loadModule(f)
