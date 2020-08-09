import os
import random
import re
import asyncio
from collections import defaultdict

import hoshino
from hoshino.typing import *
from hoshino import Service, R
from hoshino.modules.priconne import chara

sv = Service('game', help_='猜语音 | 猜猜随机的语音来自哪位角色', bundle='pcr娱乐', enable_on_default=True, visible=True)

GAME_POOL = ('voiceguess', 'cardguess', 'baseball', 'racing')
ONE_TURN_TIME = 30

_group_game = {}
_group_game = defaultdict(lambda: '', _group_game)
_group_winner = {}
_group_winner = defaultdict(lambda: [], _group_winner)
_group_parameter = {}

voicepath = os.path.join(hoshino.config.RES_DIR, 'record/title')

GAME_NAME_TIP = '请选择以下小游戏\n> 猜语音\n> 猜卡面（开发中）\n> 棒球（开发中）\n> 赛马（开发中）'
@sv.on_fullmatch(('小游戏'))
async def game_start(bot, ev: CQEvent):
    
    gid = str(ev.group_id)
    if _group_game[gid]:
        bot.send(ev, '游戏进行中,好孩子要学会耐心等候哦~')
        return
    await bot.send(ev, GAME_NAME_TIP, at_sender=True)
    

@sv.on_fullmatch(('猜语音'))
async def voiceguess(bot, ev: CQEvent):
    try:
        gid = str(ev.group_id)
        if _group_game[gid]:
            bot.send(ev, '游戏进行中,好孩子要学会耐心等候哦~')
            return
    except:
        bot.send(ev, '小游戏仅支持群组游玩，好孩子要学会和伙伴一起玩哦~')
        return
    
    try:
        _group_game[gid] = 'voiceguess'
        voice = random.choice(os.listdir(voicepath))
        voice_id = int('1' + re.compile(r'^vo_title_(customize_)?(\d{4}).*').match(voice).group(2)[-3:])
        c = chara.fromid(voice_id)
        _group_parameter[gid] = voice_id

        await bot.send(ev, f'猜猜这个语音来自哪位角色? ({ONE_TURN_TIME}s后公布答案)')
        await bot.send(ev, R.record(voicepath, voice).cqcode)
        await asyncio.sleep(ONE_TURN_TIME)
        msg = [f'锵锵，正确答案是: {c.icon.cqcode}{c.name}']
        if not _group_winner[gid]:
            msg.append('很遗憾，没有人答对呢~')
            await bot.send(ev, '\n'.join(msg))
        else:
            msg.append(f'ヤバイですね！一共有{len(_group_winner[gid])}人答对，他们是:')
            msg.append(_group_winner[gid])
            await bot.send(ev, '\n'.join(msg))
    except:
        bot.send(ev, '佩可似乎出错了o(╥﹏╥)o,快联系主人来看看吧~')
    del _group_game[gid]
    del _group_winner[gid]



@sv.on_fullmatch(('猜卡面'))
async def cardguess(bot, ev: CQEvent):
    return


@sv.on_fullmatch(('棒球'))
async def baseball(bot, ev: CQEvent):
    return


@sv.on_fullmatch(('赛马'))
async def racing(bot, ev: CQEvent):
    return


@sv.on_message()
async def input_chara_name(bot, ev: CQEvent):

    try:
        gid = str(ev.group_id)
    except:
        return
    if not _group_game[gid]:
        return

    if not ev['message'][0]['type'] == 'text':
        return
    
    name = ev.message.extract_plain_text().strip()
    _id = chara.name2id(name)
    if _id == _group_parameter[gid]:
        _group_winner[gid].append(ev['sender']['nickname'])
    else:
        return
