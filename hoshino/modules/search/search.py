import os
import time
from collections import defaultdict
import asyncio

import hoshino
from hoshino import Service, priv, util
from hoshino.typing import *
from hoshino.util import DailyNumberLimiter, FreqLimiter

from .searchmaster import SearchMaster
from .pixivmaster import *
from .musicmaster import *

try:
    import ujson as json
except:
    import json

sv = Service('search', help_='[搜图+图片] 以图搜图\n[搜图+关键字] 关键字搜图\n[点歌+关键字] 关键字点歌', bundle='pcr娱乐', enable_on_default=True, visible=True)
search_limit = DailyNumberLimiter(15)
lmt = FreqLimiter(15)

SEARCH_EXCEED_NOTICE = f'你今天搜的图太多辣，欢迎明早5点后再来！'

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
    color_ret = await bot.send(ev, color)
    bovw_ret = await bot.send(ev, bovw)
    await asyncio.sleep(60)
    await delete_msg(ev, color_ret)
    await delete_msg(ev, bovw_ret)


@sv.on_prefix('搜图')
async def search_pic_one(bot, ev: CQEvent):
    
    if not lmt.check(ev.user_id):
        await bot.send(ev, f'乖，要懂得节制噢，搜图冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(ev.user_id)

    await check_search_num(bot, ev)
    search_limit.increase(ev.user_id, 1)

    m = ev.message[0]
    if m.type == 'image':
        img_url = ev.message[0].data['url']
        sm = SearchMaster(img_url)
        saucenao, ascii2d_disable = sm.saucenao()
        await bot.send(ev, saucenao)

        if ascii2d_disable:
            return
        color, bovw = sm.ascii2d()
        color_ret = await bot.send(ev, color)
        bovw_ret = await bot.send(ev, bovw)
        await asyncio.sleep(60)
        await delete_msg(ev, color_ret)
        await delete_msg(ev, bovw_ret)

    elif m.type == 'text':
        keyword = ev.message[0].data['text']
        if not keyword:
            await bot.send(ev, ' 必须要发送指令我才能帮你找噢\n> 搜图+图片: 以图搜图\n> 搜图+关键字: 关键字搜图\n> 功能优化中……_(:3」」', at_sender=True)
            return
        try:
            t = PixivicThread(pixivic_keyword, args=keyword)
            t.start()
            t.join()
            msg = t.get_result()
            await bot.send(ev, msg, at_sender=True)
        except:
            await bot.send(ev, '由未知错误导致搜图失败QAQ', at_sender=True)

    else:
        await bot.send(ev, ' 必须要发送指令我才能帮你找噢\n> 搜图+图片: 以图搜图\n> 搜图+关键字: 关键字搜图\n> 功能优化中……_(:3」」', at_sender=True)
        return

async def delete_msg(ev: CQEvent, ret):
    try:
        await hoshino.get_bot().delete_msg(self_id=ev.self_id, message_id=ret['message_id'])
    except:
        return


@sv.on_prefix('点歌')
async def search_music(bot, ev: CQEvent):
    if not lmt.check(ev.user_id):
        await bot.send(ev, f'乖，要懂得节制噢，点歌冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(ev.user_id)

    if not search_limit.check(ev.user_id):
        await bot.send(ev, '你今天点的歌太多辣，欢迎明早5点后再来！', at_sender=True)
        return
    search_limit.increase(ev.user_id, 1)

    m = ev.message[0]
    if m.type == 'text':
        keyword = ev.message[0].data['text']
        if not keyword:
            await bot.send(ev, ' 必须要发送指令我才能帮你找噢\n> 点歌+关键字: 关键字点歌\n> 功能优化中……_(:3」」', at_sender=True)
            return
        try:
            t = MusicThread(music_keyword, args=keyword)
            t.start()
            t.join()
            msg = t.get_result()
            await bot.send(ev, msg, at_sender=True)
        except:
            await bot.send(ev, '由未知错误导致点歌失败QAQ', at_sender=True)


@sv.on_rex(r'^来[份点张](.{1,20})[涩色瑟]图$')
async def search_pic_keyword(bot, ev: CQEvent):
    
    if ev.group_id == 1058019377 or ev.group_id == 602138153:      
        if not lmt.check(ev.user_id):
            await bot.send(ev, f'乖，要懂得节制噢，搜图冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
            return
        lmt.start_cd(ev.user_id)

        await check_search_num(bot, ev)
        search_limit.increase(ev.user_id, 1)

        keyword = ev['match'].group(1)
        if not keyword:
            await bot.send(ev, ' 必须要发送指令我才能帮你找噢\n> 搜图+图片: 以图搜图\n> 搜图+关键字: 关键字搜图\n> 功能优化中……_(:3」」', at_sender=True)
            return
        try:
            t = PixivicThread(pixivic_keyword, args=keyword)
            t.start()
            t.join()
            msg = t.get_result()
            await bot.send(ev, msg, at_sender=True)
        except:
            await bot.send(ev, '由未知错误导致搜图失败QAQ', at_sender=True)

