# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/23 16:18
# File : views.py


import jwt
import json as djson
from sanic.views import HTTPMethodView
from sanic.response import json, JSONResponse
from sanic.request import Request
from sanic.exceptions import Unauthorized, SanicException
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient, AsyncIOMotorDatabase
from aioredis import Redis

from CookiesPool.CookiesPool.api.val import validate_input, is_valid_token
from CookiesPool.CookiesPool.utls.status import CookieException


# 配置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PoolViews(HTTPMethodView):
    """获取cookie"""

    @is_valid_token  # 验证令牌
    async def get(self, request: Request, *args, **kwargs) -> JSONResponse:
        """
        获取cookie
        :param request:
        :return:
        """

        username = request.ctx.username
        # redis连接池
        redis_pool: Redis = request.app.ctx.redis_pool
        # 随机获取一个数据，类型集合
        # result = await redis_pool.srandmember(request.app.config.get('REDIS_KEY', 'cookies'))

        # 获取查询字符串
        # 使用 request.ctx.username 获取已验证的用户名

        random_key: str = await redis_pool.randomkey()

        result_str: str = await redis_pool.hget(random_key, random_key.split(':')[1])
        result = djson.loads(result_str)
        if result:
            return json({'message': 'ok', 'data': result, "username": username}, status=200)
        raise CookieException(status_code=400)


class UserViews(HTTPMethodView):
    @validate_input
    async def post(self, request: Request):
        """
        post请求
        :param request:
        :return:
        """
        # mongo连接池
        mongo_pool: AsyncIOMotorClient = request.app.ctx.mongo_pool
        # mongo数据库
        db: AsyncIOMotorDatabase = mongo_pool[request.app.config.get('MONGO_DATABASE')]
        # mongo数据库的集合
        collection: AsyncIOMotorCollection = db[request.app.config.get('MONGO_COLLECTION')]

        username = request.json.get("username")
        password = request.json.get("password")

        # 验证用户凭据
        user = collection.find_one({"username": username, "password": password})
        if not user:
            raise Unauthorized("无效的用户名或密码")

        # 如果验证成功，生成 JWT 令牌并将其返回给用户
        token = jwt.encode({"username": username}, request.app.ctx.SECRET, algorithm="HS256")
        return json({"code": 200, "message": 'ok', "data": username}, headers={'token': token})


class UserRegisterViews(HTTPMethodView):
    """注册"""

    @validate_input
    async def post(self, request: Request):
        """注册"""
        # mongo连接池
        mongo_pool: AsyncIOMotorClient = request.app.ctx.mongo_pool
        # mongo数据库
        db: AsyncIOMotorDatabase = mongo_pool[request.app.config.get('MONGO_DATABASE')]
        # mongo数据库的集合
        collection: AsyncIOMotorCollection = db[request.app.config.get('MONGO_COLLECTION')]

        username = request.json.get('username')
        password = request.json.get('password')

        user_one = await collection.find_one({"username": username})
        if user_one:
            return json({"code": 200, 'data': "该账号已经存在"})
        # 查询一条数据
        result = await collection.insert_one({'username': username, "password": password})
        if result:
            token = jwt.encode({"username": username}, request.app.ctx.SECRET, algorithm="HS256")
            return json({"code": 200, "message": 'ok', "data": username}, headers={'token': token})
        raise SanicException
