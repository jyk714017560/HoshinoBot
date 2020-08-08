import os
from io import BytesIO
import requests
from PIL import Image
import threading
import time
import random

try:
    import ujson as json
except:
    import json

from hoshino import R, logger

session = requests.session()

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

    pic = Image.open(BytesIO(r.content))
    pic = pic.convert('RGB')
    try:
        pic.save(R.img('setu/keyword/', f'{title}.jpg').path)
    except OSError as e:
        logger.error(f'[pic save failed]{e}')
        return '涩图太涩，发不出去勒...'
    msg = [
    f"标题: {title}",
    f"画师: {author}",
    f"{R.img('setu/keyword/', f'{title}.jpg').cqcode}",
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