# -*- coding: utf-8 -*-

import random
import os
from PIL import Image, ImageSequence, ImageDraw, ImageFont

import hoshino
from hoshino import R, Service
from hoshino.util import pic2b64,DailyNumberLimiter
from hoshino.typing import *
from .luck_desc import luck_desc
from .luck_type import luck_type



sv_help = '''
[抽签|人品|运势|抽凯露签]
随机角色/指定凯露预测今日运势
准确率高达114.514%！
'''.strip()
#帮助文本
sv = Service('portune', help_=sv_help, bundle='pcr娱乐', enable_on_default=True, visible=True)
lmt = DailyNumberLimiter(1)

Img_Path = 'priconne/portunedata'
PORTUNE_EXCEED_NOTICE = '你今天已经抽过签了，欢迎明早5点后再来！'


@sv.on_prefix(('抽签', '人品', '运势'), only_to_me=True)
async def portune(bot, ev):

    if not lmt.check(ev.user_id):
        await bot.finish(ev, PORTUNE_EXCEED_NOTICE, at_sender=True)
    lmt.increase(ev.user_id, 1)

    model = 'DEFAULT'

    pic = drawing_pic(model)
    await bot.send(ev, pic, at_sender=True)


@sv.on_fullmatch(('抽臭鼬签', '抽猫猫签', '抽凯露签'))
async def portune_kyaru(bot, ev):

    if not lmt.check(ev.user_id):
        await bot.finish(ev, PORTUNE_EXCEED_NOTICE, at_sender=True)
    lmt.increase(ev.user_id, 1)

    model = 'KYARU'

    pic = drawing_pic(model)
    await bot.send(ev, pic, at_sender=True)


def drawing_pic(model) -> Image:
    fontPath = {
        'title': R.img('font/Mamelon.otf').path,
        'text': R.img('font/sakura.ttf').path
    }

    if model == 'KYARU':  
        base_img = R.img(os.path.join(Img_Path, "frame_1.jpg"))
    else:
        base_dir = R.img(Img_Path).path
        random_img = random.choice(os.listdir(base_dir))
        base_img = R.img(os.path.join(Img_Path, random_img))

    filename = os.path.basename(base_img.path)
    charaid = filename.lstrip('frame_')
    charaid = charaid.rstrip('.jpg')

    img = base_img.open()
    # Draw title
    draw = ImageDraw.Draw(img)
    text, title = get_info(charaid)

    font_size = 45
    color = '#F5F5F5'
    image_font_center = (140, 99)
    ttfront = ImageFont.truetype(fontPath['title'], font_size)
    font_length = ttfront.getsize(title)
    draw.text((image_font_center[0] - font_length[0] / 2, image_font_center[1] - font_length[1] / 2), title, fill=color, font=ttfront)
    # Text rendering
    font_size = 25
    color = '#323232'
    image_font_center = [140, 297]
    ttfront = ImageFont.truetype(fontPath['text'], font_size)
    result = decrement(text)
    if not result[0]:
        return Exception('Unknown error in daily luck') 
    textVertical = []
    for i in range(0, result[0]):
        font_height = len(result[i + 1]) * (font_size + 4)
        textVertical = vertical(result[i + 1])
        x = int(image_font_center[0] + (result[0] - 2) * font_size / 2 + 
                (result[0] - 1) * 4 - i * (font_size + 4))
        y = int(image_font_center[1] - font_height / 2)
        draw.text((x, y), textVertical, fill = color, font = ttfront)

    img = pic2b64(img)
    img = MessageSegment.image(img)
    return img


def get_info(charaid):
    for i in luck_desc:
        if charaid in i['charaid']:
            typewords = i['type']
            desc = random.choice(typewords)
            target_luck_type = desc['good-luck']
            for j in luck_type:
                if j['good-luck'] == target_luck_type:
                    return desc['content'], j['name']
    raise Exception('luck description not found')


def decrement(text):
    length = len(text)
    result = []
    cardinality = 9
    if length > 4 * cardinality:
        return [False]
    numberOfSlices = 1
    while length > cardinality:
        numberOfSlices += 1
        length -= cardinality
    result.append(numberOfSlices)
    # Optimize for two columns
    space = ' '
    length = len(text)
    if numberOfSlices == 2:
        if length % 2 == 0:
            # even
            fillIn = space * int(9 - length / 2)
            return [numberOfSlices, text[:int(length / 2)] + fillIn, fillIn + text[int(length / 2):]]
        else:
            # odd number
            fillIn = space * int(9 - (length + 1) / 2)
            return [numberOfSlices, text[:int((length + 1) / 2)] + fillIn,
                                    fillIn + space + text[int((length + 1) / 2):]]
    for i in range(0, numberOfSlices):
        if i == numberOfSlices - 1 or numberOfSlices == 1:
            result.append(text[i * cardinality:])
        else:
            result.append(text[i * cardinality:(i + 1) * cardinality])
    return result


def vertical(str):
    list = []
    for s in str:
        list.append(s)
    return '\n'.join(list)