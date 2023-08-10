# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/19 16:21
# File : pwd.py

import asyncio

import aiofiles
# 修改windows编码为utf-8
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs


class EncryptPassword:
    def __init__(self):
        pass

    async def _open_file(self):
        async with aiofiles.open('../pwd_encrypt/js/jsencrypt_min.js', 'r', encoding='utf-8') as f:
            return await f.read()

    async def encrypt_password(self, password: str) -> dict:
        js_script = await self._open_file()
        script = execjs.compile(js_script)
        return script.call('enc_pass', password)


if __name__ == '__main__':
    # passw = EncryptPassword()
    # pa = passw.encrypt_password('aaaa')
    # print(pa)
    async def _main():
        passw = EncryptPassword()
        pa = await passw.encrypt_password('aaaa')
        return pa


    print(asyncio.run(_main()))
