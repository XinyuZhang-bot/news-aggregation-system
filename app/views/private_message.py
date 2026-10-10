# -*- coding: utf-8 -*-

from app.core import controller
from app.service import service_select
from app.views.user import tokenGetUserId


controllerClass = getattr(controller, "Controller")


def _escape_sql(value):
    return str(value or "").replace("'", "''")


def _conversation_key(user_a, user_b):
    ua = int(user_a)
    ub = int(user_b)
    left = min(ua, ub)
    right = max(ua, ub)
    return "%s_%s" % (left, right)


class Private_message(controllerClass):
    def __init__(self, config={}):
        config_init = {
            "tpl": "./private_message/",
            "service": "private_message",
            "get_api": ["conversation_list", "conversation_detail"],
            "post_api": ["send_message", "mark_read"],
        }
        config_temp = config
        config_temp.update(config_init)
        super(Private_message, self).__init__(config_temp)

    def _current_user_id(self, ctx):
        request = getattr(ctx, "request", None)
        if request is None:
            return 0
        headers = request.headers
        token = headers.get("x-auth-token") or headers.get("X-Auth-Token")
        if not token:
            return 0
        try:
            return int(tokenGetUserId(token, request) or 0)
        except Exception:
            return 0

    def _follow_allowed(self, sender_id, receiver_id):
        follow_service = service_select("follow")
        row = follow_service.Get_obj(
            {"follower_id": int(sender_id), "followed_id": int(receiver_id)},
            {"like": False},
        )
        return row is not None

    def _user_brief(self, user_id):
        user_service = service_select("user")
        user = user_service.Get_obj({"user_id": int(user_id)}, {"like": False}) or {}
        return {
            "user_id": int(user.get("user_id") or 0),
            "nickname": user.get("nickname") or user.get("username") or ("用户" + str(user_id)),
            "avatar": user.get("avatar") or "",
            "username": user.get("username") or "",
        }

    def Conversation_list(self, ctx):
        current_user_id = self._current_user_id(ctx)
        if not current_user_id:
            return {"error": {"code": 50000, "message": "账户未登录"}}

        service = self.service
        sql = (
            "SELECT * FROM `private_message` "
            "WHERE `sender_id` = " + str(current_user_id) + " OR `receiver_id` = " + str(current_user_id) + " "
            "ORDER BY `create_time` DESC, `private_message_id` DESC LIMIT 0, 500"
        )
        rows = service.run(sql) or []
        conv_map = {}
        unread_map = {}
        for row in rows:
            key = row.get("conversation_key") or _conversation_key(row.get("sender_id") or 0, row.get("receiver_id") or 0)
            sender_id = int(row.get("sender_id") or 0)
            receiver_id = int(row.get("receiver_id") or 0)
            peer_id = receiver_id if sender_id == current_user_id else sender_id
            if key not in conv_map:
                conv_map[key] = {
                    "conversation_key": key,
                    "peer_id": peer_id,
                    "last_message": row.get("content") or "",
                    "last_time": row.get("create_time"),
                    "last_sender_id": sender_id,
                }
            if receiver_id == current_user_id and int(row.get("is_read") or 0) == 0:
                unread_map[key] = unread_map.get(key, 0) + 1

        result = []
        for key, item in conv_map.items():
            peer = self._user_brief(item["peer_id"])
            item["peer_nickname"] = peer["nickname"]
            item["peer_avatar"] = peer["avatar"]
            item["peer_username"] = peer["username"]
            item["unread_count"] = unread_map.get(key, 0)
            result.append(item)
        result.sort(key=lambda x: str(x.get("last_time") or ""), reverse=True)
        return {"result": {"list": result, "count": len(result)}}

    def Conversation_detail(self, ctx):
        current_user_id = self._current_user_id(ctx)
        if not current_user_id:
            return {"error": {"code": 50000, "message": "账户未登录"}}

        query = dict(ctx.query)
        peer_id = int(query.get("user_id") or 0)
        if not peer_id:
            return {"error": {"code": 70000, "message": "缺少聊天对象"}}
        if peer_id == current_user_id:
            return {"error": {"code": 70000, "message": "不能与自己聊天"}}

        service = self.service
        sql = (
            "SELECT * FROM `private_message` WHERE "
            "((`sender_id` = " + str(current_user_id) + " AND `receiver_id` = " + str(peer_id) + ") "
            "OR (`sender_id` = " + str(peer_id) + " AND `receiver_id` = " + str(current_user_id) + ")) "
            "ORDER BY `create_time` ASC, `private_message_id` ASC LIMIT 0, 300"
        )
        rows = service.run(sql) or []
        peer = self._user_brief(peer_id)
        return {
            "result": {
                "list": rows,
                "count": len(rows),
                "peer": peer,
                "conversation_key": _conversation_key(current_user_id, peer_id),
            }
        }

    def Send_message(self, ctx):
        current_user_id = self._current_user_id(ctx)
        if not current_user_id:
            return {"error": {"code": 50000, "message": "账户未登录"}}

        body = ctx.body or {}
        receiver_id = int(body.get("receiver_id") or 0)
        content = str(body.get("content") or "").strip()
        if not receiver_id:
            return {"error": {"code": 70000, "message": "缺少接收用户"}}
        if receiver_id == current_user_id:
            return {"error": {"code": 70000, "message": "不能给自己发送私信"}}
        if not content:
            return {"error": {"code": 70000, "message": "私信内容不能为空"}}
        if len(content) > 1000:
            return {"error": {"code": 70000, "message": "私信内容不能超过1000字"}}
        if not self._follow_allowed(current_user_id, receiver_id):
            return {"error": {"code": 70000, "message": "请先关注对方后再发送私信"}}

        payload = {
            "sender_id": current_user_id,
            "receiver_id": receiver_id,
            "conversation_key": _conversation_key(current_user_id, receiver_id),
            "content": content,
            "is_read": 0,
        }
        result = self.service.Add(payload, self.config)
        if not result:
            return {"error": {"code": 70000, "message": "私信发送失败"}}
        return {"result": {"bl": True, "message": "发送成功"}}

    def Mark_read(self, ctx):
        current_user_id = self._current_user_id(ctx)
        if not current_user_id:
            return {"error": {"code": 50000, "message": "账户未登录"}}

        body = ctx.body or {}
        peer_id = int(body.get("user_id") or 0)
        if not peer_id:
            return {"error": {"code": 70000, "message": "缺少聊天对象"}}
        sql = (
            "UPDATE `private_message` SET `is_read` = 1 "
            "WHERE `sender_id` = " + str(peer_id) + " "
            "AND `receiver_id` = " + str(current_user_id) + " "
            "AND `is_read` = 0"
        )
        result = self.service.run(sql)
        if self.service.error:
            return {"error": self.service.error}
        return {"result": {"bl": bool(result)}}
