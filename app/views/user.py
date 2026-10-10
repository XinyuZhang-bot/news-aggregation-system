# -*- coding: utf-8 -*-

from hashlib import md5
from datetime import date, timedelta
from app.core import controller
from app.service import service_select
from django.utils import timezone
import json
import re
import time

controllerClass = getattr(controller, "Controller")


# 计算字符串 MD5（用于 token 等）
def md5hash(key):
    input_name = md5()
    input_name.update(key.encode("utf-8"))
    return input_name.hexdigest()


# 合并多个配置字典
def obj_update(*config):
    config_temp = {}
    for o in config:
        config_temp.update(o)
    return config_temp


def is_valid_username(username: str) -> bool:
    username = (username or "").strip()
    if not username:
        return False
    if len(username) < 2 or len(username) > 16:
        return False
    if not re.fullmatch(r"[A-Za-z0-9\u4e00-\u9fa5]+", username):
        return False
    if username.isdigit():
        return False
    return True


def _normalize_optional_phone(phone) -> str:
    return str(phone or "").strip()


def tokenGetUserId(token, request):
    """根据 token 从 session 或 access_token 表解析 user_id。"""
    if not token:
        return 0
    user_id = request.session.get(token)
    if user_id:
        return user_id
    obj = service_select("access_token").Get_obj({"token": token})
    if obj:
        return obj.get("user_id") or 0
    return 0


