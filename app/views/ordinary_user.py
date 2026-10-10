# -*- coding: utf-8 -*-
"""普通用户扩展资料：列表查询与 user 表资料同步。"""

from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")


def _escape_sql_like(value):
    return (value or "").replace("\\", "\\\\").replace("'", "''")


def _sync_missing_ordinary_profiles():
    """为仅有 user 记录、缺少 ordinary_user 扩展行的普通用户补建资料。"""
    user_service = service_select("user")
    ou_service = service_select("ordinary_user")
    rows = user_service.run(
        "SELECT u.user_id, u.phone FROM `user` u "
        "WHERE u.user_group = '普通用户' AND u.user_id NOT IN "
        "(SELECT user_id FROM `ordinary_user`)"
    ) or []
    for row in rows:
        phone = str(row.get("phone") or "").strip()
        ou_service.Add(
            {
                "users_mobile_phone": phone[:11] if phone else "",
                "examine_state": "已通过",
                "user_id": row["user_id"],
                "create_by": 1,
            }
        )


class Ordinary_user(controllerClass):
    def __init__(self, config=None):
        if config is None:
            config = {}
        config_init = {
            "tpl": "./ordinary_user/",
            "get_api": [],
            "post_api": [],
            "service": "ordinary_user",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Ordinary_user, self).__init__(config_temp)

    def Get_list(self, ctx):
        _sync_missing_ordinary_profiles()
        qd = ctx.query
        try:
            kw = (
                str(qd.get("nickname_or_phone") or qd.get("users_mobile_phone") or "")
                .strip()
            )
            for key in ("nickname_or_phone", "users_mobile_phone"):
                if key in qd:
                    del qd[key]
            if kw:
                esc = _escape_sql_like(kw)
                clause = (
                    "("
                    f"`user_name` LIKE '%{esc}%' OR `users_mobile_phone` LIKE '%{esc}%' OR "
                    "`user_id` IN (SELECT `user_id` FROM `user` WHERE `user_group` = '普通用户' "
                    f"AND (`nickname` LIKE '%{esc}%' OR `phone` LIKE '%{esc}%' OR `username` LIKE '%{esc}%'))"
                    ")"
                )
                prev = str(qd.get("sqlwhere") or "").strip()
                if prev:
                    qd["sqlwhere"] = f"({prev}) AND {clause}"
                else:
                    qd["sqlwhere"] = clause
        except Exception:
            pass
        dedupe = (
            "`ordinary_user_id` IN (SELECT MAX(`ordinary_user_id`) FROM `ordinary_user` GROUP BY `user_id`)"
        )
        prev_sw = str(qd.get("sqlwhere") or "").strip()
        if prev_sw:
            qd["sqlwhere"] = f"({prev_sw}) AND ({dedupe})"
        else:
            qd["sqlwhere"] = dedupe
        return super(Ordinary_user, self).Get_list(ctx)
