import requests
import json
from io import BytesIO
from PIL import Image

from nonebot import on_command

from hoshino.typing import *
from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter

apikey='755900855ee1ef2a628723'

sv = Service('setu', manage_priv=priv.SUPERUSER, enable_on_default=False, visible=False)
setu_limit = DailyNumberLimiter(25)
lmt = FreqLimiter(15)

SETU_EXCEED_NOTICE = f'你今天冲的太多辣，欢迎明早5点后再来！'

session = requests.session()
# proxies = {
#     'https':'socks5://127.0.0.1:10808'
# }
# session.proxies = proxies


async def check_setu_num(session):
    if not setu_limit.check(session.ctx.user_id):
        await session.finish(SETU_EXCEED_NOTICE, at_sender=True)


def get_pic_one(num=0):
    url = 'https://api.lolicon.app/setu/'
    params = {
        'apikey': apikey,
        'r18': 0,
        'num': num,
        'size1200': True
    }
    try:
        r = session.get(url=url, params=params)
    except Exception:
        return '瑟图服务器爆炸惹_(:3」∠)_'
    j = r.json()
    pid = j['data'][0]['pid']
    title = j['data'][0]['title']
    pic_url = j['data'][0]['url']
    tags = j['data'][0]['tags']
    try:
        p = session.get(url=pic_url)
    except Exception:
        return '涩图服务器爆炸惹_(:3」∠)_'
    pic = Image.open(BytesIO(p.content))
    pic = pic.convert('RGB')
    picpath=f'setu\\{title}.jpg'
    pic.save(R.img(picpath).path)
    msg = [
    f"{title}",
    f"{R.img(picpath).cqcode}",
    f"https://pixiv.net/i/{pid}",
    f"{tags[:3]}"
    ]
    return '\n'.join(msg)


@on_command('setu', aliases=('色图测试','瑟图测试','涩图测试'))
async def setu_one(session):
    
    if not lmt.check(session.ctx.user_id):
        await session.send(f'乖，要懂得节制噢，涩图冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
        return
    lmt.start_cd(session.ctx.user_id)

    await check_setu_num(session)
    setu_limit.increase(session.ctx.user_id, 1)

    lolicon = get_pic_one()
    await session.send(lolicon)

