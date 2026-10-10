# -*- coding: utf-8 -*-
"""编辑人员扩展资料：列表查询与 user 表资料同步。"""

from app.core import controller
from app.service import service_select

controllerClass = getattr(controller, "Controller")


def _escape_sql_like(value):
    return (value or "").replace("\\", "\\\\").replace("'", "''")


def _sync_missing_compileors_profiles():
    """为仅有 user 记录、缺少 compileors 扩展行的编辑人员补建资料。"""
    user_service = service_select("user")
    cp_service = service_select("compileors")
    rows = user_service.run(
        "SELECT u.user_id, u.phone FROM `user` u "
        "WHERE u.user_group = '编辑人员' AND u.user_id NOT IN "
        "(SELECT user_id FROM `compileors`)"
    ) or []
    for row in rows:
        phone = str(row.get("phone") or "").strip()
        cp_service.Add(
            {
                "users_phone": phone[:11] if phone else "",
                "examine_state": "已通过",
                "user_id": row["user_id"],
                "create_by": 1,
            }
        )


class Compileors(controllerClass):
    def __init__(self, config=None):
        if config is None:
            config = {}
        config_init = {
            "tpl": "./compileors/",
            "get_api": [],
            "post_api": [],
            "service": "compileors",
        }
        config_temp = config
        config_temp.update(config_init)
        super(Compileors, self).__init__(config_temp)

    def Get_list(self, ctx):
        _sync_missing_compileors_profiles()
        try:
            qd = ctx.query
            kw = (
                str(qd.get("nickname_or_phone") or qd.get("users_phone") or "")
                .strip()
            )
            for key in ("nickname_or_phone", "users_phone"):
                if key in qd:
                    del qd[key]
            if kw:
                esc = _escape_sql_like(kw)
                clause = (
                    "("
                    f"`user_name` LIKE '%{esc}%' OR `users_phone` LIKE '%{esc}%' OR "
                    "`user_id` IN (SELECT `user_id` FROM `user` WHERE `user_group` = '编辑人员' "
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
        return super(Compileors, self).Get_list(ctx)
