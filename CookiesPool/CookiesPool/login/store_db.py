# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/24 19:40
# File : store_db.py

import asyncio
import logging
import aioredis
from CookiesPool.CookiesPool.login.request_login import Login
from CookiesPool.CookiesPool.settings import REDIS, REDIS_KEY, USER_JSON_, REDIS_EXPIRE_TIME, REDIS_CONFIG
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)


# logging.info("\033[0;32m" + message + "\033[0m")

class RedisPip:
    def __init__(self):
        self.conn = aioredis.from_url(**REDIS_CONFIG)

        # # 创建订阅对象
        self.pubsub = self.conn.pubsub()

        self.login = Login()

    async def redis_config(self):
        """redis配置"""
        # 配置 notify-keyspace-events，启用过期和删除事件通知 E:发布 x:过期 g:删除
        await self.conn.config_set('notify-keyspace-events', 'Exg')
        # 订阅过期事件通知，匹配 cookies:* 键名模式，需要先去数据库中设置 键空间通知允许订阅指定模式的键事件通知，而不是所有的键事件
        # 命令 CONFIG SET notify-keyspace-events Ex     然后重启数据库

        await self.pubsub.psubscribe(f"__keyevent@{REDIS.get('db', '0')}__:expired")  # 过期
        await self.pubsub.psubscribe(f"__keyevent@{REDIS.get('db', '0')}__:del")  # 删除

    async def set_key_with_expiry(self, redis_key, hash_key_username):
        # 登录得到cookie值,设置过期时间
        # cookie = await self.login.login(username=hash_key_username, pwd=USER_JSON_[hash_key_username])
        cookie = await self.login.login(username=hash_key_username, pwd=USER_JSON_[hash_key_username])
        # 存储到redis中，把cookie字典类型转换为json字符串类型
        await self.conn.hset(redis_key, hash_key_username, json.dumps(cookie))
        # //设置过期时间
        await self.conn.expire(redis_key, REDIS_EXPIRE_TIME)

    async def store_cookie(self):
        """存储到redis"""
        for username, pwd in USER_JSON_.items():
            redis_key = f"{REDIS_KEY}:{username}"
            # 先判断是否在数据库中，如果不在则登录后吧cookie存入
            if not await self.conn.hexists(redis_key, username):
                # 设置键和值到哈希，并设置过期时间
                await self.set_key_with_expiry(redis_key=redis_key, hash_key_username=username)
        return 'ok'

    async def store_cookie_any(self) -> None:
        """存储缺失的用户 Cookie"""
        # 启动的时候如果数据比配置文件中的少，则继续添加
        # redis数据库中查出来的是列表类型 [b'cookies:user2', b'cookies:user4', b'cookies:user1', b'cookies:user3']
        redis_key_list: list[str] = await self.conn.keys(f"{REDIS_KEY}:*")
        # USER_JSON_ {"user2":"123456",'user3':"dadas"}
        if len(redis_key_list) < len(USER_JSON_):
            # 根据账号名计算没有在数据库中的数据,然后登录获取到的cookie存入数据库
            user_set = set(USER_JSON_.keys()) - {user.split(":")[1] for user in redis_key_list}
            for username in user_set:
                redis_key = f"{REDIS_KEY}:{username}"
                await self.set_key_with_expiry(redis_key, hash_key_username=username)

    async def message_expired_del(self, message):
        """处理过期或者被删除的cookie"""
        # 获取键名 cookies:aaaa
        cookie_key: str = message["data"]
        hash_key_username = cookie_key.split(":")[1]
        await self.set_key_with_expiry(redis_key=cookie_key, hash_key_username=hash_key_username)
        logging.info("键过期了: %s", message["data"])

    async def listen_message(self):
        """监听过期事件"""
        async for message in self.pubsub.listen():
            logging.info(str(message))
            if message["type"] == "pmessage":
                await self.message_expired_del(message)

    async def main(self):
        # 判断数据库中是否是空的
        if await self.conn.dbsize() == 0:
            # 如果是空的,执行一遍添加数据的操作
            await self.store_cookie()
        # 启动的时候如果数据比配置文件中的少，则继续添加
        await self.store_cookie_any()

        logging.info('============================')
        # 开始监听过期事件
        await self.listen_message()


async def run():
    red = RedisPip()
    await red.redis_config()  # 发布订阅配置
    await red.main()


def runserver():
    asyncio.run(run())


if __name__ == '__main__':
    runserver()
    # run()
    # print(red.store_cookie())

    # 示例使用，设置键并指定过期时间
    # red.set_key_with_expiry("my_hash", "field1", "value1", 60)
