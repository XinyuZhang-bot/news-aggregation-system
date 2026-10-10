# -*- coding: utf-8 -*-
"""
HTTP 请求封装：将 Django request 转为 CTX 对象，统一 JSON 响应格式。
"""
from django.shortcuts import render as django_render
from django.http import HttpResponse
from urllib.parse import parse_qs, urlparse
import json


def toQuery(str1):
    dt = {}
    arr = str1.split('&')
    for val in arr:
        ar = val.split('=')
        if len(ar) == 2:
            dt[ar[0]] = ar[1]
    return dt


class CTX:
    """控制器上下文：query=GET 参数，body=POST/JSON 请求体。"""

    def __init__(self, request):
        self.query = request.GET.dict()
        self.request = request
        self.response = HttpResponse
        self.auth = ""
        self.status = 200
        headers = request.headers
        if (("Content-Type" in headers) and headers["Content-Type"]):
            if (request.method == 'GET'):
                self.body = {}
            else:
                if headers["Content-Type"] == "application/json":
                    self.body = json.loads(request.body)
                elif headers[
                        "Content-Type"] == "application/x-www-form-urlencoded":
                    self.body = toQuery(bytes.decode(request.body))
                elif headers["Content-Type"] == "text/plain":
                    self.body = {}
                else:
                    self.body = request.POST.dict()

    def render(self, view, model):
        return django_render(self.request, view, model)


def router(method, actionFunc):
    """根据 method(get/post/all) 返回 Django 视图函数。"""

    def get(request):
        if request.method == "GET":
            ctx = CTX(request)
            body = actionFunc(ctx)
            if body and isinstance(body, HttpResponse) == False:
                if isinstance(body, dict):
                    return HttpResponse(json.dumps(body, ensure_ascii=False))
                else:
                    return HttpResponse(body)
            else:
                return body

    def post(request):
        if request.method == "POST":
            ctx = CTX(request)
            body = actionFunc(ctx)
            if body and isinstance(body, HttpResponse) == False:
                if isinstance(body, dict):
                    return HttpResponse(json.dumps(body, ensure_ascii=False))
                else:
                    return HttpResponse(body)
            else:
                return body

    def all_fun(request):
        ctx = CTX(request)
        body = actionFunc(ctx)
        if body and isinstance(body, HttpResponse) == False:
            if isinstance(body, dict):
                return HttpResponse(json.dumps(body, ensure_ascii=False))
            else:
                return HttpResponse(body)
        else:
            return body

    if method == "get":
        return get
    elif method == "post":
        return post
    else:
        return all_fun
