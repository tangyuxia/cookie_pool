# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/23 18:48
# File : redis_.py

from random import choice
from aioredis import ConnectionPool


class RedisPool():
    def __init__(self, conn_pool: ConnectionPool):
        self.conn_pool = conn_pool

    # 上下文管理器
    async def __aenter__(self):
        self.conn = self.conn_pool
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

    def add_one(self):
        pass

    def get_one(self, redis_key):
        data = self.conn_pool.e
        print(data)
        if data:
            random_data = choice(data)  # 随机选择一条数据
            return random_data
        else:
            return None
