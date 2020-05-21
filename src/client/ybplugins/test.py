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

class Test:
    id_arr:[]
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

        # 如果需要启用，请注释掉下面一行
        #return

        # 这是来自yobot_config.json的设置，如果需要增加设置项，请修改default_config.json文件
        self.setting = glo_setting

        # 这是cqhttp的api，详见cqhttp文档
        self.api = bot_api

        

        def get_id(self):
            print('获取日榜ID中')
            rankByDayHtml=requests.get('https://yande.re/post/popular_recent').text
            regex=re.compile('"id":\d{6}')
            imgIdArr=re.findall(regex,rankByDayHtml)
            for index in range(len(imgIdArr)):
                imgIdArr[index]=imgIdArr[index].replace('"id":','')
            print('获取日榜ID成功')
            return imgIdArr
        # self.id_arr=get_id(self)   
        # # 注册定时任务，详见apscheduler文档
        @scheduler.scheduled_job('interval', minutes=60)
        # async def get_id_schedule():
        #     self.id_arr=get_id(self)
        async def good_morning():
            now = time.time()
            local_time = time.localtime(now)
            date_format_localtime = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
            test_msg = "这是妈在测试,时间戳为："+date_format_localtime
            await self.api.send_group_msg(group_id=690925851, message=test_msg)
        

        # # 注册web路由，详见flask与quart文档
        # @app.route('/is-bot-running', methods=['GET'])
        # async def check_bot():
        #     return 'yes, bot is running'

        #获取日榜图片ID
    

    async def execute_async(self, ctx: Dict[str, Any]) -> Union[None, bool, str]:
        '''
        每次bot接收有效消息时触发

        参数ctx 具体格式见：https://cqhttp.cc/docs/#/Post
        '''
        # 注意：这是一个异步函数，禁止使用阻塞操作（比如requests）

        # 如果需要使用，请注释掉下面一行
        # return

        cmd = ctx['raw_message']

        if cmd.find('你妈死了') != -1 or cmd.find('nmsl') != -1:
            reply=requests.get("https://nmsl.shadiao.app/api.php?level=max").text
            reply=ab.str2abs(reply)
            return reply

        if cmd.find('妈') != -1 and cmd.find('你妈死了') == -1:
            reply=requests.get("https://v1.hitokoto.cn/?c=i").json()

            # 调用api发送消息，详见cqhttp文档
            # await self.api.send_private_msg(
            #     user_id=740984027, message='收到问好')

            # 返回字符串：发送消息并阻止后续插件
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
        
        if cmd.find('1453766088') != -1 and cmd.find('CQ:at') != -1:
            
            msg = re.sub(r'^\[[a-zA-Z,:=\w]*\]','',cmd)
            apiUrl='http://api.qingyunke.com/api.php?key=free&appid=0&msg='+msg
            try:
                reply =requests.get(apiUrl).json()['content']
                reply=ab.str2abs(reply)
            except json.JSONDecodeError as e:
                print(e)
                reply = msg
            return reply
          
        
        # 返回布尔值：是否阻止后续插件（返回None视作False）
        return False
