# -*- coding: utf-8 -*-

from app.core import controller
from app.core.controller import obj_update
from app.service import service_select
from app.news_html import strip_news_media_markup
from datetime import date, datetime
import math

controllerClass = getattr(controller, "Controller")

# 新闻资讯：发布、搜索、个性化推荐
class News_information(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./news_information/",
            # 注册API
            "get_api": ["recommend_advice"],
            # POST API 路由
            "post_api": [],
            # Service 名称
            "service": "news_information",
        }
        config_temp = config
        config_temp.update(config_init)
        super(News_information , self).__init__(config_temp)

    def _sanitize_news_row(self, row):
        if not row or not isinstance(row, dict):
            return
        if row.get("news_body") is not None:
            row["news_body"] = strip_news_media_markup(str(row["news_body"]))
        if row.get("news_description") is not None:
            row["news_description"] = strip_news_media_markup(str(row["news_description"]))

    def Add_before(self, ctx):
        body = getattr(ctx, "body", None)
        if isinstance(body, dict):
            if body.get("news_body") is not None:
                body["news_body"] = strip_news_media_markup(str(body["news_body"]))
            if body.get("news_description") is not None:
                body["news_description"] = strip_news_media_markup(str(body["news_description"]))
        return {"code": 0}

    def Set_before(self, ctx):
        body = getattr(ctx, "body", None)
        if isinstance(body, dict):
            if body.get("news_body") is not None:
                body["news_body"] = strip_news_media_markup(str(body["news_body"]))
            if body.get("news_description") is not None:
                body["news_description"] = strip_news_media_markup(str(body["news_description"]))
        return {"code": 0}

    def Get_obj(self, ctx):
        query = dict(ctx.query)
        config_plus = {}
        if "field" in query:
            field = query.pop("field")
            config_plus["field"] = field

        obj = self.service.Get_obj(query, obj_update(self.config, config_plus))
        if self.service.error:
            return {"error": self.service.error}
        if obj:
            self._sanitize_news_row(obj)
            self.interact_obj(ctx, obj)
        return {"result": {"obj": obj}}

    def _get_user_interest_weights(self, user_id):
        """汇总用户 hits/history/collect/praise，按新闻分类计算兴趣权重。"""
        service = self.service
        uid = str(int(user_id))
        sql = (
            "SELECT ni.news_categories AS cat, "
            "SUM(t.weight) AS total_weight "
            "FROM ("
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
            "GROUP BY ni.news_categories "
            "ORDER BY total_weight DESC"
        )
        rows = service.run(sql) or []
        result = {}
        for row in rows:
            cat = (row.get("cat") or "").strip()
            if cat:
                result[cat] = float(row.get("total_weight") or 0)
        return result

    def _pick_recommend_categories(self, cat_weight, max_cats=2):
        """选取用于推荐展示的分类（与 recommend_advice 文案逻辑一致，默认取权重最高的 2 类）。"""
        if not cat_weight:
            return []
        sorted_cats = sorted(cat_weight.items(), key=lambda x: x[1], reverse=True)
        total = sum(cat_weight.values()) or 1.0
        picked = []
        for name, weight in sorted_cats:
            if not name:
                continue
            if len(picked) >= max_cats:
                break
            if not picked or weight >= total * 0.12 or len(picked) < 2:
                picked.append(name)
        if not picked and sorted_cats:
            picked = [sorted_cats[0][0]]
        return picked[:max_cats]

    def _parse_news_datetime(self, row):
        value = row.get("publication_date") or row.get("create_time")
        if not value:
            return None
        if hasattr(value, "year"):
            if isinstance(value, date) and not isinstance(value, datetime):
                return datetime.combine(value, datetime.min.time())
            return value
        text = str(value).strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(text[:19], fmt)
            except Exception:
                continue
        return None

    def _freshness_boost(self, row):
        dt = self._parse_news_datetime(row)
        if not dt:
            return 1.0
        age_days = max(0.0, (datetime.now() - dt).total_seconds() / 86400.0)
        return 1.0 + 1.2 * math.exp(-age_days / 7.0)

    def _resolve_hits_list_pool(self, query):
        """解析推荐列表拉取规模；支持首页 top_k 与列表页 page/size 分页。"""
        page = int(query.get("page", 0) or 0)
        size = int(query.get("size", 0) or 0)
        top_k = int(query.get("top_k", 0) or 0)
        # 列表页分页时先对完整候选池排序，再按 page/size 切片，不能用 page*size 当池子上限
        max_pool = 500
        if top_k > 0 and page <= 0 and size <= 0:
            return 0, 0, max(5, min(max_pool, top_k))
        if page > 0 and size > 0:
            size = max(1, min(24, size))
            page = max(1, page)
            return page, size, max_pool
        return 0, 0, max(5, min(max_pool, top_k or 12))

    def _format_hits_list_response(self, full_list, page, size):
        if page > 0 and size > 0:
            start = (page - 1) * size
            return {"result": {"list": full_list[start:start + size], "count": len(full_list)}}
        return {"result": {"list": full_list, "count": len(full_list)}}

    def _fallback_hot_list(self, pool_limit, page=0, size=0):
        sql = (
            "SELECT * FROM news_information "
            "ORDER BY `recommend` DESC, `hits` DESC, `create_time` DESC "
            "LIMIT 0," + str(pool_limit)
        )
        lst = self.service.run(sql) or []

        def to_f(v):
            try:
                return float(v or 0)
            except Exception:
                return 0.0

        for row in lst:
            self._sanitize_news_row(row)
            rdb = to_f(row.get("recommend"))
            if rdb > 0:
                row["recommend_display"] = round(rdb, 2)
            else:
                h = to_f(row.get("hits"))
                c = to_f(row.get("collect_len"))
                p = to_f(row.get("praise_len"))
                alt = h * 0.15 + c * 2.0 + p * 1.2 + 0.12
                row["recommend_display"] = round(max(alt, 0.12), 2)

        return self._format_hits_list_response(lst, page, size)

    # 个性化推荐：基于用户行为分类权重 + 热度 + 时效性排序
    def Get_hits_list(self, ctx):
        query = dict(ctx.query)

        user_id = query.get("user_id", "")
        if user_id == "":
            user_id = self._get_user_id_from_ctx(ctx)

        page, size, pool_limit = self._resolve_hits_list_pool(query)

        if not user_id:
            return self._format_hits_list_response([], page, size)

        user_id = str(int(user_id))

        cat_weight = self._get_user_interest_weights(user_id)
        picked_cats = self._pick_recommend_categories(cat_weight, max_cats=2)
        if not picked_cats:
            return self._format_hits_list_response([], page, size)

        picked_weight = {c: cat_weight.get(c, 0.0) for c in picked_cats}
        safe_cats = [c.replace("'", "''") for c in picked_cats if c]
        if not safe_cats:
            return self._format_hits_list_response([], page, size)

        in_sql = ",".join(["'%s'" % c for c in safe_cats])
        candidate_sql = (
            "SELECT * FROM news_information "
            "WHERE news_categories IN (" + in_sql + ") "
            "ORDER BY create_time DESC"
        )
        candidates = self.service.run(candidate_sql) or []

        def to_float(v):
            try:
                return float(v or 0)
            except Exception:
                return 0.0

        def score(row):
            cat = (row.get("news_categories") or "").strip()
            w = picked_weight.get(cat, 0.0)
            hits = to_float(row.get("hits"))
            recommend = to_float(row.get("recommend"))
            collect_len = to_float(row.get("collect_len"))
            praise_len = to_float(row.get("praise_len"))
            freshness = self._freshness_boost(row)
            return (w * 8.0 + hits * 0.8 + recommend * 1.2 + collect_len * 1.5 + praise_len) * freshness

        sorted_candidates = sorted(candidates, key=score, reverse=True)
        result_list = [
            row for row in sorted_candidates[:pool_limit]
            if (row.get("news_categories") or "").strip() in picked_cats
        ]

        for row in result_list:
            self._sanitize_news_row(row)
            rdb = to_float(row.get("recommend"))
            s = score(row)
            if rdb > 0:
                row["recommend_display"] = round(rdb, 2)
            else:
                h = to_float(row.get("hits"))
                row["recommend_display"] = round(
                    s if s > 0.001 else max(h * 0.08 + 0.06, 0.1),
                    2,
                )

        return self._format_hits_list_response(result_list, page, size)

    def _build_recommend_advice(self, user_id):
        """根据用户兴趣分类权重生成推荐建议文案。"""
        uid = str(int(user_id))
        cat_weight = self._get_user_interest_weights(uid)
        if not cat_weight:
            return {
                "message": "基于以上数据，该用户暂无行为记录，建议优先推荐全局热门资讯",
                "categories": [],
            }

        picked = self._pick_recommend_categories(cat_weight, max_cats=3)

        if len(picked) == 1:
            cat_text = picked[0]
        else:
            cat_text = "、".join(picked)

        return {
            "message": "基于以上数据，建议对该用户推荐%s类的新闻" % cat_text,
            "categories": picked,
            "cat_text": cat_text,
        }

    def Recommend_advice(self, ctx):
        """推荐效果分析：返回对该用户的分类推荐建议。"""
        query = dict(ctx.query)
        user_id = query.get("user_id", "")
        if user_id == "":
            user_id = self._get_user_id_from_ctx(ctx)
        if not user_id:
            return {
                "result": {
                    "message": "请先选择用户后再查看推荐建议",
                    "categories": [],
                }
            }
        return {"result": self._build_recommend_advice(user_id)}

    def _get_user_id_from_ctx(self, ctx):
        # 兼容：前端如果没传 user_id，我们从 x-auth-token 对应的 session 反查
        try:
            q_user_id = ctx.query.get("user_id", "")
            if q_user_id:
                return q_user_id
        except Exception:
            pass

        try:
            token = ctx.request.headers.get("x-auth-token", "") if hasattr(ctx, "request") else ""
            if not token:
                return ""
            # AuthMiddleware 会把 request.session[token] = user_id
            s = getattr(ctx.request, "session", None)
            if not s:
                return ""
            uid = s.get(token)
            return uid or ""
        except Exception:
            return ""

    def Get_list(self, ctx):
        """
        兼容前端搜索：
        - 前端会用 get_list + news_headlines/news_categories 来做关键词搜索
        - 这里对这两种“关键词搜索”场景进行个性化打分排序，并返回 matched_fields 方便前端高亮
        """
        query = dict(ctx.query)

        # 非关键词搜索：保持原有通用逻辑
        is_keyword_search = ("news_headlines" in query) or ("news_categories" in query)
        if not is_keyword_search:
            res = super().Get_list(ctx)
            lst = (res.get("result") or {}).get("list")
            if isinstance(lst, list):
                for row in lst:
                    self._sanitize_news_row(row)
            return res

        # 关键词（兼容：可能来自 news_headlines，也可能来自 news_categories）
        keyword = query.get("news_headlines") or query.get("news_categories") or ""
        keyword = (keyword or "").strip()
        if not keyword:
            return {"result": {"list": [], "count": 0}}

        # page/size
        try:
            page = int(query.get("page") or 1)
        except Exception:
            page = 1
        try:
            size = int(query.get("size") or 10)
        except Exception:
            size = 10
        if page <= 0:
            page = 1
        if size <= 0:
            size = 10

        user_id = query.get("user_id", "")
        if not user_id:
            user_id = self._get_user_id_from_ctx(ctx)
        if user_id:
            user_id = str(int(user_id))
        else:
            user_id = ""

        # 取候选：news_headlines/news_categories/news_description/news_body 任意字段包含关键词即可
        # 注意：这里用 LIMIT 控制候选规模，避免表太大导致排序慢
        service = self.service
        kw_sql = keyword.replace("'", "''")
        where_sql = (
            "("
            "news_headlines LIKE '%" + kw_sql + "%' "
            "OR news_categories LIKE '%" + kw_sql + "%' "
            "OR news_description LIKE '%" + kw_sql + "%' "
            "OR news_body LIKE '%" + kw_sql + "%'"
            ")"
        )

        count_sql = "SELECT COUNT(*) AS cnt FROM news_information WHERE " + where_sql
        count_res = service.run(count_sql) or []
        total = int(count_res[0].get("cnt") or 0) if count_res else 0

        candidates_sql = (
            "SELECT * FROM news_information WHERE " + where_sql + " ORDER BY create_time DESC LIMIT 0, 1000"
        )
        candidates = service.run(candidates_sql) or []

        # 用户兴趣分类热度（如果有用户）
        cat_weight = {}
        if user_id:
            cat_weight = self._get_user_interest_weights(user_id)

        # 打分：关键词匹配度（主） + 用户兴趣分类（辅）
        kw_tokens = [t for t in keyword.split() if t] or [keyword]
        kw_tokens = [t.lower() for t in kw_tokens if t]

        def contains(text, token):
            if text is None:
                return False
            return token in str(text).lower()

        def count_token(text, token):
            if not text:
                return 0
            s = str(text).lower()
            return s.count(token)

        def compute_score(row):
            headlines = row.get("news_headlines") or ""
            categories = row.get("news_categories") or ""
            description = row.get("news_description") or ""
            body = row.get("news_body") or ""

            matched = 0
            for t in kw_tokens:
                # headlines 权重最高
                if contains(headlines, t):
                    matched += 10 * count_token(headlines, t)
                if contains(categories, t):
                    matched += 6 * count_token(categories, t)
                if contains(description, t):
                    matched += 3 * count_token(description, t)
                if contains(body, t):
                    matched += 1 * count_token(body, t)

            # 用户兴趣加权
            cat = (row.get("news_categories") or "").strip()
            w = cat_weight.get(cat, 0.0)

            # hits 字段作为二级信号（全局热度）
            try:
                hits = float(row.get("hits") or 0)
            except Exception:
                hits = 0.0
            try:
                recommend = float(row.get("recommend") or 0)
            except Exception:
                recommend = 0.0

            return (matched + w * 5.0 + hits * 0.02 + recommend * 0.1) * self._freshness_boost(row)

        # 组装 matched_fields 供前端高亮展示
        def build_matched_fields(row):
            fields = []
            headlines = row.get("news_headlines") or ""
            categories = row.get("news_categories") or ""
            description = row.get("news_description") or ""
            body = row.get("news_body") or ""

            # 如果任意 token 命中就返回对应字段的 value
            if any(contains(headlines, t) for t in kw_tokens):
                fields.append({"field": "news_headlines", "value": headlines})
            if any(contains(categories, t) for t in kw_tokens):
                fields.append({"field": "news_categories", "value": categories})
            if any(contains(description, t) for t in kw_tokens):
                fields.append({"field": "news_description", "value": description})
            if any(contains(body, t) for t in kw_tokens):
                fields.append({"field": "news_body", "value": body})
            return fields

        sorted_candidates = sorted(candidates, key=compute_score, reverse=True)

        # 分页切片
        start = (page - 1) * size
        end = start + size
        page_list = sorted_candidates[start:end]

        for row in page_list:
            self._sanitize_news_row(row)
            # 前端列表组件优先 display_title，其次 title
            row["display_title"] = row.get("news_headlines") or ""
            row["matched_fields"] = build_matched_fields(row)

        return {"result": {"list": page_list, "count": total}}

