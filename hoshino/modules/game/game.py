import os
import random
import re
import asyncio
from collections import defaultdict

from PIL import Image

import hoshino
from hoshino.typing import *
from hoshino import Service, R, logger
from hoshino.modules.priconne import chara
from hoshino.util import pic2b64

sv = Service('game', help_='[猜语音] 猜猜随机的语音来自哪位角色\n[猜卡面] 猜猜截取的卡面来自哪位角色', bundle='pcr娱乐', enable_on_default=True, visible=True)

GAME_POOL = ('voiceguess', 'cardguess', 'baseball', 'racing')
ONE_TURN_TIME = 30

_group_game = {}
_group_game = defaultdict(lambda: '', _group_game)
_group_winner = {}
_group_winner = defaultdict(lambda: [], _group_winner)
_group_parameter = {}

voicepath = os.path.join(hoshino.config.RES_DIR, 'record/title')
cardpath = os.path.join(hoshino.config.RES_DIR, 'img/priconne/card/')

GAME_NAME_TIP = '请选择以下小游戏\n> 猜语音\n> 猜卡面\n> 棒球（开发中）\n> 赛马（开发中）'
@sv.on_fullmatch(('小游戏'))
async def game_start(bot, ev: CQEvent):
    
    gid = str(ev.group_id)
    if _group_game[gid]:
        await bot.send(ev, '游戏进行中,好孩子要学会耐心等候哦~')
        return
    await bot.send(ev, GAME_NAME_TIP, at_sender=True)
    

@sv.on_fullmatch(('猜语音'))
async def voiceguess(bot, ev: CQEvent):

    await bot.send(ev, '语音维护中,暂不开放 (•̀へ•╮)')
    return

    if ev['message_type'] != 'group':
        await bot.send(ev, '小游戏仅支持群组游玩，好孩子要学会和伙伴一起玩哦~')
        return
    
    try:
        gid = str(ev.group_id)
        if _group_game[gid]:
            await bot.send(ev, '游戏进行中,好孩子要学会耐心等候哦~')
            return
        _group_game[gid] = 'voiceguess'
        voice = random.choice(os.listdir(voicepath))
        voice_id = int('1' + re.compile(r'^vo_title_(customize_)?(\d{4}).*').match(voice).group(2)[-3:])
        c = chara.fromid(voice_id)
        _group_parameter[gid] = voice_id

        await bot.send(ev, f'猜猜这个语音来自哪位角色? ({ONE_TURN_TIME}s后公布答案)')
        await bot.send(ev, R.record(f"title/{voice}").cqcode)
        await asyncio.sleep(ONE_TURN_TIME)
        msg = [f'锵锵，正确答案是: \n{c.icon.cqcode}{c.name}']
        if not _group_winner[gid]:
            msg.append('很遗憾，没有人答对呢~')
            await bot.send(ev, '\n'.join(msg))
        else:
            _group_winner[gid] = list(set(_group_winner[gid]))
            msg.append(f'ヤバイですね！一共有{len(_group_winner[gid])}人答对，他们是:')
            for n in _group_winner[gid]:
                msg.append(str(n))
            await bot.send(ev, '\n'.join(msg))
    except Exception as e:
        logger.error(f'{e}')
        await bot.send(ev, '佩可似乎出错了o(╥﹏╥)o,快联系主人来看看吧~')
    del _group_game[gid]
    del _group_winner[gid]


@sv.on_fullmatch(('猜卡面'))
async def cardguess(bot, ev: CQEvent):

    if ev['message_type'] != 'group':
        await bot.send(ev, '小游戏仅支持群组游玩，好孩子要学会和伙伴一起玩哦~')
        return
    
    try:
        gid = str(ev.group_id)
        if _group_game[gid]:
            await bot.send(ev, '游戏进行中,好孩子要学会耐心等候哦~')
            return
        _group_game[gid] = 'cardguess'
        card = random.choice(os.listdir(cardpath))
        card_id = int(re.compile(r'^card_(\d{4}).*').match(card).group(1))
        c = chara.fromid(card_id)
        _group_parameter[gid] = card_id

        img = Image.open(os.path.join(cardpath, card))
        h = img.height
        w = img.width
        box = random.choice([(0, 0, 200, 200), (w - 200, 0, w, 200), (0, h - 200, 200, h), (w - 200, h - 200, w, h)])
        res = img.crop(box)
        res = pic2b64(res)
        res = MessageSegment.image(res)

        await bot.send(ev, f'猜猜这张卡面来自哪位角色? ({ONE_TURN_TIME}s后公布答案)\n{res}')
        await asyncio.sleep(ONE_TURN_TIME)
        imgcard = R.img(f'priconne/card/{card}').cqcode
        msg = [f'锵锵，正确答案是: \n{imgcard}{c.name}']
        if not _group_winner[gid]:
            msg.append('很遗憾，没有人答对呢~')
            await bot.send(ev, '\n'.join(msg))
        else:
            _group_winner[gid] = list(set(_group_winner[gid]))
            msg.append(f'ヤバイですね！一共有{len(_group_winner[gid])}人答对，他们是:')
            for n in _group_winner[gid]:
                msg.append(str(n))
            await bot.send(ev, '\n'.join(msg))
    except Exception as e:
        logger.error(f'{e}')
        await bot.send(ev, '佩可似乎出错了o(╥﹏╥)o,快联系主人来看看吧~')
    del _group_game[gid]
    del _group_winner[gid]


@sv.on_fullmatch(('棒球'))
async def baseball(bot, ev: CQEvent):
    return
    if ev['message_type'] != 'group':
        await bot.send(ev, '小游戏仅支持群组游玩，好孩子要学会和伙伴一起玩哦~')
        return


@sv.on_fullmatch(('赛马'))
async def racing(bot, ev: CQEvent):
    return
    if ev['message_type'] != 'group':
        await bot.send(ev, '小游戏仅支持群组游玩，好孩子要学会和伙伴一起玩哦~')
        return


@sv.on_message()
async def input_chara_name(bot, ev: CQEvent):

    gid = str(ev.group_id)
    if not _group_game[gid]:
        return

    if not ev['message'][0]['type'] == 'text':
        return
    
    if _group_game[gid] == 'voiceguess' or _group_game[gid] == 'cardguess':
        name = ev.message.extract_plain_text().strip()
        _id = chara.name2id(name)
        if _id == _group_parameter[gid]:
            _group_winner[gid].append(ev['sender']['nickname'])
        else:
            return
    else:
        return
