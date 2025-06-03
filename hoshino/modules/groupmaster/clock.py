import os
import random

from datetime import datetime
from PIL import ImageDraw, ImageFont

from hoshino import R, Service
from hoshino.typing import *
from hoshino.util import pic2b64, DailyNumberLimiter

sv = Service('clock', visible=False)
fontPath = R.img('font/SF-Pro-Display-Bold.otf').path
clock_limit = DailyNumberLimiter(1)

@sv.on_keyword(('晚安'))
async def clock(bot, ev):
    #仅开放七曜群和塞姆利亚群
    if ev.group_id == 1058019377 or ev.group_id == 602138153 or ev.group_id == 611941900:
        if not clock_limit.check(ev.group_id):
            return
        clock_limit.increase(ev.group_id)
        text = datetime.now().strftime('%H:%M')
        imgFont = ImageFont.truetype(font=fontPath, size=90)
        textSize = imgFont.getsize(text=text)
        img = R.img(f'clock/{random.randint(1, 5)}.JPG').open()

        draw = ImageDraw.Draw(img)
        xy = (332 - textSize[0] / 2, 310 - textSize[1] / 2)
        draw.text(xy=xy, text=text, font=imgFont, fill='black')

        res = pic2b64(img)
        res = MessageSegment.image(res)
        await bot.send(ev, res)
