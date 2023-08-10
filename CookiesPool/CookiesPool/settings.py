# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/23 15:17
# File : settings.py

import os
from CookiesPool.CookiesPool.config_json import UserJson

BASEDIR = os.path.abspath(os.path.dirname(__file__))

JSON_PATH = os.path.join(BASEDIR, 'UserPwd.json')

# 转发秘钥，比如nginx就需要
FORWARDED_SECRET = 'asdasd16165163'

CORS_ORIGINS = ['http://127.0.0.1:887', 'http://localhost:887']

# 登录获取cookie的并发量
COOKIE_LOGIN_SEMAPHORE = 4

# redis配置
REDIS_KEY = "cookies"
REDIS_EXPIRE_TIME = 60 * 60 * 22  # 过期时间
# REDIS_EXPIRE_TIME = 20  # 过期时间
REDIS = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': '0'
}
REDIS_CONFIG = {
    'url': f'redis://{REDIS.get("host", "127.0.0.1")}:{REDIS.get("port", "6379")}/{REDIS.get("db", "0")}',
    'max_connections': 10,  # 最大连接数量
    'decode_responses': True,  # 返回值解码

}

# mongodb数据库中集合的名称
MONGO_DATABASE = 'cookie_user'
MONGO_COLLECTION = 'cookie_user'
MONGO_CONFIG = {
    'host': 'localhost',  # MongoDB 主机地址
    'port': 27017,  # MongoDB 端口号
    # 'username': 'myuser',  # MongoDB 用户名
    # 'password': 'mypassword',  # MongoDB 密码
    'authSource': MONGO_DATABASE,  # MongoDB 鉴权数据库
    # 'authMechanism': 'SCRAM-SHA-1',  # 鉴权机制（可根据 MongoDB 的实际配置调整）
    'maxPoolSize': 100,  # 连接池中允许的最大连接数
    'minPoolSize': 1,  # 连接池中保持的最小连接数
}

# 配置文件，账号和密码配置
USER_JSON_: dict = UserJson().user_json

if __name__ == '__main__':
    print(BASEDIR)
    print(USER_JSON_)
