import os
from io import BytesIO
import re
import requests
from PIL import Image, ImageDraw, ImageFont

import hoshino
from hoshino.typing import *
from hoshino import Service, R
from hoshino.util import pic2b64, FreqLimiter, DailyNumberLimiter

sv = Service('memegenerator', help_='', bundle='pcr娱乐', enable_on_default=True, visible=False)
fontPath = R.img('font/msyhbd.ttf').path
_nlmt = DailyNumberLimiter(15)
_flmt = FreqLimiter(15)
session = requests.session()

CONTROL_GROUP = 700
MEME_EXCEED_NOTICE = '佩可今天不想为你生成表情包啦，欢迎明早5点后再来！'

@sv.on_prefix('生成表情')
async def meme(bot, ev: CQEvent):
    if ev.message[0].type != 'text':
        await bot.send(ev, '必须要发送关键字才能生成表情噢\n> 生成表情+关键字+图片: 生成表情', at_sender=True)
        return
    keyword = ev.message[0].data['text']
    keyword=keyword.rstrip()

    if len(ev.message) < 2 or ev.message[1].type != 'image':
        await bot.send(ev, '必须要发送图片才能生成表情噢\n> 生成表情+关键字+图片: 生成表情', at_sender=True)
        return
    img_url = ev.message[1].data['url']

    if not _flmt.check(ev.user_id):
        await bot.send(ev, f'乖，要懂得节制噢，生成表情冷却中（剩余 {int(_flmt.left_time(ev.user_id)) + 1}秒）', at_sender=True)
        return
    if not _nlmt.check(ev.user_id):
        await bot.send(ev, MEME_EXCEED_NOTICE, at_sender=True)
        return
    _flmt.start_cd(ev.user_id)
    _nlmt.increase(ev.user_id, 1)

    #爬图片
    try:
        r = session.get(url=img_url, timeout=10)
    except:
        await bot.send(ev, '图片太大了惹_(:3」∠)_', at_sender=True)
        return
    try:
        img = Image.open(BytesIO(r.content))
    except:
        await bot.send(ev, '图片太大了惹_(:3」∠)_', at_sender=True)
        return

    #图片处理
    w, h = img.size[0],img.size[1]
    img_new = Image.new("RGB", (w, h + max(int(h / 5), 30)), "white")
    img_new.paste(img, (0, 0))

    imgFont = ImageFont.truetype(font=fontPath, size=max(int(h / 10), 15))
    textSize = imgFont.getsize(text=keyword)
    xy = ((w - textSize[0]) / 2, h + (max(int(h / 5), 30) - textSize[1]) / 2)
    draw = ImageDraw.Draw(img_new)
    draw.text(xy=xy, text=keyword, font=imgFont, fill='black')

    buf = BytesIO()
    img_new.save(buf, format='PNG')
    size = len(buf.getvalue()) / 1024
    while size > CONTROL_GROUP:
        width, height = img_new.size
        img_new = img_new.resize((int(width * 0.5), int(height * 0.5)), Image.ANTIALIAS)
        buf = BytesIO()
        img_new.save(buf, format='PNG')
        size = len(buf.getvalue()) / 1024

    res = pic2b64(img_new)
    res = MessageSegment.image(res)
    await bot.send(ev, res)