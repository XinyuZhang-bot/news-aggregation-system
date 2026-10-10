# -*- coding: utf-8 -*-

from hashlib import md5
from app.core import controller
from app.service import service_select
import json

controllerClass = getattr(controller, "Controller")


# 帮助方法，取得md5后的hash值
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


# 找回密码
class Forgot(controllerClass):
	def __init__(self, config={}):
		config_init = {
			# 模板路径前缀
			"tpl": "./forgot/",
			# Service 名称
			"service": "user",
		}
		super(Forgot, self).__init__(obj_update(config_init, config))

	def Api(self, ctx):
		user = service_select("user")
		body = ctx.body
		username = body["username"]
		obj = {}
		text = ""
		if "email" in body:
			email = body["email"]
			text = "邮箱"
			obj = user.Get_obj({"username": username, "email": email}, { "like": False }) or {}
		elif "phone" in body:
			phone = body["phone"]
			text = "号码"
			obj = user.Get_obj({"username": username, "phone": phone}, { "like": False }) or {}
		# print("OBJ" , obj)
		if obj:
			password = md5hash(body["password"])
			bl_for = user.Set({"username": username}, {"password": password})
			if bl_for:
				return ctx.response(json.dumps({"result": "修改成功"}, ensure_ascii=False))
			else:
				error = {
					"error": {
						"code": 70000,
						"message": "修改失败",
					}
				}
				return ctx.response(json.dumps(error, ensure_ascii=False))
		else:
			error = {
				"error": {
					"code": 70000,
					"message": "账户不存在或" + text + "错误",
				}
			}
			return ctx.response(json.dumps(error, ensure_ascii=False))