# 用户账户与后台统计
class User(controllerClass):
    def __init__(self, config=None):
        if config is None:
            config = {}
        config_init = {
            "tpl": "./user/",
            "service": "user",
            "get_api": [
                "state",
                "quit",
                "admin_dashboard",
                "news_resources_origin",
                "viewed_news_categories",
            ],
            "post_api": ["login", "register", "change_password", "forget_password"],
            "unique": ["username"],
        }
        config_temp = config
        config_temp.update(config_init)
        super(User, self).__init__(config_temp)

    def Register(self, ctx):
        
        print("===================注册=====================")
        userService = service_select("user")
        body = ctx.body or {}

        username = (body.get("username") or "").strip()
        password = (body.get("password") or "").strip()
        user_group = (body.get("user_group") or "").strip()
        nickname = (body.get("nickname") or username or "").strip()
        phone = _normalize_optional_phone(body.get("phone"))

        if not username:
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "用户名不能为空",
                }
            }, ensure_ascii=False))
        if not is_valid_username(username):
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "用户名需为 2～16 个字符，支持中文/英文/数字及其混合，但不能为纯数字",
                }
            }, ensure_ascii=False))
        if not password:
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "密码不能为空",
                }
            }, ensure_ascii=False))
        if len(password) < 6 or len(password) > 64:
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "密码长度需在 6～64 个字符",
                }
            }, ensure_ascii=False))
        if not user_group:
            user_group = "编辑人员"
        allowed_groups = ("编辑人员", "普通用户")
        if user_group not in allowed_groups:
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "仅支持注册为：编辑人员、普通用户",
                }
            }, ensure_ascii=False))

        post_param = {
            "username": username,
            "nickname": nickname[:16] if nickname else username[:16],
            "password": password,
            "user_group": user_group,
            "avatar": (body.get("avatar") or "").strip() or "/static/upload/default_avatar.jpg",
            "phone": phone[:11] if phone else "",
            "state": 1,
        }

        obj = userService.Get_obj({"username": post_param["username"]}, {"like": False})
        if obj:
            return ctx.response(json.dumps({
                "error": {
                    "code": 70000,
                    "message": "用户名已存在",
                }
            }, ensure_ascii=False))

        ret = {
            "error": {
                "code": 70000,
                "message": "注册失败",
            }
        }
        bl = userService.Add(post_param)
        if not bl:
            return ctx.response(json.dumps(ret, ensure_ascii=False))

        new_user = userService.Get_obj({"username": post_param["username"]}, {"like": False})
        if not new_user:
            return ctx.response(json.dumps(ret, ensure_ascii=False))
        uid = new_user["user_id"]
        display_name = post_param["nickname"] or username

        try:
            if user_group == "编辑人员":
                service_select("compileors").Add(
                    {
                                "users_phone": phone,
                        "examine_state": "已通过",
                        "user_id": uid,
                        "create_by": 1,
                    }
                )
            elif user_group == "普通用户":
                service_select("ordinary_user").Add(
                    {
                                "users_mobile_phone": phone,
                        "examine_state": "已通过",
                        "user_id": uid,
                        "create_by": 1,
                    }
                )
        except Exception as e:
            userService.Del({"user_id": uid})
            return ctx.response(
                json.dumps(
                    {
                        "error": {
                            "code": 70000,
                            "message": "注册失败：扩展资料写入异常，请稍后重试",
                        }
                    },
                    ensure_ascii=False,
                )
            )

        ret = {
            "result": {
                "bl": True,
                "message": "注册成功",
                "user_id": uid,
            }
        }
        return ctx.response(json.dumps(ret, ensure_ascii=False))

    def Forget_password(self, ctx):
        
        print("===================修改密码=====================")
        body = ctx.body

        def error_response(message):
            return ctx.response(
                json.dumps(
                    {"error": {"code": 70000, "message": message}},
                    ensure_ascii=False,
                )
            )

        if not body.get("code"):
            return error_response("验证码不存在或者错误")

        # 获取用户
        obj = service_select("user").Get_obj(
            {"username": body.get("username")}, {"like": False}
        )

        if not obj:
            return error_response("用户名不存在或者错误")

        password = body.get("password")
        if not password:
            return error_response("密码不存在或者错误")

        # 修改密码
        bl = service_select("user").Set({"user_id": obj["user_id"]}, {"password": password})
        if bl:
            ret = {"result": {"bl": True, "message": "修改成功"}}
        else:
            ret = {
                "error": {
                    "code": 70000,
                    "message": "修改失败",
                }
            }
        return ctx.response(json.dumps(ret, ensure_ascii=False))

    def Login(self, ctx):
        
        print("===================登录=====================")
        ret = {
            "error": {
                "code": 70000,
                "message": "账户不存在",
            }
        }
        body = ctx.body
        # 获取用户
        password = body["password"] or ""
        obj = service_select("user").Get_obj(
            {"username": body["username"]}, {"like": False}
        )
        if obj:
            # 检查用户所属用户组
            user_group = service_select("user_group").Get_obj({'name': obj['user_group']}, {"like": False})
            if user_group and user_group['source_table'] != '':
                tbl = (user_group.get("source_table") or "").strip()
                user_obj = service_select(tbl).Get_obj({"user_id": obj['user_id']}, {"like": False})
                if not user_obj:
                    # 常见情况：只在 user 表手工建号，未写 ordinary_user / compileors，登录与后台列表会失败
                    phone = _normalize_optional_phone(obj.get("phone"))
                    if tbl == "ordinary_user":
                        service_select("ordinary_user").Add(
                            {
                                "users_mobile_phone": phone,
                                "examine_state": "已通过",
                                "user_id": obj["user_id"],
                                "create_by": 1,
                            }
                        )
                    elif tbl == "compileors":
                        service_select("compileors").Add(
                            {
                                "users_phone": phone,
                                "examine_state": "已通过",
                                "user_id": obj["user_id"],
                                "create_by": 1,
                            }
                        )
                    user_obj = service_select(tbl).Get_obj({"user_id": obj['user_id']}, {"like": False})
                if not user_obj:
                    ret = {
                        "error": {
                            "code": 70000,
                            "message": "账户扩展资料写入失败，请联系管理员",
                        }
                    }
                    return ctx.response(json.dumps(ret, ensure_ascii=False))
                if user_obj['examine_state'] == '未通过':
                    ret = {
                        "error": {
                            "code": 70000,
                            "message": "账户未通过审核",
                        }
                    }
                    return ret
                if user_obj['examine_state'] == '未审核':
                    ret = {
                        "error": {
                            "code": 70000,
                            "message": "账户未审核",
                        }
                    }
                    return ret
            # 校验用户状态
            if obj["state"] == 1:
                # 校验密码
                if obj["password"] == password:
                    # 生成Token
                    timeout = timezone.now()
                    timestamp = int(time.mktime(timeout.timetuple())) * 1000
                    token = md5hash(str(obj["user_id"]) + "_" + str(timestamp))
                    # 存储Token
                    ctx.request.session[token] = obj["user_id"]
                    service_select("access_token").Add(
                        {"token": token, "user_id": obj["user_id"]}
                    )
                    # 回传用户
                    obj["token"] = token
                    ret = {
                        "result": {"obj": obj}
                    }
                else:
                    ret = {
                        "error": {
                            "code": 70000,
                            "message": "密码错误",
                        }
                    }
            else:
                ret = {
                    "error": {
                        "code": 70000,
                        "message": "用户账户不可用，请联系管理员",
                    }
                }
        return ctx.response(json.dumps(ret, ensure_ascii=False))


    def Change_password(self, ctx):
        
        print("===================修改密码=====================")
        ret = {
            "error": {
                "code": 70000,
                "message": "账号未登录",
            }
        }
        request = ctx.request
        headers = request.headers
        # 判断Token
        if ("x-auth-token" in headers) and headers["x-auth-token"]:
            token = headers["x-auth-token"]
            user_id = tokenGetUserId(token, request)
            userService = service_select("user")
            # 获取密码和新密码
            body = ctx.body
            password = body["o_password"]
            # 判断用户密码是否正确
            obj = userService.Get_obj({"user_id": user_id, "password": password}, {"like": False})
            if obj:
                # 修改密码并返回结果
                password = body["password"]
                bl = userService.Set({"user_id": user_id}, {"password": password})
                if bl:
                    ret = {"result": {"bl": True, "message": "修改成功"}}
                else:
                    ret = {
                        "error": {
                            "code": 70000,
                            "message": "修改失败",
                        }
                    }
            else:
                ret = {
                    "error": {
                        "code": 70000,
                        "message": "密码错误",
                    }
                }
        else:
            ret = {
                "error": {
                    "code": 70000,
                    "message": "账户未登录",
                }
            }
        return ctx.response(json.dumps(ret, ensure_ascii=False))

    def State(self, ctx):
        
        print("===================获取登录态=====================")
        ret = {
            "error": {
                "code": 50000,
                "message": "账户未登录！"
            }
        }
        request = ctx.request
        headers = request.headers
        # 判断Token
        if ("x-auth-token" in headers) and headers["x-auth-token"]:
            token = headers.get("x-auth-token", None)
            user_id = tokenGetUserId(token, request)
            # 判断用户ID是否存在
            if user_id > 0:
                userService = service_select("user")
                user = userService.Get_obj({"user_id": user_id})
                user["token"] = token
                ret = {
                    "result": {
                        "obj": user
                    }
                }
        return json.dumps(ret, ensure_ascii=False)

    def Quit(self, ctx):
        ret = {"error": {"code": 50000, "message": "账户未登录！"}}
        request = ctx.request
        token = request.headers.get("x-auth-token")
        if token:
            try:
                del request.session[token]
            except Exception:
                pass
            service_select("access_token").Del({"token": token})
            ret = {"result": {"bl": True, "tip": "已退出！"}}
        return json.dumps(ret, ensure_ascii=False)

    def News_resources_origin(self, ctx):
        """爬虫资源按发布来源聚合，供图表使用。"""
        rows = service_select("news_resources").run(
            "SELECT COALESCE(NULLIF(TRIM(`origin`), ''), '未知') AS name, COUNT(*) AS value "
            "FROM `news_resources` GROUP BY name ORDER BY value DESC LIMIT 20"
        ) or []
        return {"result": {"list": rows}}

    def Viewed_news_categories(self, ctx):
        """指定用户浏览过的新闻分类分布（饼图数据）。"""
        user_id = str(ctx.query.get("user_id") or "").strip()
        if not user_id:
            return {"result": []}
        uid = str(int(user_id))
        sql = (
            "SELECT ni.news_categories AS name, SUM(t.weight) AS value FROM ("
            "SELECT h.source_id, 1.0 AS weight FROM hits h "
            "WHERE h.source_table = 'news_information' AND h.user_id = " + uid + " "
            "UNION ALL "
            "SELECT hs.source_id, 1.5 AS weight FROM history hs "
            "WHERE hs.source_table = 'news_information' AND hs.user_id = " + uid + " "
            "UNION ALL "
            "SELECT c.source_id, 4.0 AS weight FROM collect c "
            "WHERE c.source_table = 'news_information' AND c.user_id = " + uid + " "
            "UNION ALL "
            "SELECT p.source_id, 3.0 AS weight FROM praise p "
            "WHERE p.source_table = 'news_information' AND p.user_id = " + uid + " AND IFNULL(p.status, 1) = 1"
            ") t "
            "JOIN news_information ni ON ni.news_information_id = t.source_id "
            "GROUP BY ni.news_categories ORDER BY value DESC"
        )
        rows = self.service.run(sql) or []
        pie = []
        for row in rows:
            name = (row.get("name") or "").strip() or "未分类"
            pie.append({"name": name, "value": float(row.get("value") or 0)})
        return {"result": pie}

    def Admin_dashboard(self, ctx):
        """管理后台首页统计大屏数据。"""
        user_svc = self.service
        crawl_svc = service_select("crawl_run")
        news_svc = service_select("news_information")
        hits_svc = service_select("hits")

        def _monthly(sql_table):
            rows = user_svc.run(
                "SELECT DATE_FORMAT(create_time, '%Y-%m') AS m, COUNT(*) AS c "
                f"FROM `{sql_table}` "
                "WHERE create_time >= DATE_SUB(CURDATE(), INTERVAL 11 MONTH) "
                "GROUP BY m ORDER BY m"
            ) or []
            return {"xAxis": [r.get("m") for r in rows], "values": [int(r.get("c") or 0) for r in rows]}

        user_monthly = _monthly("user")
        status_rows = user_svc.run(
            "SELECT CASE state WHEN 1 THEN '正常' WHEN 2 THEN '冻结' ELSE '其他' END AS name, "
            "COUNT(*) AS value FROM `user` GROUP BY state"
        ) or []
        cat_rows = news_svc.run(
            "SELECT news_categories AS name, COUNT(*) AS value FROM news_information "
            "GROUP BY news_categories ORDER BY value DESC LIMIT 12"
        ) or []
        origin_rows = service_select("news_resources").run(
            "SELECT COALESCE(NULLIF(TRIM(origin), ''), '未知') AS name, COUNT(*) AS value "
            "FROM news_resources GROUP BY name ORDER BY value DESC LIMIT 10"
        ) or []
        # 按每日实际入库的新闻条数统计（news_resources），而非 crawl_run 运行次数
        crawl_rows = service_select("news_resources").run(
            "SELECT DATE(create_time) AS d, COUNT(*) AS c FROM news_resources "
            "WHERE create_time >= DATE_SUB(CURDATE(), INTERVAL 14 DAY) "
            "GROUP BY d ORDER BY d"
        ) or []
        read_rows = hits_svc.run(
            "SELECT DATE(create_time) AS d, COUNT(*) AS c FROM hits "
            "WHERE source_table = 'news_information' AND create_time >= DATE_SUB(CURDATE(), INTERVAL 14 DAY) "
            "GROUP BY d ORDER BY d"
        ) or []
        pref_rows = hits_svc.run(
            "SELECT ni.news_categories AS name, COUNT(*) AS value FROM hits h "
            "JOIN news_information ni ON ni.news_information_id = h.source_id "
            "WHERE h.source_table = 'news_information' "
            "GROUP BY ni.news_categories ORDER BY value DESC LIMIT 10"
        ) or []
        hot_rows = news_svc.run(
            "SELECT news_headlines AS name, hits AS value FROM news_information "
            "ORDER BY hits DESC LIMIT 10"
        ) or []
        crawl_summary = crawl_svc.run(
            "SELECT "
            "SUM(CASE WHEN status='success' THEN 1 ELSE 0 END) AS success, "
            "SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) AS failed, "
            "SUM(CASE WHEN status='running' THEN 1 ELSE 0 END) AS running "
            "FROM crawl_run"
        ) or [{}]
        cs = crawl_summary[0]
        return {
            "result": {
                "user_monthly": user_monthly,
                "user_status_ring": status_rows,
                "news_category_bar": {
                    "xAxis": [r.get("name") for r in cat_rows],
                    "values": [int(r.get("value") or 0) for r in cat_rows],
                },
                "news_origin_pie": origin_rows,
                "crawl_daily": {
                    "xAxis": [str(r.get("d")) for r in crawl_rows],
                    "values": [int(r.get("c") or 0) for r in crawl_rows],
                },
                "read_daily": {
                    "xAxis": [str(r.get("d")) for r in read_rows],
                    "values": [int(r.get("c") or 0) for r in read_rows],
                },
                "read_pref_bar": {
                    "xAxis": [r.get("name") for r in pref_rows],
                    "values": [int(r.get("value") or 0) for r in pref_rows],
                },
                "hot_news_rank": {
                    "xAxis": [r.get("name") for r in hot_rows],
                    "values": [int(r.get("value") or 0) for r in hot_rows],
                },
                "trend_highlights": {"growing_category": {}, "growing_article": {}},
                "crawl_run_summary": {
                    "success": int(cs.get("success") or 0),
                    "failed": int(cs.get("failed") or 0),
                    "running": int(cs.get("running") or 0),
                },
            }
        }

    def Add(self, ctx):
        
        ctx.body['password'] = ctx.body["password"]
        result = self.service.Add(ctx.body, self.config)
        if self.service.error:
            return {"error": self.service.error}
        return {"result": result}
