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

import numpy as np
from aiocqhttp.api import Api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart

this_season = np.zeros(15001)
all_season = np.zeros(15001)

this_season[1:11] = 50
this_season[11:101] = 10
this_season[101:201] = 5
this_season[201:501] = 3
this_season[501:1001] = 2
this_season[1001:2001] = 2
this_season[2001:4000] = 1
this_season[4000:8000:100] = 50
this_season[8100:15001:100] = 15

all_season[1:11] = 500
all_season[11:101] = 50
all_season[101:201] = 30
all_season[201:501] = 10
all_season[501:1001] = 5
all_season[1001:2001] = 3
all_season[2001:4001] = 2
all_season[4001:7999] = 1
all_season[8100:15001:100] = 30

class mining_query:
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

        # # 注册定时任务，详见apscheduler文档
        # @scheduler.scheduled_job('cron', hour=8)
        # async def good_morning():
        #     await self.api.send_group_msg(group_id=123456, message='早上好')

        # # 注册web路由，详见flask与quart文档
        # @app.route('/is-bot-running', methods=['GET'])
        # async def check_bot():
        #     return 'yes, bot is running'

    async def execute_async(self, ctx: Dict[str, Any]) -> Union[None, bool, str]:
        '''
        每次bot接收有效消息时触发

        参数ctx 具体格式见：https://cqhttp.cc/docs/#/Post
        '''
        # 注意：这是一个异步函数，禁止使用阻塞操作（比如requests）

        # 如果需要使用，请注释掉下面一行
        # return
        cmd_raw = ctx['raw_message']
        value = []
        cmd = []
        for i in cmd_raw:
            if i.isdigit():
                value.append(i)
            elif (i != ' '):
                cmd.append(i)

        words_list = ['挖矿', 'jjc钻石', '竞技场钻石', 'jjc钻石查询', '竞技场钻石查询']
        words_set = set(words_list)

        cmd_txt = ''.join(cmd)
        print(cmd_txt)

        if cmd_txt in words_set:

            if not value:
                new_msg = f'请输入"挖矿 纯数字最高排名"'
                await self.api.send_group_msg(group_id=690925851, message=new_msg)
                return

            value_tmp = [str(integer) for integer in value]
            value = ''.join(value_tmp)

            rank = int(value)
            rank = np.clip(rank, 1, 15001)

            s_all = int(all_season[1:rank].sum())
            s_this = int(this_season[1:rank].sum())

            # 调用api发送消息，详见cqhttp文档
            new_msg = f"最高排名奖励还剩 {s_this} 钻\n历届最高排名还剩 {s_all} 钻"
            await self.api.send_group_msg(group_id=690925851, message=new_msg)

            # 返回字符串：发送消息并阻止后续插件
            return

        # 返回布尔值：是否阻止后续插件（返回None视作False）
        return False
