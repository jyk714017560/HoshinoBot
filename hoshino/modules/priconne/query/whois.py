from hoshino.typing import CQEvent, MessageSegment
from hoshino.util import FreqLimiter

from .. import chara
from . import sv

lmt = FreqLimiter(5)

@sv.on_suffix(('是谁', '是誰'))
@sv.on_prefix(('谁是', '誰是'))
async def whois(bot, ev: CQEvent):
    uid = ev.user_id
    if not lmt.check(uid):
        await bot.send(ev, f'兰德索尔花名册冷却中(剩余 {int(lmt.left_time(uid)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(uid)

    name = ev.message.extract_plain_text().strip()
    if not name:
        await bot.send(ev, '请发送"谁是"+别称，如"谁是佩可"')
        return
    id_ = chara.name2id(name)
    confi = 100
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
    c = chara.fromid(id_)
    
    msg = ''
    if confi < 100:
        msg = f'兰德索尔似乎没有叫"{name}"的人...'
        await bot.send(ev, msg)
        msg = f'您有{confi}%的可能在找{guess_name} '

    if confi > 60:
        msg += f'{c.icon.cqcode} {c.name}'
        await bot.send(ev, msg)

@sv.on_suffix(('卡面'))
async def fullcard(bot, ev: CQEvent):
    uid = ev.user_id
    if not lmt.check(uid):
        await bot.send(ev, f'兰德索尔花名册冷却中(剩余 {int(lmt.left_time(uid)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(uid)

    name = ev.message.extract_plain_text().strip()
    if not name:
        await bot.send(ev, '请发送别称+"卡面"，如"佩可卡面"')
        return
    id_ = chara.name2id(name)
    confi = 100
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
    c = chara.fromid(id_)
    
    msg = ''
    if confi < 100:
        msg = f'兰德索尔似乎没有叫"{name}"的人...'
        await bot.send(ev, msg)
        msg = f'您有{confi}%的可能在找{guess_name} '

    if confi > 60:
        msg += f'{c.card.cqcode}'
        await bot.send(ev, msg)
