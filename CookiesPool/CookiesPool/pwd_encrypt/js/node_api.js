// 导入express框架
const express = require('express');

// 导入的需用破解的函数文件名，后面不要加.js
const { enc_pass } = require('./jsencrypt_min');

// 创建Express应用程序
const app = express();

// 处理/getw1请求
// http://127.0.0.1:3000/getpwd?pwd=aaaaa
app.get('/getpwd', (req, res) => {
    // 获取请求参数
    const str = req.query.pwd;
    // 调用自定义函数 w1 进行处理
    const result = enc_pass(str);

    // 将结果发送回Python程序
    res.send(result);
});

const port = 3000;
const host = '127.0.0.1';

app.listen(port, host, () => {
    console.log(`Server is running on ${host}:${port}`);
});

