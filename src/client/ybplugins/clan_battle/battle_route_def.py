import asyncio
import logging
import os
import random
import re
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin

import peewee
from aiocqhttp.api import Api
from apscheduler.triggers.cron import CronTrigger
from quart import (Quart, jsonify, make_response, redirect, request, session,
                   url_for)

from ..ybdata import (Clan_challenge, Clan_group, Clan_member, Clan_subscribe,
                      User)

from .util import atqq, pcr_datetime, pcr_timestamp, timed_cached_func

_logger = logging.getLogger(__name__)


# scar额外添加的api
def record_api_helper(
        self,
        group_id
):
    group = Clan_group.get_or_none(group_id=group_id)
    d, _ = pcr_datetime(group.game_server)
    # 获取出刀记录 其中1590379200为时间戳，需要动态获取
    report = self.get_report(
        group_id,
        None,
        None,
        pcr_datetime(group.game_server, 1590379200)[0],
    )
    return jsonify(
        code=30,
        members=self.get_member_list(group_id),
        challenge=report,
        today=d
    )
