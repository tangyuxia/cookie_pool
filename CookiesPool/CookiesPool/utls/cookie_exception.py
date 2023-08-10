# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/24 16:38
# File : cookie_exception.py

"""
异常数量器
"""
from sanic.request import Request
from sanic import json
from CookiesPool.CookiesPool.utls.status import CookieException


# 定义异常处理器并添加类型注释
async def handle_cookie_exception(request: Request, exception: CookieException) -> json:
    return json({'msg': exception.message, 'data': exception.data})
