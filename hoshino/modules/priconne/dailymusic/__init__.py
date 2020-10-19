import random

import hoshino
from hoshino import Service,R
from hoshino.typing import *

from . import _music_data

sv = Service('dailymusic', help_='', bundle='pcr娱乐', enable_on_default=True, visible=False)

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