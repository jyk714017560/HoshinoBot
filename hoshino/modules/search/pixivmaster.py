import os
from io import BytesIO
import requests
from PIL import Image
import threading
import time
import random
import datetime

try:
    import ujson as json
except:
    import json

from hoshino import R, logger

session = requests.session()
headers = {
    'token': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBa2VpIiwidXVpZCI6ImM5MzM0Y2Q3Yzg0NTRkMWI4MWRlMmJmZTZkYzI0ZGFhIiwiaWF0IjoxNjExNTg3MzIzLCJhY2NvdW50Ijoie1wiYXZhdGFyXCI6XCJodHRwczovL2ltYWdlLmFjZ214LmNvbS9hY2NvdW50LzYyMEFrZWkucG5nXCIsXCJlbWFpbFwiOlwiNzE0MDE3NTYwQHFxLmNvbVwiLFwiZ2VuZGVyXCI6LTEsXCJoYXNQcm9uXCI6MCxcImlkXCI6NjIwLFwicGFzc1dvcmRcIjpcIjU3ZGVhZWYyYjg1YzI2ZDg3ZmExMWQwYmQxYzFiMzk1XCIsXCJzdGF0dXNcIjowLFwidXNlck5hbWVcIjpcIkFrZWlcIn0iLCJqdGkiOiI2MjAifQ.tk4-StNIyXzwEi64Nta3-ykEyxqxjmbx8I7kFkd0nJg'
}
session.headers = headers

def pixivic_keyword(keyword):
    url = 'https://api.pixivic.com/illustrations'
    params = {
        'illustType': 'illust',
        'searchType': 'original',
        'maxSanityLevel': 4,
        'page': 1,
        'pageSize': 30,
        'keyword':keyword
    }    
    try:
        r = session.get(url=url, params=params, timeout=10)
    except (requests.exceptions.RequestException) as e:
        logger.error(f'[pixivic.com/illustration connect failed]{e}')
        return '搜索失败惹 QAQ\n有可能是服务器网络爆炸，请重试一次'
    
    results = r.json()
    if not 'data' in results:
        return '涩图太涩，发不出去勒...'
    setu = random.choice(results['data'])
    pid = setu['id']
    title = setu['title']
    author = setu['artistPreView']['name']
    pic_url = setu['imageUrls'][0]['original']
    pic_url = pic_url.replace('/i.pximg.net/', '/i.pixiv.cat/')
    try:
        r = session.get(url=pic_url, timeout=10)
    except (requests.exceptions.RequestException) as e:
        logger.error(f'[pixiv.cat connect failed]{e}')
        return '瑟图服务器爆炸惹_(:3」∠)_'

    try:
        pic = Image.open(BytesIO(r.content))
        pic = pic.convert('RGB')
        title = title.replace('/','-')
        date = datetime.datetime.now().strftime('%Y%m%d')
        datePath = f'/home/res/img/setu/keyword/{date}'
        if not os.path.exists(datePath):
            os.makedirs(datePath)
        pic.save(R.img(f'setu/keyword/{date}/', f'{title}.jpg').path)
    except OSError as e:
        logger.error(f'[pic save failed]{e}')
        return '涩图太涩，发不出去勒...'
    msg = [
    f"标题: {title}",
    f"画师: {author}",
    f"{R.img(f'setu/keyword/{date}/', f'{title}.jpg').cqcode}",
    f"源地址: https://pixiv.net/i/{pid}"
    ]  
    return '\n'.join(msg)

# def get_pixivSuggestions(keyword):
#     url = f'https://api.pixivic.com/keywords/{keyword}/pixivSuggestions'
#     try:
#         r = session.get(url=url, timeout=10)
#     except (requests.exceptions.RequestException) as e:
#         logger.error(f'[pixivic.com/pixivSuggestions connect failed]{e}')
#         return ''
#     results = r.json()
#     msg = ['\n如果这不是你要找的图，可以试试以下几个关键词:']
#     if not 'data' in results:
#         return ''
#     for suggestion in results['data'][:3]:
#         msg.append(f"来份{suggestion['keyword']}色图")
#     return '\n'.join(msg)

class PixivicThread(threading.Thread):

    def __init__(self, func, args=()):
        super(PixivicThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None