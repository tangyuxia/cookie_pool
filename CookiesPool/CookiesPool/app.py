# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/23 16:13
# File : app.py

# import tracemalloc

import aiomysql
import aioredis
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic
from orjson import dumps

from CookiesPool.CookiesPool import settings
from CookiesPool.CookiesPool.api.url import user, cookie
from CookiesPool.CookiesPool.utls.status import CookieException
from CookiesPool.CookiesPool.utls.cookie_exception import handle_cookie_exception


# 启动 tracemalloc
# tracemalloc.start()


def create_app(config_name=None):
    app = Sanic("register", dumps=dumps)
    app.config.update_config(settings)  # 导入配置
    # app.ctx.auth = Auth(app)

    # 注册app
    register_app(app)

    # jwt秘钥 随机的
    app.ctx.SECRET = 'dampfjamfanfoafnaljfnab%$#<>adf1685165?/=-'
    # nginx配置反向代理的秘钥
    app.config.FORWARDED_SECRET = 'adafafa1641d6ad1a6<>?@#%$-daf'
    # app.config.CORS_ORIGINS = ['http://127.0.0.1:8887', 'http://localhost:8887']
    # print(app.config.FORWARDED_SECRET)
    # print(app.config.CORS_ORIGINS)

    return app


def register_app(app: Sanic) -> Sanic:
    create_blueprint(app)  # 创建蓝图

    # 异常处理
    app.exception(CookieException, handle_cookie_exception)
    # app.blueprint(user)
    # 注册redis before_server_start代表在服务启动之前连接数据库
    app.register_listener(setup_redis_pool, 'before_server_start')
    # 注册mongo
    app.register_listener(setup_mongo_pool, 'before_server_start')

    # 程序退出之前关闭数据库连接
    app.register_listener(stop_app, 'before_server_stop')

    return app


def create_blueprint(app: Sanic) -> Sanic:
    app.blueprint(user)  # 注册user
    app.blueprint(cookie)  # 注册cookie
    return app


async def stop_app(app: Sanic) -> None:
    # 关闭mysql
    # app.ctx.db_pool.close()
    # 关闭mongo
    if 'mongo_pool' in app.ctx:
        app.ctx.mongo_pool.close()
    # 关闭redis
    if 'redis_pool' in app.ctx:
        app.ctx.redis_pool.close()
        await app.ctx.redis_pool.wait_closed()


async def setup_mysql_pool(app: Sanic) -> None:
    # before_server_start代表在服务启动之前连接数据库
    # 注册mysql数据量应用
    app.ctx.db_pool = await aiomysql.create_pool(**app.config.get('MYSQL_CONFIG'), autocommit=True, minsize=1,
                                                 maxsize=10)


async def setup_mongo_pool(app: Sanic) -> None:
    app.ctx.mongo_pool = AsyncIOMotorClient(**app.config.get("MONGO_CONFIG"))


async def setup_redis_pool(app: Sanic) -> None:
    """注册redis"""
    # app.ctx.redis_pool = await aioredis.create_pool(**settings.REDIS_CONFIG, minsize=5, maxsize=10, loop=loop)
    app.ctx.redis_pool = aioredis.from_url(**app.config.get('REDIS_CONFIG'))
