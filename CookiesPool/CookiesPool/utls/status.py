# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/24 16:21
# File : status.py


from sanic.exceptions import SanicException


class CookieException(SanicException):
    status_code = 400
    message = "数据为空"
    data = ""
