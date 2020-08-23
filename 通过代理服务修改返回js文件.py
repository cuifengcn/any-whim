# change_js.py
import re
import json
from mitmproxy.http import flow

def response(flow: flow):
    target_url = 'https://www.baidu.com'
    if  target_url in flow.request.url:
        jscode = flow.response.get_text()
        jscode = 'hello world.' # for test.
        flow.response.set_text(jscode)

# 功能：使用 mitmproxy 修改脚本，
#     使用 fiddler 也能做到，不过那种修改起来比较麻烦
#     使用 mitmproxy 可以使用 python 代码来修改返回信息，会更加方便一些
#     这样可以实现更加复杂的替换操作
#
# 需要安装 mitmproxy： pip install mitmproxy
# 使用该库的命令行工具 mitmdump 来创建一个代理端口
#
# mitmdump -q -s change_js.py -p 8888
# # -q 静音模式(仅限制该代码内的打印输出) -s 指定mitm中间件代码(即当前代码脚本) -p 指定端口
# 
# 使用代理方式打开 chrome ，建议使用 chromedriver 方式来增加代理打开，有时命令行打开代理无效
# --proxy-server=http://127.0.0.1:8888