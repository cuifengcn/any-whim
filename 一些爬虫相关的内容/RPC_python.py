# !function(){
#   var websocket = new WebSocket("ws://127.0.0.1:8887/browser");
#   websocket.onopen = function(){
#     var info = 'browser:start'
#     console.log(info);
#     websocket.send(info)
#   }
#   websocket.onmessage = function(e){
#     console.log('websocket.onmessage', e.data)
#     // 这里处理请求参数以及对应rpc函数调用，返回参数用字符串传递回 websocket
#     var ret = ''
#     websocket.send(ret)
#   }
# }()






# pip install websockets flask

import traceback
import threading
from urllib.parse import unquote
from flask import Flask, request
app = Flask(__name__)
@app.route('/', methods=['POST'])
def main():
    try:
        info = unquote(request.data.decode())
        async def clientRun():
            async with websockets.connect("ws://127.0.0.1:8887/getinfo") as websocket:
                await websocket.send(info)
                return await websocket.recv()
        return asyncio.run(clientRun())
    except:
        traceback.print_exc()
        return "启动接口失败."
threading.Thread(target=app.run).start()


import asyncio
import websockets
tog = False
async def echo(websocket, path):
    global tog
    async for message in websocket:
        print("path:{} message:{}".format(path, message))
        if path == '/browser':
            if message == 'browser:start':
                tog = True
                while 1:
                    await websocket.send(await que.get())
                    await res.put(await websocket.recv())
        if path == '/getinfo':
            if tog:
                await que.put(message)
                return await websocket.send(await res.get())
            return await websocket.send('browser websocket not start.')
async def main():
    global que, res
    que = asyncio.Queue()
    res = asyncio.Queue()
    async with websockets.serve(echo, "localhost", 8887):
        await asyncio.Future()
asyncio.run(main())

