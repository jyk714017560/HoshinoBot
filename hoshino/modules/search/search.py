import os
import time
from collections import defaultdict
import asyncio

from nonebot import MessageSegment
from hoshino import Service, priv, util
from hoshino.typing import *
from hoshino.util import DailyNumberLimiter, FreqLimiter

from .searchmaster import SearchMaster

try:
    import ujson as json
except:
    import json

sv = Service('search', help_='sv_help', bundle='pcr娱乐', enable_on_default=False, visible=False, manage_priv=priv.OWNER)
search_limit = DailyNumberLimiter(25)
lmt = FreqLimiter(5)

SEARCH_EXCEED_NOTICE = f'你今天搜的图太多辣，欢迎明早5点后再来！'
SIMILARITY = 50

_search_user = {}
_search_user = defaultdict(lambda: False, _search_user)


async def check_search_num(bot, ev: CQEvent):
    if not search_limit.check(ev.user_id):
        await bot.finish(ev, SEARCH_EXCEED_NOTICE, at_sender=True)


@sv.on_prefix('佩可搜图')
async def search_mode_on(bot, ev: CQEvent):
    
    uid = str(ev.user_id)
    await check_search_num(bot, ev)

    if _search_user[uid]:
        await bot.finish(ev, '您已经在搜图模式下啦！\n如想退出搜索模式请发送“谢谢佩可”', at_sender=True)
        
    _search_user[uid] = True
    await bot.send(ev, '了解～请发送图片吧！\n如想退出搜索模式请发送“谢谢佩可”', at_sender=True)
    await asyncio.sleep(60)
    if _search_user[uid]:
        _search_user[uid] = False
        await bot.send(ev, '由于超时，已为您自动退出搜图模式，以后要记得说“谢谢佩可”来退出搜图模式噢', at_sender=True)


@sv.on_prefix('谢谢佩可')
async def search_mode_off(bot, ev: CQEvent):
    
    uid = str(ev.user_id)

    if not _search_user[uid]:
        await bot.finish(ev, 'にゃ～')

    _search_user[uid] = False
    await bot.send(ev, '不用谢～', at_sender=True)


@sv.on_message()
async def search_pic(bot, ev: CQEvent):

    uid = str(ev.user_id)
    if not _search_user[uid]:
        return

    if not ev['message'][0]['type'] == 'image':
        return

    await check_search_num(bot, ev)
    search_limit.increase(ev.user_id, 1)
  
    sm = SearchMaster(ev['message'][0]['data']['url'])
    saucenao, ascii2d_disable = sm.saucenao()
    await bot.send(ev, saucenao)

    if ascii2d_disable:
        return
    color, bovw = sm.ascii2d()
    await bot.send(ev, color)
    await bot.send(ev, bovw)




@sv.on_prefix('搜图')
async def search_pic_one(bot, ev: CQEvent):
    
    if not lmt.check(ev.user_id):
        await bot.send(ev, f'乖，要懂得节制噢，搜图冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(ev.user_id)

    await check_search_num(bot, ev)
    search_limit.increase(ev.user_id, 1)

    img_url = []
    for m in ev.message:
        if m.type == 'image':
            img_url.append(m.data['url'])

    if not img_url:
        await bot.send(ev, '必须要发送"搜图"+图片我才能帮你找噢_(:3」」')
        return

    for u in img_url:
        sm = SearchMaster(u)
        saucenao, ascii2d_disable = sm.saucenao()
        await bot.send(ev, saucenao)

        if ascii2d_disable:
            continue
        color, bovw = sm.ascii2d()
        await bot.send(ev, color)
        await bot.send(ev, bovw)

        
    

