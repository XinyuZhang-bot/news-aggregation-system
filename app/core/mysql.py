# -*- coding: utf-8 -*-
"""
MySQL 数据访问层：封装原生 SQL 的增删改查，供 Service 子类调用。

使用 Django connection + pandas 读写；不依赖 Django ORM Models。
"""
import json
from django.db import connection
import numpy as np
import pandas as pd
import datetime
import time


# 合并多个配置字典
def obj_update(*config):
    config_temp = {}
    for o in config:
        config_temp.update(o)
    return config_temp


# 帮助类：重写json类
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if pd.isna(obj):
                return None
        except:
            pass
        # 遇到日期特殊处理
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")
        # 遇到nparray特殊处理
        elif isinstance(
                obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray, )):
            return obj.tolist()
        else:
            return json.JSONEncoder.default(self, obj)


# 帮助类：mysql请求池
class MysqlPool:
    def _is_lock_retryable(self, err) -> bool:
        msg = str(err).lower()
        return (
            "lock wait timeout exceeded" in msg
            or "deadlock found" in msg
            or "(1205" in msg
            or "(1213" in msg
        )

    def run(self, sql, values=None):
        result = None
        if sql.find("SELECT") != -1:
            df = pd.read_sql(sql, connection)
            # 获取列名
            column_list = list(df.columns)
            df = df.replace({np.nan: None})
            df1 = list(np.array(df))
            lst = []
            for row in df1:
                # 循环每一行数据，组装成一个字典，然后得到字典的列表
                lst.append(dict(zip(column_list, row.tolist())))
            # 导入json,将列表转为json字符串
            # son.dumps序列化时候对中文默认使用的ascii编码，想要输出真正的中文需要指定ensure_ascii=False
            str1 = json.dumps(lst, cls=MyEncoder, ensure_ascii=False)
            # 再转回dict
            result = json.loads(str1)
        else:
            result = False
            retry = 0
            last_err = None
            while retry < 4:
                cur = None
                try:
                    cur = connection.cursor()
                    cur.execute(sql)
                    result = True
                    last_err = None
                    break
                except Exception as e:
                    last_err = e
                    if self._is_lock_retryable(e) and retry < 3:
                        retry += 1
                        # 锁冲突常见于爬虫批量写库与后台手动删改并发，短暂等待后重试。
                        time.sleep(0.35 * retry)
                        continue
                    raise
                finally:
                    try:
                        if cur is not None:
                            cur.close()
                    except Exception:
                        pass
            if last_err is not None:
                raise last_err
        return result

    def escapeId(self, str_1):
        """ 作用：将`去掉 """
        str_1 = str(str_1)
        return "`" + str_1.replace(r"/`/", "") + "`"

    def escape(self, str_1):
        """ 作用：将前后的'去掉 """
        str_1 = str(str_1)
        if str_1.upper() == 'TRUE' or str_1.upper() == 'FALSE':
            return str_1.replace(r"/'/", r"\'")
        else:
            return "'" + str_1.replace(r"/'/", r"\'").replace("'", "''") + "'"

    def toWhere(self, queryDict={}, like=True):
        where = ""
        like = str(like).lower() in ['true', '1', 'yes']
        if like:
            for k in queryDict:
                val = queryDict[k]
                if(k.endswith("_min")):
                    where += " and `" + k.replace("_min", "") + "` >= " + self.escape(str(val))
                elif(k.endswith("_max")):
                    where += " and `" + k.replace("_max", "") + "` <= " + self.escape(str(val))
                elif isinstance(val, str):
                    where += (" and `" + k + "` LIKE '%" +
                              self.escape(val).strip("'") + "%'")
                elif isinstance(val, int):
                    where += " and `" + k + "`=" + str(val)
                else:
                    where += " and `" + k + "`=" + str(val)

        else:
            for k in queryDict:
                val = queryDict[k]
                if(k.endswith("_min")):
                    where += " and `" + k.replace("_min", "") + "` >= " + self.escape(str(val))
                elif(k.endswith("_max")):
                    where += " and `" + k.replace("_max", "") + "` <= " + self.escape(str(val))
                elif isinstance(val, str):
                    where += (" and `" + k + "` = '" +
                              self.escape(val).strip("'") + "'")
                elif isinstance(val, int):
                    where += " and `" + k + "`=" + str(val)
                else:
                    where += " and `" + k + "`=" + str(val)
        return where.replace(" and ", "", 1)

    def toOrWhere(self, queryDict={}, like=True):
        where = ""
        if like:
            for k in queryDict:
                val = queryDict[k]
                # type(val) == "<type 'str'>"
                if isinstance(val, str):
                    where += (" or `" + k + "` LIKE '%" +
                              self.escape(val).strip("'") + "%'")
                elif isinstance(val, int):
                    where += " or `" + k + "`=" + str(val)
                else:
                    where += " or `" + k + "`=" + str(val)

        else:
            for k in queryDict:
                where += " or " + self.escapeId(k) + "=" + self.escape(
                    queryDict[k])
        return where.replace(" or ", "", 1)

    def toSet(self, body):
        setData = ""
        for k in body:
            v = body[k]
            setData += ", `" + k + "`=" + self.escape(v)
        return setData.replace(", ", "", 1)

    def toAddSql(self, body, config):
        if "table" in config:
            table = config["table"]
        key = ""
        val = ""
        for k in body:
            key += "," + self.escapeId(k)
            val += "," + self.escape(body[k])
        sql = "INSERT INTO `{0}` ({1}) VALUES ({2});"
        return (sql.replace("{0}", table).replace("{1}", key.replace(
            ",", "", 1)).replace("{2}", val.replace(",", "", 1)))

    def toDelSql(self, query={}, config={}):
        if "table" in config:
            table = config["table"]
        where = self.toWhere(query, False)
        sql = "DELETE FROM `{0}` WHERE {1};"
        return sql.replace("{0}", table).replace("{1}", where)

    def toSetSql(self, query, body, config):
        if "table" in config:
            table = config["table"]
        where = self.toWhere(query, False)
        setData = self.toSet(body)
        sql = "UPDATE `{0}` SET {1} WHERE {2};"
        return sql.replace("{0}",
                           table).replace("{1}",
                                          setData).replace("{2}", where)

    def toGetSql(self, query={}, config={}):
        like = True
        where = groupby = orderby = size = page = sqlwhere = ""
        sql = "SELECT {1} FROM `{0}`"
        if "table" in config:
            table = config["table"]
        if "orderby" in config:
            orderby = config["orderby"]
        if "field" in config:
            field = config["field"]
        else:
            field = "*"
        if "page" in config:
            page = int(config["page"])
        if "size" in config:
            size = int(config["size"])
        if "like" in query:
            like = query["like"]
            del query["like"]
        elif "like" in config:
            like = config["like"]
        if "groupby" in config:
            groupby = config["groupby"]
        if "sqlwhere" in config:
            sqlwhere = config["sqlwhere"]
        where = self.toWhere(query, like)
        if where:
            sql += " WHERE " + where
        if sqlwhere:
            if where:
                sql += " AND " + sqlwhere.replace(r"/;/", "")
            else:
                sql += " WHERE " + sqlwhere.replace(r"/;/", "")
        if groupby:
            sql += " GROUP BY " + groupby.replace(r"/;/", "")
        if orderby:
            sql += " ORDER BY " + orderby.replace(r"/;/", "")

        sql = sql.replace("{0}", table).replace("{1}", field)
        if size and page:
            start = size * (page - 1)
            sql += " limit " + str(start) + "," + str(size)
        return sql

    def toCountSql(self, query={}, config={}):
        groupby = sqlwhere = ""
        like = True
        if "table" in config:
            table = config["table"]
        if "groupby" in config:
            groupby = config["groupby"]
        if "sqlwhere" in config:
            sqlwhere = config["sqlwhere"]
        if "like" in query:
            like = query["like"]
            del query["like"]
        elif "like" in config:
            like = config["like"]

        sql = "SELECT count(*) count FROM `" + table + "`"
        where = self.toWhere(query, like)
        if where:
            sql += " WHERE " + where
        if sqlwhere:
            if where:
                sql += " AND " + sqlwhere.replace(r"/;/", "")
            else:
                sql += " WHERE " + sqlwhere.replace(r"/;/", "")
        # 用户组
        if groupby:
            sql = sql.replace("count(", groupby + ",count(")
            if "groupby" in query:
                query.pop("groupby")
            sql += " GROUP BY " + groupby
        return sql

    def toSumSql(self, query={}, config={}):
        groupby = sqlwhere = ""
        where = ""
        if "table" in config:
            table = config["table"]
        if "field" in config:
            field = config["field"]
        if "groupby" in config:
            groupby = config["groupby"]
        if "sqlwhere" in config:
            sqlwhere = config["sqlwhere"]
        if "sqlwhere" in query:
            sqlwhere = query["sqlwhere"]
            del query["sqlwhere"]
        sql = "SELECT sum(" + self.escapeId(
            field) + ") sum FROM `" + table + "`"
        where = self.toWhere(query)
        if where:
            sql += " WHERE " + where
        if sqlwhere:
            if where:
                sql += " AND " + sqlwhere.replace(r"/;/", "")
            else:
                sql += " WHERE " + sqlwhere.replace(r"/;/", "")
        if groupby:
            sql = sql.replace("sum(", groupby + ",sum(")
            if "groupby" in query:
                query.pop("groupby")
            sql += " GROUP BY" + self.escapeId(groupby)

        return sql

    def toAvgSql(self, query={}, config={}):
        groupby = sqlwhere = ""
        if "table" in config:
            table = config["table"]
        if "field" in config:
            field = config["field"]
        if "groupby" in config:
            groupby = config["groupby"]
        if "sqlwhere" in config:
            sqlwhere = config["sqlwhere"]
        sql = "SELECT avg(" + self.escapeId(
            field) + ") avg FROM `" + table + "`"
        where = self.toWhere(query)
        if where:
            sql += " WHERE " + where
        if sqlwhere:
            if where:
                sql += " AND " + sqlwhere.replace(r"/;/", "")
            else:
                sql += " WHERE " + sqlwhere.replace(r"/;/", "")
        if groupby:
            sql = sql.replace("avg(", groupby + ",avg(")
            if "groupby" in query:
                query.pop("groupby")
            sql += " GROUP BY" + self.escapeId(groupby)
        return sql

    # 计算日期
    def toDateComput(self, query={}, config={}):
        date_key = "create_time"
        method = "count"
        field = "*"
        size = 0
        format_t = r"%Y-%m-%d"
        if "date_key" in config:
            date_key = config["date_key"]
        if "method" in config:
            method = config["method"]
        if "field" in config:
            field = config["field"]
        if "size" in config:
            size = config["size"]
        if "format" in config:
            format_t = config["format"]
        if "table" in config:
            table = config["table"]
        sql = ("SELECT DATE_FORMAT(`" + date_key + "`, '" + format_t +
               "') `date`, " + method + "(" + field + ") " + method +
               " FROM `" + table + "`")
        where = self.toWhere(query)
        if where:
            sql += " WHERE " + where
        sql += " GROUP BY `date` ORDER BY `date` desc"
        if size:
            sql += " limit 0," + str(size)
        return sql


