import random

from nonebot import on_command

from hoshino import R, Service, priv, util
from hoshino.typing import *


# basic function for debug, not included in Service('chat')
@on_command('zai?', aliases=('在?', '在？', '在吗', '在么？', '在嘛', '在嘛？','佩可在？'), only_to_me=True)
async def say_hello(session):
    await session.send('[CQ:face,id=203]はい！私はいつも貴方の側にいますよ！')


sv = Service('chat', visible=False)

@sv.on_fullmatch('沙雕机器人')
async def say_sorry(bot, ev):
    await bot.send(ev, 'ごめんなさい！嘤嘤嘤(〒︿〒)')


@sv.on_fullmatch(('老婆', 'waifu', 'laopo'), only_to_me=True)
async def chat_waifu(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, R.img('laopo.jpg').cqcode)
    else:
        await bot.send(ev, 'mua~')


@sv.on_fullmatch('老公', only_to_me=True)
async def chat_laogong(bot, ev):
    await bot.send(ev, '你给我滚！', at_sender=True)


@sv.on_fullmatch('mua', only_to_me=True)
async def chat_mua(bot, ev):
    await bot.send(ev, '笨蛋~', at_sender=True)


@sv.on_fullmatch('来点星奏')
async def seina(bot, ev):
    await bot.send(ev, R.img('星奏.png').cqcode)


@sv.on_fullmatch(('我有个朋友说他好了', '我朋友说他好了', ))
async def ddhaole(bot, ev):
    await bot.send(ev, '那个朋友是不是你弟弟？')


@sv.on_fullmatch('我好了')
async def nihaole(bot, ev):
    await bot.send(ev, '不许好，憋回去！')
    await util.silence(ev, 60)


# ============================================ #


@sv.on_keyword(('确实', '有一说一', 'u1s1', 'yysy'))
async def chat_queshi(bot, ctx):
    if random.random() < 0.05:
        await bot.send(ctx, R.img('确实.jpg').cqcode)


@sv.on_keyword(('会战'))
async def chat_clanba(bot, ctx):
    if random.random() < 0.02:
        await bot.send(ctx, R.img('我的天啊你看看都几度了.jpg').cqcode)


@sv.on_keyword(('内鬼'))
async def chat_neigui(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img('内鬼.png').cqcode)

nyb_player = f'''{R.img('newyearburst.gif').cqcode}
正在播放：New Year Burst
──●━━━━ 1:05/1:30
⇆ ㅤ◁ ㅤㅤ❚❚ ㅤㅤ▷ ㅤ↻
'''.strip()

@sv.on_keyword(('春黑', '新黑'))
async def new_year_burst(bot, ev):
    if random.random() < 0.02:
        await bot.send(ev, nyb_player)

qks_url = ["granbluefantasy.jp"]
qksimg = R.img('anti.jpg').cqcode
@sv.on_keyword(qks_url)
async def qks_keyword(bot, ev):
    msg = f'骑空士爪巴\n{qksimg}'
    await bot.send(ev, msg, at_sender=True)
    await util.silence(ev, 60)


@sv.on_keyword(('炼铜'))
async def chat_liantong(bot, ev):
    await bot.send(ev, R.record('hentai.wav').cqcode)

@sv.on_keyword(('pahu'))
async def chat_pahu(bot, ev):
    return
    await bot.send(ev, R.record(f"pahu/{random.randint(1, 3)}.m4a").cqcode)

@sv.on_prefix('echo')
async def echo(bot, ev):
    msg = ev.message.extract_plain_text().strip()
    await bot.send(ev, msg)

@sv.on_prefix('佩可说话')
async def text_to_voice(bot, event):
    msg = event.message.extract_plain_text().strip()
    if not msg:
        return
    tts = MessageSegment(type_='tts', data={'text': msg})
    await bot.send(event, tts)



