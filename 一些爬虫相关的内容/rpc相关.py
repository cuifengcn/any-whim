# 代码还有点问题。

# !function(){
#   var websocket = new WebSocket("ws://127.0.0.1:8887/getinfo");
#   websocket.onopen = function(){
#     v_log("websocket open");
#   }
#   websocket.inclose = function(){
#     v_log('websocket close');
#   }
#   websocket.onmessage = function(e){
#     v_log('websocket.onmessage', e)
#     websocket.send(v_stringify(v_env_cache))
#   }
# }()

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
async def echo(websocket, path):
    async for message in websocket:
        print("path:{} message:{}".format(path, message))
        if path == '/server':
            await websocket.send(message+'asdf')
        if path == '/getinfo':
            await websocket.send(message+'asdf')
        await websocket.send('empty')
async def main():
    async with websockets.serve(echo, "localhost", 8887):
        await asyncio.Future()
asyncio.run(main())

