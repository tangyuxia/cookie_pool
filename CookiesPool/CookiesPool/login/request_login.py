# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/19 16:20
# File : request_login.py

from fake_useragent import UserAgent
import aiohttp
from aiohttp.cookiejar import Morsel
import asyncio

from CookiesPool.CookiesPool.login.get_cookie import GetCookie
from CookiesPool.CookiesPool.pwd_encrypt.encrypt.pwd import EncryptPassword
from CookiesPool.CookiesPool.settings import COOKIE_LOGIN_SEMAPHORE
from CookiesPool.CookiesPool.pwd_encrypt.api_encrypt.api_pwd import ApiPwd


class Login:
    def __init__(self, index_url: str = 'http://shanzhi.spbeen.com/login/'):
        self.index_url = index_url
        # 并发量
        self.semaphore = asyncio.Semaphore(COOKIE_LOGIN_SEMAPHORE)
        self.csrf = GetCookie()

    async def login(self, username: str, pwd: str):
        headers = {'User-Agent': str(UserAgent.random)}

        csrf_cookie = await self.csrf.csrf()

        csrfmiddlewaretoken = csrf_cookie.get('csrfmiddlewaretoken')
        csrftoken_: Morsel = csrf_cookie.get('csrftoken')

        csrftoken = {csrftoken_.key: csrftoken_.value}

        enc = EncryptPassword()
        # password = enc.encrypt_password(pwd)['pwd']
        password_dict = await enc.encrypt_password(pwd)
        password = password_dict['pwd']

        # api启动
        # enc = ApiPwd()
        # password=enc.request(pwd)['pwd']

        data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrfmiddlewaretoken

        }
        async with aiohttp.ClientSession(cookies=csrftoken) as session:
            # resp = await session.post(url=self.index_url, data=data, headers=headers, cookies={'csrftoken': csrftoken})
            resp = await session.post(url=self.index_url, data=data, headers=headers)
        cookie_shanzhi_kmer_dict = {cookie.key: cookie.value for cookie in resp.cookies.values()}
        return dict(cookie_shanzhi_kmer_dict, **csrftoken)


async def main(username: str, pwd: str):
    login = Login()
    return await login.login(username=username, pwd=pwd)


if __name__ == '__main__':
    # username = 'user1'
    # pwd = 'py123456'
    # login = Login()
    print(asyncio.run(main(username='user1', pwd='py123456')))
    # print(login.login(username, pwd))
