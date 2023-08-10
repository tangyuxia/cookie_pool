# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/24 20:04
# File : config_json.py

import os
import aiofiles
import asyncio
import json

BASEDIR = os.path.abspath(os.path.dirname(__file__))

JSON_PATH = os.path.join(BASEDIR, 'UserPwd.json')


class UserJson:
    """读取json配置文件中的账号密码"""

    def __init__(self):
        pass

    async def load_config_file(self):
        # from CookiesPool.CookiesPool.settings import JSON_PATH
        try:
            async with aiofiles.open(JSON_PATH, mode='r') as file:
                data = await file.read()
                config_data = json.loads(data)
                return config_data
        except FileNotFoundError:
            print(f"文件未找到: {JSON_PATH}")
            return None
        except json.JSONDecodeError:
            print(f"文件中无效的JSON格式: {JSON_PATH}")
            return None

    async def load_settings(self):
        config_data = await self.load_config_file()
        return config_data

    async def get_settings(self):
        return await self.load_settings()

    async def main(self):
        user_json = await self.get_settings()
        return user_json

    @property
    def user_json(self):
        config_data = asyncio.run(self.main())
        return config_data


if __name__ == '__main__':
    # user_json=UserJson()
    # print(user_json.user_json())
    print(UserJson().user_json)
