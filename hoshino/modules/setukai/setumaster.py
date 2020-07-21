import os
from io import BytesIO
import requests
from PIL import Image
from queue import Queue
import threading

try:
    import ujson as json
except:
    import json

from hoshino import R, logger


session = requests.session()
apikey = '755900855ee1ef2a628723'

_setu_quene_file = os.path.expanduser('~/.hoshino/setu_quene_config.json')
_setu_quene = []
try:
    with open(_setu_quene_file, encoding='utf8') as f:
        _setu_quene = json.load(f)
except FileNotFoundError as e:
    logger.warning('setu_quene_config.json not found, will create when needed.')
   
quene = Queue()
for setu in _setu_quene:
    quene.put(setu)
logger.info(f'initial {quene.qsize} setu is put into the main thread')


def dump_setu_config():
    with open(_setu_quene_file, 'w', encoding='utf8') as f:
        json.dump(_setu_quene, f, ensure_ascii=False)


def get_setu():
    url = 'https://api.lolicon.app/setu/'
    params = {
        'apikey': apikey,
        'r18': 0,
        'num': 5,
        'size1200': True
    }
    try:
        r = session.get(url=url, params=params)
    except (requests.exceptions.RequestException) as e:
        logger.warning(f'[lolicon.app connect failed]{e}')
        return []
    
    results = r.json()
    setu_list = []
    for setu in results['data']:
        title = setu['title']
        pic_url = setu['url']
        try:
            r = session.get(url=pic_url)
        except (requests.exceptions.RequestException) as e:
            logger.warning(f'[pixiv.cat connect failed]{e}')
            return []

        pic = Image.open(BytesIO(r.content))
        pic = pic.convert('RGB')
        pic.save(R.img('setu/', f'{title}.jpg').path)

        setu_list.append(setu)
    return setu_list


def setu_producer():
    while True:
        if quene.qsize() < 5:
            setu_list = get_setu()
            for setu in setu_list:
                quene.put(setu)
                _setu_quene.append(setu)
            dump_setu_config()
            logger.info('色图生产')

    
def setu_consumer():
    setu = quene.get()
    _setu_quene.pop(1)
    logger.info('色图消费')
    pid = setu['pid']
    title = setu['title']
    tags = setu['tags']
    author = setu['author']
    msg = [
    f"{title}/{author}",
    f"{R.img('setu/', f'{title}.jpg').cqcode}",
    f"author: https://pixiv.net/i/{pid}",
    f"{tags[:3]}"
    ]   
    return '\n'.join(msg)

p = threading.Thread(target=setu_producer)
p.start()