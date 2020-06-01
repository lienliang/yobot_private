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
import time
from typing import Any, Dict, Union

from aiocqhttp.api import Api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart
import requests

from ybplugins import ybdata
from ybplugins import clan_battle


class auto_reminder:

    # 获取出刀记录
    def get_challenge_record(self,group_id):
        d, _ = clan_battle.pcr_datetime('cn')
        # 获取时间戳
        now = time.localtime(time.time())
        time_str = str(now.tm_year) + ',' + str(now.tm_mon) + ',' + str(now.tm_mday) + ',' + str(12)
        sp = time.strptime(time_str, "%Y,%m,%d,%H")
        stamp = int(time.mktime(sp))
        # 获取当天的出刀记录
        challenge = clan_battle.ClanBattle.get_report(
            None,
            group_id,
            None,
            None,
            clan_battle.pcr_datetime('cn', stamp)[0],
        )

        return challenge

    # 获取成员列表
    def get_member_list(self, group_id):
        return clan_battle.ClanBattle.get_member_list(None, group_id)

    # 获取未出够3刀的成员qqid
    def get_non_record_qqid(self, group_id):
        member_list = self.get_member_list(group_id)
        challenge_list = self.get_challenge_record(group_id)
        challenge = {}
        for item in member_list:
            challenge[item['qqid']] = 0

        for item in challenge_list:
            if not item['is_continue']:
                challenge[item['qqid']] += 1

        non_record_qqid_list = []
        for key in challenge:
            if challenge[key] < 3:
                non_record_qqid_list.append(key)

        return non_record_qqid_list

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
        # return

        # 这是来自yobot_config.json的设置，如果需要增加设置项，请修改default_config.json文件
        self.setting = glo_setting

        # 这是cqhttp的api，详见cqhttp文档
        self.api = bot_api

        # 催刀模式
        @scheduler.scheduled_job('cron', hour='0,1,21,23', minute='25') # 更加人性化的设定，仅在当天九点后每隔一到两小时提醒一次出刀
        async def reminder():
            # 参数为群号
            qqid = self.get_non_record_qqid(690925851)
            print(qqid)
            msg = "可可萝提醒您，主人您今天还没出够3刀 0x0"
            for item in qqid:
                await self.api.send_private_msg(user_id=item, message=msg)



    async def execute_async(self, ctx: Dict[str, Any]) -> Union[None, bool, str]:
        '''
        每次bot接收有效消息时触发

        参数ctx 具体格式见：https://cqhttp.cc/docs/#/Post
        '''
        # 注意：这是一个异步函数，禁止使用阻塞操作（比如requests）

        # 如果需要使用，请注释掉下面一行
        return
        '''
        cmd = ctx['raw_message']
        if cmd == '你好':

            # 调用api发送消息，详见cqhttp文档
            # await self.api.send_private_msg(
            #     user_id=123456, message='收到问好')

            # 返回字符串：发送消息并阻止后续插件
            return '世界'

        # 返回布尔值：是否阻止后续插件（返回None视作False）
        return False '''
