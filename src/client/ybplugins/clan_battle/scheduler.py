from datetime import datetime
from .battle import ClanBattle


from typing import Any, Dict, List, Optional, Tuple, Union
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

from .typing import BossStatus, ClanBattleReport, Groupid, Pcr_date, QQid

@nonebot.scheduler.scheduled_job('interval', minutes=2)
async def _():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await ClanBattle.send_remind(group_id=Groupid,
                                     member_list=List[QQid],
                                     sender=QQid,
                                     send_private_msg=True)
    except CQHttpError:
        pass