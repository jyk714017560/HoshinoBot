import os
import random

from datetime import datetime
from PIL import ImageDraw, ImageFont

from hoshino import R, Service
from hoshino.typing import *
from hoshino.util import pic2b64

sv = Service('clock', visible=False)
fontPath = fontPath = os.path.join(os.path.dirname(__file__), '1.otf')

@sv.on_fullmatch(('佩可几点了','佩可报时', '报时', '几点了'))
async def clock(bot, ev):
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
