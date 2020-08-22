import requests
from nonebot import MessageSegment

try:
    import ujson as json
except:
    import json


session = requests.session()

def music_keyword(keyword):
    keywordUrl = 'http://musicapi.leanapp.cn/search'
    musicUrl = 'https://api.imjad.cn/cloudmusic/'
    try:
        keywordResult = session.get(url=keywordUrl, params={'keywords': keyword}, timeout=10)
    except (requests.exceptions.RequestException) as e:
        logger.error(f'[musicapi.leanapp.cn connect failed]{e}')
        return '点歌失败惹 QAQ\n有可能是服务器网络爆炸，请重试一次'
    
    keywordJson = keywordResult.json()
    if keywordJson['result']['songCount']:
        id = keywordJson['result']['songs'][0]['id']
        title = keywordJson['result']['songs'][0]['name']
        artist = keywordJson['result']['songs'][0]['artists'][0]['name']
    else:
        return '没有版权，发不出去勒...'
    
    try:
        musicResult = session.get(url=musicUrl, params={'id': id}, timeout=10)
    except (requests.exceptions.RequestException) as e:
        logger.error(f'[api.imjad.cn connect failed]{e}')
        return '点歌失败惹 QAQ\n有可能是服务器网络爆炸，请重试一次'
    
    musicJson = musicResult.json()
    audioUrl = musicJson['data'][0]['url']
    if not audioUrl:
        return '没有版权，发不出去勒...'
    
    return MessageSegment.music_custom(url='https://game.granbluefantasy.jp/', audio_url=audioUrl, title=title, content=artist)

    