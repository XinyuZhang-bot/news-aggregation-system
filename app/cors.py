# -*- coding: utf-8 -*-
"""CORS 中间件：允许前端跨域访问 API（开发/前后端分离场景）。"""
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


class CorsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "Origin" or request.method == "OPTIONS":
            return HttpResponse(status=204)

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Headers'] = "Content-Type,Accept,Authorization,x-auth-token"
        response["Access-Control-Allow-Credentials"] = "true"
        response['Access-Control-Allow-Methods'] = "*"
        response["Access-Control-Max-Age"] = "86400"
        return response
