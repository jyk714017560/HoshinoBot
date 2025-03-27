import requests
import threading
from nonebot import MessageSegment

try:
    import ujson as json
except:
    import json

from hoshino import logger


session = requests.session()

def music_keyword(keyword):
    url = 'https://music.163.com/api/search/get/web'
    headers = {
    'Cookie': 'appver = 2.0.2',
    'refer': 'http://music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    params = {
    's': keyword,
    'offset': 0,
    'limit': 1,
    'type': 1
    }
    try:
        keywordResult = session.post(url=url, headers=headers, params=params, timeout=10)
    except (requests.exceptions.RequestException) as e:
        logger.error(f'[music.163.com connect failed]{e}')
        return '点歌失败惹 QAQ\n有可能是服务器网络爆炸，请重试一次'
    
    keywordJson = keywordResult.json()
    if keywordJson['result']['songCount']:
        id = keywordJson['result']['songs'][0]['id']
        # title = keywordJson['result']['songs'][0]['name']
        # artist = keywordJson['result']['songs'][0]['artists'][0]['name']
        # image = keywordJson['result']['songs'][0]['album']['blurPicUrl']
        # imageUrl = f'{image}?param=90y90'
        # audioUrl = f'http://music.163.com/song/media/outer/url?id={id}.mp3'
    else:
        return '没有版权，发不出去勒...'
  
    return MessageSegment.music(type_='163', id_=id)

def music_keyword_qq(keyword):
    params = {
        "w": keyword, 
        "format": "json", 
        "p": 0, 
        "n": 1
        }

    headers = {
        "referer": "http://m.y.qq.com",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    try:
        resp = session.get(
            url="http://c.y.qq.com/soso/fcgi-bin/client_search_cp",
            params=params,
            headers=headers,
            timeout=10
        )
        res_data = resp.json()
    except Exception as e:
        logger.error(f'[music.qq.com connect failed]{e}')
        return '点歌失败惹 QAQ\n有可能是服务器网络爆炸，请重试一次'

    if res_data['data']['song']['list']:
        id = res_data['data']['song']['list'][0]['songid']
    else:
        return '没有版权，发不出去勒...'

    return MessageSegment.music(type_='qq', id_=id)
    #return MessageSegment(type_='music',data={'id': str(id),'type': 'qq'})


class MusicThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MusicThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

    