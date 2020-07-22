from hoshino.typing import *
from hoshino import Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter

from .setumaster import setu_consumer

sv = Service('setu', visible=False)
_nlmt = DailyNumberLimiter(25)
_flmt = FreqLimiter(15)

SETU_EXCEED_NOTICE = '你今天冲的太多辣，欢迎明早5点后再来！'

@sv.on_fullmatch(('色图', '瑟图', '涩图'))
async def setu_one(bot, ev: CQEvent):
    
    if not _flmt.check(ev.user_id):
        await bot.send(ev, f'乖，要懂得节制噢，涩图冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
        return
    if not _nlmt.check(ev.user_id):
        await bot.send(ev, SETU_EXCEED_NOTICE, at_sender=True)
        return
    _flmt.start_cd(ev.user_id)
    _nlmt.increase(ev.user_id, 1)

    msg = setu_consumer()
    await bot.send(ev, msg)

