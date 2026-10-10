# -*- coding: utf-8 -*-
"""
RBAC 权限中间件：基于 auth 表配置，按用户组控制页面/API 访问。

认证流程：x-auth-token 请求头 → access_token 表查 user_id → session 缓存。
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from app.service import service_select
from django.shortcuts import render
import json
import datetime

dict_auth = {}


class Auth:
    """权限校验：根据 path + user_group 返回该路由的增删改查权限配置。"""

    def Check(self, user, path, method="get"):
        auth = self.Get_dict()
        model_auth = {
                "auth_id": 0,
                "user_group": "访客",
                "mod_name": "",
                "table_name": "",
                "page_title": "",
                "path": "",
                "add": 0,
                "del": 0,
                "set": 0,
                "get": 1,
                "field_add": "",
                "field_set": "",
                "field_get": "",
                "table_nav_name": "",
                "table_nav": 0,
                "option": {
                    "examine": False,
                    "can_show_comment": False,
                    "can_comment": False,
                    "can_show_score": False,
                    "can_score": False,
                },
            }
        user_group = "游客"
        if user:
            user_group = user["user_group"]

        if (path in auth) and auth[path] and (user_group in auth[path]) and auth[path][user_group]:
            model_auth = auth[path][user_group]
        else:
            if user_group == "管理员":
                model_auth = {
                    "auth_id": 0,
                    "user_group": "管理员",
                    "mod_name": "",
                    "table_name": "",
                    "page_title": "",
                    "path": "",
                    "add": 1,
                    "del": 1,
                    "set": 1,
                    "get": 1,
                    "field_add": "",
                    "field_set": "",
                    "field_get": "",
                    "table_nav_name": "",
                    "table_nav": 1,
                    "option": {
                        "examine": True,
                        "can_show_comment": True,
                        "can_comment": True,
                        "can_show_score": True,
                        "can_score": True,
                    },
                }
        if model_auth[method]:
            return model_auth
        return ""

    def Get_dict(self):
        if len(dict_auth.keys()) == 0:
            service = service_select("auth")
            lst = service.Get_list({}, {"page": 0})
            for o in lst:
                if "option" in o and o["option"]:
                    o["option"] = json.loads(o["option"])
                else:
                    o["option"] = {}
                path = o["path"]
                if path not in dict_auth:
                    dict_auth[path] = {}
                dict_auth[path][o["user_group"]] = o
        return dict_auth


auth = Auth()


class AuthMiddleware(MiddlewareMixin):
    """请求拦截：解析 token 获取用户，非 /api 路径校验页面访问权限。"""

    def process_request(self, request):
        path = request.path
        if ("x-auth-token" in request.headers) and request.headers["x-auth-token"]:
            user = None
            token = request.headers["x-auth-token"]
            user_id = request.session.get("token", None)
            if not user_id:
                if token:
                    obj = service_select("access_token").Get_obj(
                        {"token": token}
                    )
                    if obj:
                        user_id = obj["user_id"]
            if user_id:
                create_time = datetime.datetime.strptime(obj["create_time"], "%Y-%m-%d %H:%M:%S")
                now_time = datetime.datetime.now()
                create_stamp = create_time + datetime.timedelta(minutes = 60 * obj["maxage"])
                if create_stamp > now_time:
                    request.session[token] = user_id
                    user = service_select("user").Get_obj(
                        {"user_id": user_id}
                    )

            if path.find("/api") == 0:
                pass
            else:
                model_auth = auth.Check(user, path, "get")
                if model_auth:
                    request.auth = model_auth
                else:
                    return render(request, "403.html", {}, status=403)
