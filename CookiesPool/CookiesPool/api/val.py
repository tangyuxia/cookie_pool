# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/8/9 17:34
# File : val.py

from functools import wraps
from sanic.exceptions import  Unauthorized
import jwt
import re
from sanic.request import Request
from sanic.response import json


def validate_input(func):
    async def wrapper(request: Request):
        username = request.json.get("username")
        password = request.json.get("password")

        # 验证 username 长度4-12,可以是汉字
        if not re.match(r'^[a-zA-Z\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5]{3,11}$', username):
            return json({"code": 400, "message": "Invalid username"}, status=400)

        # 验证 password 长度8-16
        if not re.match(r'^[a-zA-Z0-9]{8,16}$', password):
            return json({"code": 400, "message": "Invalid password"}, status=400)

        return await func(request)

    return wrapper


def is_valid_token(func):
    async def wrapper(self,request: Request, *args, **kwargs):
        # print(request.json)
        token = request.headers.get("token")
        if not token:
            raise Unauthorized("无效令牌")
        try:

            # 尝试解码令牌
            decoded_token = jwt.decode(token, request.app.ctx.SECRET, algorithms=["HS256"])
            username = decoded_token.get("username")
        except jwt.InvalidTokenError:
            # 如果解码失败，说明令牌无效
            raise Unauthorized("无效令牌")
        # 在装饰器中添加用户信息到请求对象中，以便在视图函数中使用
        request.ctx.username = username

        return await func(self,request, *args, **kwargs)

    return wrapper
