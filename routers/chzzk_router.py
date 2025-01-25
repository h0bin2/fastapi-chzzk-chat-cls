from typing import Optional
from fastapi import APIRouter, Depends, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from db.connection import get_db
from views import chzzk_view

from schemas.chzzk_schema import *

from core.config import settings
from core.chzzk import Chat

import websockets
import asyncio
import json

from pytz import timezone
from datetime import datetime, timedelta


chzzk = APIRouter(
    prefix="/chzzk"
)

@chzzk.get('/top20')
def chzzk_top20_List(request: Request):
    res = chzzk_view.get_chzzk_top20_list()
    return res

@chzzk.websocket('/ws/{bjid}')
async def connect_chzzk(mySocket: WebSocket, bjid: str):
    print(f'Client Connected[FastAPI] : {mySocket.client}')
    await mySocket.accept()
    await mySocket.send_text(f'Connectting Chzzk Just Wait..')
    try:
        chat = Chat(bjid)
        async with websockets.connect(chat.socketUrl, ping_interval=60) as websocket:
            await websocket.send(json.dumps(chat.reqData))

            if chat.channelId is None:
                return

            while True:
                now = datetime.now(timezone('Asia/Seoul'))

                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=60.0)
                except asyncio.TimeoutError:
                    print(f"{chat.bjid} timeout")
                    break

                response = json.loads(response)

                if response['cmd'] == 0:
                    await websocket.send(json.dumps({'ver':"3", 'cmd':10000}))
                    print(f"{chat.channelId}", end=' / ')
                    continue

                if response['cmd'] == 93101:
                    for res in response['bdy']:
                        msg = res['msg']
                        nickname = json.loads(res['profile'])['nickname']
                        strNow = now.strftime('%Y-%m-%d_%H:%M:%S')
                        await mySocket.send_text(f'{chat.nickname}-{nickname} : {msg}[{strNow}]')
                
                if response is None:
                    print(f"{chat.channelId} 방송 종료됨.")
                    break
    except WebSocketDisconnect:
        print("클라이언트 연결 종료")               
    except Exception as e:
        print(e)
        await mySocket.send_text('Fail Chzzk')
