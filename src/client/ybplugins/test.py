'''
自定义功能：

在这里可以编写自定义的功能，
编写完毕后记得 git commit，

这个模块只是为了快速编写小功能，如果想编写完整插件可以使用：
https://github.com/richardchien/python-aiocqhttp
或者
https://github.com/richardchien/nonebot

关于PR：
如果基于此文件的PR，请在此目录下新建一个`.py`文件，并修改类名
然后在`yobot.py`中添加`import`（这一步可以交给仓库管理者做）
'''

import asyncio
from typing import Any, Dict, Union

from aiocqhttp.api import Api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart

import requests
import time
import random
import re

import ab
import json

from ybplugins import ybdata
from ybplugins import clan_battle


# 图灵机器人API
url = "http://openapi.tuling123.com/openapi/api/v2"
# 图灵机器人POST数据
payload = {
	"reqType":0,
    "perception": {
        "inputText": {
            "text": "可可萝"
        }
    },
    "userInfo": {
        "apiKey": "f25069c9279945388b191de71715f344",
        "userId": "487406"
    }
}
# POST访问头
headers = {
  'Content-Type': 'application/json'
}
# 图灵机器人APIKEY
apiKey = [
    "db35ba9e08ad4acfa1942d80fc87eac0","f25069c9279945388b191de71715f344",
    "67ade1de28fa440f9248851caebbdb68",
    "4d9af4e01f754827a03fd1d946766aa3",
    "b13414ff212840759e08455398326e41",
]


