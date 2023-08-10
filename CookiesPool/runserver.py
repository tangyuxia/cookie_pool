# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/8/8 10:30
# File : runserver.py

import sys
from multiprocessing import Process
import os
import subprocess

from CookiesPool.app import create_app
from CookiesPool.login.store_db import RedisPip
from CookiesPool.settings import BASEDIR

app = create_app()
red = RedisPip()

def start_sanic():

    # 启动 sanic
    sanic_path = os.path.dirname(BASEDIR)
    sanic_script = 'main.py'
    # host = '127.0.0.1'
    # port = '8887'
    # sanic_agr = ['--host', host, ]
    subprocess.Popen(['python', sanic_script], cwd=sanic_path)


def start_cookie_pool():
    # 启动 sanic
    cookie_path = os.path.join(BASEDIR,'login')
    cookie_script = 'store_db.py'
    # host = '127.0.0.1'
    # port = '8887'
    # sanic_agr = ['--host', host, ]
    subprocess.Popen(['python', cookie_script], cwd=cookie_path)

# def start_all_programs():
#     processes = []
#
#     login_process = Process(target=red.main)
#     sanic_api_process = Process(target=statr_sanic)
#     # verification_process = Process(target=start_verification_program)
#
#     processes.append(login_process)
#     processes.append(sanic_api_process)
#     # processes.append(verification_process)
#
#     for process in processes:
#         process.start()
#
#     for process in processes:
#         process.join()
#
#
# def start_program(program_name):
#     if program_name == "cookies":
#         red.main()
#     elif program_name == "sanic":
#         statr_sanic()
#     # elif program_name == "verification":
#     #     start_verification_program()
#     else:
#         print("Invalid program name")
#
#
# def statr_sanic():
#     app.run(host='127.0.0.1', port=8887)
#
#
# def main():
#     if len(sys.argv) == 2:
#         if sys.argv[1] == "all":
#             start_all_programs()
#         else:
#             start_program(sys.argv[1])
#     else:
#         print("Usage: python start_programs.py <program_name | all>")


# if __name__ == '__main__':
#     # single_process 单线程运行
#     """"""
#     # main()
#     print(BASEDIR)
#     print(sanic_path)

if __name__ == '__main__':
    start_sanic()