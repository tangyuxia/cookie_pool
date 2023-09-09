# CookiesPool

#### 介绍
1. 一个简单的cookie池，对应网站是闪职，这个网站是专门的爬虫工程师练习网站.在这里感谢网站作者的贡献
2. 该项目全部是异步编程
3. 用户名密码存入mongodb数据库中，cookie存入redis数据库中
4. 使用了redis的发布订阅模式，cookie过期后会自动登录，如果cookie被手动删除后也会自动登录 
5. 网站地址：http://shanzhi.spbeen.com/
6. 登录需要用到js逆向，本项目是用PyExecJs库直接执行js代码
7. 随机ua用的fake-useragent库
8. 发生请求用的aiohttp库

---

#### python版本 python3.10


---


#### 软件架构
1. 需要用到sanic、redis数据库、mongodb数据库
2. 访问cookie池api是用sanic框架编写的
3. 访问api需要用户登录，请求头中的token
#### 安装教程

---
1. gitee地址
```bash
git clone git@gitee.com:snow-lotos/cookies-pool-c.git
```
2. github地址
```bash
git clone git@github.com:tangyuxia/cookies_pool.git
```
3. 安装依赖包,推荐创建虚拟环境安装
``` bash
pip3 install -r requirements.txt
```

---

#### 项目启动 
1. 运行run_cookie.py 启动cookie池
2. 运行main.py 启动后端api接口

---

#### 项目配置
1. setting.py为配置文件
2. UserPwd.json为账号密码，可以直接去闪职网站注册后添加

---

#### 使用
1. 先访问注册接口,需要username和password，json格式传入
```bash
POST /user/register 
```
2. 访问登录接口，需要username和password，json格式传入，后续需要用到响应头里面的token
```bash
POST /user/login
```
3. 访问cookie池api，需要用第二步登录的token，添加到请求头中
```bash
GET /user/cookie
```