import os
from io import BytesIO
import requests
from PIL import Image
from queue import Queue
import threading
import time

try:
    import ujson as json
except:
    import json

from hoshino import R, logger


session = requests.session()
apikey = '435221525ed48358ebab15'

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
logger.info(f'initial {quene.qsize()} setu is put into the main thread')


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
            continue

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
            logger.info(f'{len(setu_list)} setu is put into the main thread')
        time.sleep(60)

    
def setu_consumer():
    if quene.empty():
        return '色图库正在补充，请稍候再冲'
    setu = quene.get()
    _setu_quene.pop(0)
    dump_setu_config()
    logger.info('1 setu is take out from the main thread')
    pid = setu['pid']
    title = setu['title']
    tags = setu['tags']
    author = setu['author']
    msg = [
    f"标题: {title}",
    f"画师: {author}",
    f"{R.img('setu/', f'{title}.jpg').cqcode}",
    f"源地址: https://pixiv.net/i/{pid}"
    ]   
    return '\n'.join(msg)

p = threading.Thread(target=setu_producer)
p.start()