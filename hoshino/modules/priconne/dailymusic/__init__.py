import requests
import random
import time

try:
    import ujson as json
except:
    import json

import hoshino
from hoshino import Service,R,logger
from hoshino.typing import *

from . import _music_data
from . import _vacation_data

sv = Service('dailymusic', help_='', bundle='pcr娱乐', enable_on_default=True, visible=False)
session = requests.session()

def music_gener():
    musiclist = []
    for music in _music_data.MUSIC_DATA:
        musiclist.append(music)
    random.shuffle(musiclist)
    for musicId in musiclist:
        musicInfo = _music_data.MUSIC_DATA[musicId]
        yield musicId, musicInfo

music_gener = music_gener()

@sv.scheduled_job('cron', hour=18, minute=1)
async def daily_music():
    bot = hoshino.get_bot()
    musicId, musicInfo = music_gener.__next__()
    msg = [
        "美食殿今日的晚间音乐~",
        f"{musicInfo[1]}",
        f"{R.img('priconne/dailymusic/', musicInfo[4]).cqcode}",
        f"歌曲名: {musicInfo[2]}",
        f"歌手: {musicInfo[3]}"
    ]  
    music = MessageSegment.music(type_=musicInfo[0], id_=musicId)
    await bot.send_group_msg(group_id=602138153, message='\n'.join(msg))
    await bot.send_group_msg(group_id=602138153, message=music)

@sv.scheduled_job('cron', hour=19, minute=00)
async def daily_music():
    bot = hoshino.get_bot()
    msg=[]
    today=time.time()
    try:
        for vacationInfo in _vacation_data.VACATION_DATA.values():
            holiday=''
            vDay=time.mktime(time.strptime(vacationInfo[0],'%Y-%m-%d'))
            intervalDay=int((vDay-today)/(60*60*24))
            if intervalDay<=0:
                continue
            if vacationInfo[2]==1:
                holiday='假期'
            msg.append(f'距离【{vacationInfo[1]}】{holiday}还有:{intervalDay}天')
        msg.append("\n接下来为mmk大人献上精挑细选的晚间音乐~")
        #msg.append(f"{R.img('打工人.jpg').cqcode}")
        await bot.send_group_msg(group_id=873875268, message='\n'.join(msg))
        music=mmk_music()
        await bot.send_group_msg(group_id=873875268, message=music)
    except Exception as e:
        logger.error(f'{e}')


def mmk_music():
    url = 'https://music.163.com/api/v1/playlist/detail'
    headers = {
    'Cookie': 'appver = 2.0.2',
    'refer': 'http://music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    params = {
        'id': 315624195
    }
    try:
        keywordResult = session.post(url=url, headers=headers, params=params, timeout=10)
    except (requests.exceptions.RequestException) as e:
        logger.error(f'[music.163.com connect failed]{e}')
        return '没有版权，发不出去勒...'
    
    keywordJson = keywordResult.json()
    if keywordJson['playlist']['trackIds']:
        id=random.choice(keywordJson['playlist']['trackIds'])['id']
    else:
        return '没有版权，发不出去勒...'
  
    return MessageSegment.music(type_='163', id_=id)