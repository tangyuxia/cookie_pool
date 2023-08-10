# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/8/9 16:32
# File : auth.py

from functools import wraps

import jwt
from sanic import text
from sanic.request import Request


def check_token(request: Request):
    if not request.token:
        return False

    try:
        jwt.decode(
            request.token, request.app.config.SECRET, algorithms=["HS256"]
        )
    # JWT 解码失败，说明令牌无效
    except jwt.exceptions.InvalidTokenError:
        return False
    # JWT 解码成功，令牌有效
    else:
        return True


def protected(wrapped):
    """定义一个装饰器函数，用于保护需要认证的路由"""
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # 检查用户是否已经通过身份验证
            is_authenticated = check_token(request)

            if is_authenticated:
                # 如果用户已认证
                # 调用被装饰的函数
                response = await f(request, *args, **kwargs)
                return response
            else:
                # 如果用户未认证
                # 返回 401 未授权状态码的文本响应
                return text("You are unauthorized.", 401)

        return decorated_function

    return decorator(wrapped)
