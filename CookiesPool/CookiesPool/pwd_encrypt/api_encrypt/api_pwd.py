# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/19 21:20
# File : api_pwd.py


import requests


class ApiPwd(object):
    def __init__(self, url: str = "http://127.0.0.1", port: int = 3000, pwd_url: str = '/getpwd'):
        self.api_url = url + ":" + str(port) + pwd_url

    def request(self, pwd: str) -> dict:
        params = {'pwd': pwd}
        resp = requests.get(url=self.api_url, params=params)
        return resp.json()


if __name__ == '__main__':
    api_pwd = ApiPwd()
    pwd = api_pwd.request(pwd='aaa')
    print(pwd)
