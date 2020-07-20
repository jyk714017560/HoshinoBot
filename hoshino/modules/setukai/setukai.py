import threading

from nonebot import on_command

from hoshino.typing import *
from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter

from .setumaster import SetuMaster



sv = Service('setu', manage_priv=priv.SUPERUSER, enable_on_default=False, visible=False)
setu_limit = DailyNumberLimiter(25)
lmt = FreqLimiter(15)

SETU_EXCEED_NOTICE = '你今天冲的太多辣，欢迎明早5点后再来！'


# proxies = {
#     'https':'socks5://127.0.0.1:10808'
# }
# session.proxies = proxies

sm = SetuMaster()
p = threading.Thread(target=sm.setu_producer, args=(sv,))
p.start()


async def check_setu_num(bot, ev: CQEvent):
    if not setu_limit.check(ev.user_id):
        await bot.finish(SETU_EXCEED_NOTICE, at_sender=True)


@sv.on_fullmatch(('色图测试','瑟图测试','涩图测试'))
async def setu_one(bot, ev: CQEvent):
    
    if not lmt.check(ev.user_id):
        await bot.send(f'乖，要懂得节制噢，涩图冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(ev.user_id)

    await check_setu_num(bot, ev)
    setu_limit.increase(ev.user_id, 1)

    setu = sm.setu_consumer(sv)
    await bot.send(setu)

