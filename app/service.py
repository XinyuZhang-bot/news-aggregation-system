# -*- coding: utf-8 -*-
"""
Service 自动加载：扫描 app/services/ 目录，按类名（如 News_information）提供单例。

用法：service_select("news_information") → News_information 实例
"""
import os
import importlib

services_abspath_arr = []
services_arr = []
services_dir = os.path.join(os.getcwd(), "app", "services")


def service_select(str):
    for service_item in services_arr:
        if str.capitalize() == service_item.__class__.__name__:
            return service_item


def foreach_file(path_name):
    for root, dirs, files in os.walk(path_name):
        for f in files:
            services_abspath_arr.append(os.path.join(root, f))


def loadModule(f):
    f = os.path.splitext(os.path.basename(f))[0]

    mod = importlib.import_module("app.services." + f)
    cs_service = getattr(mod, f.capitalize())
    service = cs_service()
    services_arr.append(service)


foreach_file(services_dir)

for f in services_abspath_arr:
    if f.find(".pyc") == -1 and f.find("__init__") == -1:
        loadModule(f)