class Test:
    Himg:[]
    def __init__(self,
                 glo_setting: Dict[str, Any],
                 scheduler: AsyncIOScheduler,
                 app: Quart,
                 bot_api: Api,
                 *args, **kwargs):
        '''
        初始化，只在启动时执行一次

        参数：
            glo_setting 包含所有设置项，具体见default_config.json
            bot_api 是调用机器人API的接口，具体见<https://python-aiocqhttp.cqp.moe/>
            scheduler 是与机器人一同启动的AsyncIOScheduler实例
            app 是机器人后台Quart服务器实例
        '''
        # 注意：这个类加载时，asyncio事件循环尚未启动，且bot_api没有连接
        # 此时不要调用bot_api
        # 此时没有running_loop，不要直接使用await，请使用asyncio.ensure_future并指定loop=asyncio.get_event_loop()
        # 调用api发送消息，详见cqhttp文档
        # await self.api.send_private_msg(
        # user_id=740984027, message='收到问好')
        # 如果需要启用，请注释掉下面一行
        #return

        # 这是来自yobot_config.json的设置，如果需要增加设置项，请修改default_config.json文件
        self.setting = glo_setting

        # 这是cqhttp的api，详见cqhttp文档
        self.api = bot_api

        def getRecentYandeImgUrl(self):
            print('获取日榜图片URL中')
            rankByDayHtml=requests.get('https://yande.re/post/popular_recent').text
            regex=re.compile('"sample_url":.*\.jpg","s')
            imgUrl=re.findall(regex,rankByDayHtml)
            for index in range(len(imgUrl)):
                imgUrl[index]=imgUrl[index].replace('"sample_url":','').replace(',"s','')
            print('获取日榜图片URL成功')
            return imgUrl
        # self.Himg=getRecentYandeImgUrl(self)
        
        
        # 保留此接口作为每日早安任务
        @scheduler.scheduled_job('cron', hour='8', minute='30')
        async def good_morning():
            now = time.time() # 获取时间戳
            local_time = time.localtime(now)  # 转时区

            month = int(time.strftime('%m', local_time))    # 获得富格式时间
            date = int(time.strftime('%d', local_time))

            # 查询节假日API，决定动作模式
            date_format_localtime = time.strftime('%Y%m%d', local_time)
            url = "http://tool.bitefu.net/jiari/?d=" + date_format_localtime + "&info=1"
            response = requests.request("GET", url).json()

            type = response["type"]  # Extract信息
            weekcn = response["weekcn"]

            if type == 0:
                new_msg = "主人早安，今天是" + str(month) + "月" + str(date) + "号周" + str(weekcn) + "呢，请打起精神来准备上班啦~"
            elif type == 1:
                new_msg = "主人起得真早，今天是" + str(month) + "月" + str(date) + "号周" + str(weekcn) + "哦，周末再多睡一点也没关系的呢"
            else:
                new_msg = "今天是" + str(month) + "月" + str(date) + "号周" + str(weekcn) + "呀！ 快起床搬砖！ 嘻嘻，骗你的呀，今天调休呢"

            await self.api.send_group_msg(group_id=690925851, message=new_msg)
        async def get_Himg():
            self.Himg=getRecentYandeImgUrl(self)

        # 保留此接口作为每日晚安任务
        @scheduler.scheduled_job('cron', hour='23', minute='55')
        async def good_night():
            now = time.time()
            local_time = time.localtime(now)
            # 查询节假日API，决定动作模式
            date_format_localtime = time.strftime('%Y%m%d', local_time)
            url = "http://tool.bitefu.net/jiari/?d=" + date_format_localtime + "&info=1"
            response = requests.request("GET", url).json()
            week = response["week2"] # extract 信息

            if week == "5" or week == "6":
                new_msg = "今天是周末？ 好吧那... 是可以晚一点睡啦，但是不要太晚哦！"
            else:
                new_msg = "时间不早了，主人请早点休息，这样才能精神饱满地迎接新的一天呢~"
            await self.api.send_group_msg(group_id=690925851, message=new_msg)
            
    async def execute_async(self, ctx: Dict[str, Any]) -> Union[None, bool, str]:
        '''
        每次bot接收有效消息时触发

        参数ctx 具体格式见：https://cqhttp.cc/docs/#/Post
        '''
        # 注意：这是一个异步函数，禁止使用阻塞操作（比如requests）

        # 如果需要使用，请注释掉下面一行
        # return
        
        cmd = ctx['raw_message']

        if cmd.find('苟利国家生死以') != -1:
            return "岂因祸福避趋之"
        # if cmd.find('你妈死了') != -1 or cmd.find('nmsl') != -1:
        #     reply=requests.get("https://nmsl.shadiao.app/api.php?level=min").text
        #     reply=ab.str2abs(reply)
        #     return reply

        if cmd.find('妈') != -1:
            reply=requests.get("https://v1.hitokoto.cn?c=a").json()
            return reply['hitokoto']
        
        if cmd.find('色图') != -1 :
            print('获取色图')
            try:
                res=requests.get('https://api.ixiaowai.cn/api/api.php?return=json').text
                res=res.split(',')[1].split(':')
                reply=(res[1]+':'+res[2]).replace('\\','')
            except json.JSONDecodeError as e:
                print(e)
                reply = '获取图片失败'
            return reply

        # 图灵机器人API消息回复
        if cmd.find('1453766088') != -1 and cmd.find('CQ:at') != -1:
            msg = re.sub(r'^\[[a-zA-Z,:=\w]*\]','',cmd)
            payload["perception"]["inputText"]["text"]=msg 
            payload["userInfo"]["apiKey"] = apiKey[random.randint(0,4)] 
            # apiUrl='http://api.qingyunke.com/api.php?key=free&appid=0&msg='+msg
            reply = requests.post("http://openapi.tuling123.com/openapi/api/v2",json=payload,headers=headers).json()['results'][0]['values']['text']
            return reply
        
        if cmd.find('涩图') != -1:
            index = random.randint(0,39)
            reply = self.Himg[index]
            return reply
        
        if cmd.find('谢谢茄子') != -1:
            picnum=random.randint(1,2638)
            url = 'http://106.52.133.22:8070/'+str(picnum)+'.jpg'
            return url

        # 返回布尔值：是否阻止后续插件（返回None视作False）
        return False
