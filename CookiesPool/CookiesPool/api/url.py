# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/23 16:17
# File : url.py

from sanic import Blueprint
from CookiesPool.CookiesPool.api.views import PoolViews, UserViews,UserRegisterViews

cookie = Blueprint('cookie', url_prefix='/user')
cookie.add_route(PoolViews.as_view(), '/cookie')

user = Blueprint('user', url_prefix='/user')
user.add_route(UserViews.as_view(), 'login')
user.add_route(UserRegisterViews.as_view(), 'register')
