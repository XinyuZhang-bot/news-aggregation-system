# -*- coding: utf-8 -*-

from app.core import controller
from django.core.mail import EmailMessage
import random
import string
import json
from hashlib import md5
from datetime import timedelta, timezone, datetime
from django.utils.timezone import make_aware

controllerClass = getattr(controller, "Controller")


# 验证码token
class Code_token(controllerClass):
    def __init__(self, config={}):
        config_init = {
            # 模板路径前缀
            "tpl": "./code_token/",
            # Service 名称
            "service": "code_token",
            # 接口地址
            "get_api": ["send_email", "verify_email_code"]
        }
        config_temp = config
        config_temp.update(config_init)
        super(Code_token, self).__init__(config_temp)

    # 发送验证码到邮箱
    def Send_email(self, ctx):
        query = dict(ctx.query)

        if "email" not in query:
            ret = {
                "error": {
                    "code": 30000,
                    "message": "参数错误",
                }
            }
            return ctx.response(json.dumps(ret, ensure_ascii=False))

        email = query.pop("email")

        # 生成验证码
        code = ''.join(random.choices(string.digits, k=6))
        now = datetime.now(timezone.utc)
        token = md5(f"{code}_{now.timestamp()}".encode()).hexdigest()

        # 配置邮件内容
        subject = "找回密码"
        body = f'<h1>验证码为：{code}</h1>'
        from_email = "3216252476@qq.com"  # 发件人邮箱
        to = [email]  # 收件人列表

        # 创建邮件对象
        message = EmailMessage(subject, body, from_email, to)

        # 设置邮件内容类型为 HTML（默认是纯文本）
        message.content_subtype = "html"
        try:
            # 发送邮件
            message.send()
            # 保存验证码到数据库
            service = self.service

            # 获取当前时间（UTC 时间）
            now = datetime.now(timezone.utc)

            # 调整为 UTC+8 时区（手动计算）
            beijing_time = now + timedelta(hours=8)

            # 增加 10 分钟
            future_time = beijing_time + timedelta(minutes=10)

            # 格式化为 'yyyy-MM-dd HH:mm:ss'
            formatted_future_time = future_time.strftime('%Y-%m-%d %H:%M:%S')

            body = {
                "token": token,
                "code": code,
                "expire_time": formatted_future_time
            }
            result = service.Add(body, self.config)
            # 返回结果
            ret = {
                "result": result,
                "token": token
            }
            return ctx.response(json.dumps(ret, ensure_ascii=False))
        except Exception as e:
            ret = {
                "error": {
                    "code": 30000,
                    "message": str(e),
                }
            }
            return ctx.response(json.dumps(ret, ensure_ascii=False))

    # 验证验证码是否正确
    def Verify_email_code(self, ctx):
        query = dict(ctx.query)
        if "token" not in query or "code" not in query:
            ret = {
                "error": {
                    "code": 30000,
                    "message": "参数错误"
                }
            }
            return ctx.response(json.dumps(ret, ensure_ascii=False))
        else:
            token = query.pop("token")
            code = query.pop("code")
            service = self.service
            obj = service.Get_obj({"token": token}, {"like": False})
            if obj:
                expire_time = make_aware(datetime.strptime(obj['expire_time'], "%Y-%m-%d %H:%M:%S"))
                now = datetime.now(timezone.utc)
                # 调整为 UTC+8 时区（手动计算）
                beijing_time = now + timedelta(hours=8)
                if beijing_time < expire_time:
                    if code == obj['code']:
                        ret = {
                            "result": 1
                        }
                        return ctx.response(json.dumps(ret, ensure_ascii=False))
                    else:
                        ret = {
                            "error": {
                                "code": 30000,
                                "message": "验证码错误"
                            }
                        }
                        return ctx.response(json.dumps(ret, ensure_ascii=False))
                else:
                    ret = {
                        "error": {
                            "code": 30000,
                            "message": "验证码已失效"
                        }
                    }
                    return ctx.response(json.dumps(ret, ensure_ascii=False))
            else:
                ret = {
                    "error": {
                        "code": 30000,
                        "message": "token请求错误"
                    }
                }
                return ctx.response(json.dumps(ret, ensure_ascii=False))
