# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/19 22:00
# File : get_cookie.py

from fake_useragent import UserAgent
import asyncio
import aiohttp
from aiohttp import ClientResponse
from lxml import etree


class GetCookie:
    def __init__(self, login_url: str = 'http://shanzhi.spbeen.com/login/'):
        self.login_url = login_url

    async def request_index_html(self):
        ua = str(UserAgent.random)
        headers = {
            'User-Agent': ua
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.login_url, headers=headers) as resp:
                text = await resp.text()
                return resp, text

    async def html_parse(self, resp: ClientResponse, html_text: str) -> dict:
        """"""

        xpath_html = etree.HTML(html_text)
        csrfmiddlewaretoken = xpath_html.xpath("//input[@name='csrfmiddlewaretoken']/@value")[0]
        # Set-Cookie: csrftoken=mI037TPq0fmmv5FCsiI0i7rVNxSmxIRficMsawTPMIBhyNy5X3TOj1J9wUvoAbcn; Domain=shanzhi.spbeen.com; expires=Wed, 07 Aug 2024 05:15:28 GMT; Max-Age=31449600; Path=/; SameSite=Lax
        # 合并
        csrf = dict({'csrfmiddlewaretoken': csrfmiddlewaretoken}, **dict(resp.cookies))
        return csrf

    async def csrf(self) -> dict:
        resp, text = await self.request_index_html()
        csrf = await self.html_parse(resp, text)
        return csrf


if __name__ == '__main__':
    async def _main():
        get_cookie = GetCookie()
        csrf = await get_cookie.csrf()
        return csrf


    # get_cookie = GetCookie()
    # print(get_cookie.csrf())
    print(asyncio.run(_main()))
    # asyncio.run(_main())
