import requests
import json
import asyncio
import websockets
import pandas as pd

from fake_useragent import UserAgent
import ssl

from datetime import datetime
from pytz import timezone

class Top():
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context

        user_agent = UserAgent()
        self.headers = {'User-Agent': user_agent.random} #requests 로 get 요청 때 user-Agent 오류 떠서 해결하기 위함. 

        self.bjid_list = {} #csv로 만들기 위한 보관함 딕셔너리
        self.getAPIURL = "https://api.chzzk.naver.com/service/v1/lives" #현재 방송중인 방송국 중 가장 인기 있는 방송국 20개 출력 api
        self.params = {
            'size':20,
            'sortType':'POPULAR'
        }
        self.getTop()
        
    def getTop(self):
        tops = requests.get(url=self.getAPIURL, headers=self.headers, params=self.params).json()['content']['data']
        for top in tops:
            channel = top['channel']
            self.bjid_list[channel['channelName']] = channel['channelId']

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(self.bjid_list.items())[index]
        return list(self.bjid_list.items())[index]
    

class Chzzk():
    def __init__(self, bjid):

        self.bjid = bjid
        
        self.session = requests.session()
        self.channelId = ""
        self.nickname = ""
        
        self.accessToken = ""
        self.extraToken = ""

        self.nowTime = datetime.now(timezone('Asia/Seoul'))

    def getChannelInfo(self):
        try:
            url = f'https://api.chzzk.naver.com/polling/v3/channels/{self.bjid}/live-status'
            self.channelId = self.session.get(url=url).json()['content']['chatChannelId']
            if self.channelId is None:
                raise Exception
            print(f'channelId : {self.channelId}')
        except:
            print(f"{self.bjid} : channelId not found(getChannelInfo)")

    def getToken(self):
        try:
            url = f'https://comm-api.game.naver.com/nng_main/v1/chats/access-token?channelId={self.channelId}&chatType=STREAMING'
            token = self.session.get(url=url).json()['content']

            self.accessToken = token['accessToken']
            self.extraToken = token['extraToken']

        except:
            print(f'{self.bjid} : Token not found(getToken)')


class Chat(Chzzk):
    def __init__(self, bjid):
        self.socketUrl = 'wss://kr-ss1.chat.naver.com/chat'
        self.chatting = {'host':[], 'channelId':[], 'nickname':[], 'msg':[], 'time':[]}

        super().__init__(bjid)
        super().getChannelInfo()
        super().getToken()

        self.reqData = {
            'bdy':{
                'accTkn':self.accessToken,
                'auth':'READ',
            },
            'cid':self.channelId,
            'cmd':100,
            'svcid':'game',
            'tid':1,
            'ver':'3'
        }