from hoshino.typing import *
from hoshino import Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter

from .setumaster import setu_consumer, get_setu_keyword, get_pixivSuggestions

sv = Service('setu', visible=False)
_nlmt = DailyNumberLimiter(25)
_flmt = FreqLimiter(15)

SETU_EXCEED_NOTICE = '你今天冲的太多辣，欢迎明早5点后再来！'

@sv.on_rex(r'^来?[份点张]?[涩色瑟]图$')
async def setu_one(bot, ev: CQEvent):
    
    if not _flmt.check(ev.user_id):
        await bot.send(ev, f'乖，要懂得节制噢，涩图冷却中(剩余 {int(_flmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
        return
    if not _nlmt.check(ev.user_id):
        await bot.send(ev, SETU_EXCEED_NOTICE, at_sender=True)
        return
    _flmt.start_cd(ev.user_id)
    _nlmt.increase(ev.user_id, 1)

    # keyword = ev['match'].group(1)  if ev['match'].group(1) else ev['match'].group(2)

    # if keyword:
    #     _flmt.start_cd(ev.user_id,60)
    #     msg = await get_setu_keyword(keyword)
    #     await bot.send(ev, msg, at_sender=True)
    #     suggestion = await get_pixivSuggestions(keyword)
    #     if suggestion:
    #         await bot.send(ev, suggestion, at_sender=True)
    #     return

    msg = setu_consumer()
    await bot.send(ev, msg)

