# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/7/23 16:15
# File : main.py

from CookiesPool.app import create_app

app = create_app()


# app.run(host='127.0.0.1', port=8888,access_log=False)

def run():
    app.run(host='127.0.0.1', port=8887, access_log=False)


if __name__ == '__main__':
    # single_process 单线程运行
    # app.run(host='127.0.0.1', port=8888, single_process=True,debug=True)
    run()
