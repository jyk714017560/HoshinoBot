from hoshino.typing import *
from hoshino import Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter

from .setumaster import *
from .discernmaster import setu_distinguish

import random
from datetime import datetime

sv = Service('setu', visible=False)
_nlmt = DailyNumberLimiter(15)
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

    msg = await setu_consumer()
    await bot.send(ev, msg)
    if random.random() < 0.02:
        await bot.send(ev, f"{R.img('色图.gif').cqcode}")


@sv.on_fullmatch('涩图重启')
async def reset_setu(bot, ev: CQEvent):

    if not priv.check_priv(ev, priv.ADMIN):
        return
    msg = setu_reset()
    await bot.send(ev, msg)


async def setu_discern(bot, ev):

    m = ev.message[0]
    if m.type == 'image':
        img_url = m.data['url']
        confidence = await setu_distinguish(img_url)
        msg = []
        msg.append(f'色图指数：{confidence}%')
        if not confidence:
            if random.random() < 0.02:
                await bot.send(ev, '诶嘿~')
            return
        elif confidence < 30:
            if random.random() < 0.05:
                await bot.send(ev, '哦呐嘎憋锅憋锅~')
            return
        elif confidence < 50:
            if random.random() < 0.10:
                msg.append('就这，不够色!')
            elif random.random() < 0.20:
                msg.append('一般，多来点！')
        elif confidence < 90:
            msg.append('警察叔叔就是这个人o(╥﹏╥)o')
        else:
            msg.append('群要没了o(╥﹏╥)o')
        await bot.send(ev, '\n'.join(msg))


@sv.on_message()
async def setu_discern_group(bot, ev: CQEvent):
    #仅开放七曜群和塞姆利亚群
    if ev.group_id == 1058019377 or ev.group_id == 602138153:
        now = datetime.now()
        if 21 <= now.hour <= 23:
            if len(ev.message) == 1:
                await setu_discern(bot, ev)


@sv.on_prefix('识图')
async def setu_discern_master(bot, ev: CQEvent):
    #测试用
    if not priv.check_priv(ev, priv.ADMIN):
        return
    await setu_discern(bot, ev)




            


            