mysqlPool = MysqlPool()


# 服务器父类
class Service:
    error = {"code": 0, "message": "", "sql": ""}

    def __init__(self, config):
        config_temp = {
            "table": "",
            "page": 1,
            "size": 30,
        }
        self.config = obj_update(config_temp, config)

    def run(self, sql, values=None):
        ret = None
        try:
            self.error = None
            ret = mysqlPool.run(sql, values=None)
        except Exception as e:
            self.error = {"code": 0, "message": str(e), "sql": sql}
            return False
        else:
            if sql.find("SELECT") != -1:
                if ret is None:
                    ret = []
            return ret

    def Add(self, body={}, config={}):
        sql = mysqlPool.toAddSql(body, obj_update(self.config, config)).replace('%', '%%')
        ret = self.run(sql)
        return ret

    def Del(self, query={}, config={}):
        sql = mysqlPool.toDelSql(query, obj_update(self.config, config))
        ret = self.run(sql)
        return ret

    def Set(self, query={}, body={}, config={}):
        sql = mysqlPool.toSetSql(query, body, obj_update(self.config, config)).replace('%', '%%')
        ret = self.run(sql)
        return ret

    def Get_list(self, query={}, config={}):
        sql = mysqlPool.toGetSql(query, obj_update(self.config, config))
        return self.run(sql)

    def Get_obj(self, query={}, config={}):
        sql = mysqlPool.toGetSql(query, obj_update(self.config, config))
        arr = self.run(sql)
        if arr and len(arr) > 0:
            return arr[0]
        return None

    def Count(self, query={}, config={}):
        sql = mysqlPool.toCountSql(query, obj_update(self.config, config))
        arr = self.run(sql)
        if arr and len(arr) > 0:
            return arr[0]["count"] or 0
        return 0

    def Sum(self, query={}, config={}):
        sql = mysqlPool.toSumSql(query, obj_update(self.config, config))
        arr = self.run(sql)
        if arr and len(arr) > 0:
            return arr[0]["sum"] or 0
        return 0

    def Avg(self, query={}, config={}):
        sql = mysqlPool.toAvgSql(query, obj_update(self.config, config))
        arr = self.run(sql)
        if arr and len(arr) > 0:
            return arr[0]["avg"] or 0
        return 0

    def Count_group(self, query={}, config={}):
        sql = mysqlPool.toCountSql(query, obj_update(self.config, config))
        return self.run(sql)

    def Sum_group(self, query={}, config={}):
        sql = mysqlPool.toSumSql(query, obj_update(self.config, config))
        return self.run(sql)

    def Bar_group(self, query={}, config={}):
        sum_list = ''
        where = ''
        for o in config['field'].split(','):
            sum_list += ",sum(" + o + ")"
        if "like" in config:
            like = config["like"]
            where = " WHERE " + self.toWhere(query, like)
        if "sqlwhere" in config:
            sqlwhere = config["sqlwhere"]
            if where and where != '':
                where += " AND " + sqlwhere.replace(r"/;/", "")
            else:
                where += " WHERE " + sqlwhere.replace(r"/;/", "")
        sql = "SELECT " + config['groupby'] + sum_list + " FROM " + self.config["table"] + where + " GROUP BY " + config['groupby']
        return self.run(sql)

    def Avg_group(self, query={}, config={}):
        sql = mysqlPool.toAvgSql(query, obj_update(self.config, config))
        return self.run(sql)

    def Prev(self, key, value):
        sql = ("SELECT * FROM `" + self.config["table"] + "` WHERE `" +
               str(key) + "`<" + str(value) + " ORDER BY `" + str(key) +
               "` DESC limit 0,10;")
        return self.run(sql)

    def Next(self, key, value):
        sql = ("SELECT * FROM `" + self.config["table"] + "` WHERE `" +
               str(key) + "`>" + str(value) + " limit 0,10;")
        return self.run(sql)

    def date_comput(self, query={}, config={}):
        sql = mysqlPool.toDateComput(query, obj_update(query, {"table": self.config["table"]}), config)
        return self.run(sql)

    # 导入
    def Import_db(self, data, config):
        pass

    # 导出
    def Export_db(self, query={}, config={}):
        # 数据库语言
        sql = mysqlPool.toGetSql(query, obj_update(self.config, config))
        df = pd.read_sql(sql, connection)
        # 获取列名
        column_list = list(np.array(df.columns))
        df1 = list(np.array(df))
        lst = []
        lst.append(column_list)
        for row in df1:
            lst.append(row)
        # json.dumps转换时间格式
        str1 = json.dumps(lst, cls=MyEncoder, ensure_ascii=False)
        # 再转回lst
        lst = json.loads(str1)
        return lst

    # 是否已有
    def Has(self, query={}, config={}):
        sql = mysqlPool.toOrWhere(query)
        df = pd.read_sql(sql, connection)
        return df == True