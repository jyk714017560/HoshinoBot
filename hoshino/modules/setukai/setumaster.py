import os
from io import BytesIO
import requests
from PIL import Image
from queue import Queue

from hoshino import R, Service

session = requests.session()
apikey = '755900855ee1ef2a628723'

class SetuMaster(object):

    def __init__(self):
        self.q = Queue(8)
    
    def setu_producer(self, sv: Service):
        while True:
            setu = get_pic_one()
            sv.logger.info(f'色图生产')
            self.q.put(setu)
    
    def setu_consumer(self, sv: Service):
        setu = self.q.get()
        sv.logger.info(f'色图消费')
        return setu


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
    picpath = f'setu\\{title}.jpg'
    pic.save(R.img(picpath).path)
    msg = [
    f"{title}",
    f"{R.img(picpath).cqcode}",
    f"https://pixiv.net/i/{pid}",
    f"{tags[:3]}"
    ]
    return '\n'.join(msg)