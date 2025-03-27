import os
from io import BytesIO
import requests
from PIL import Image, ImageFile
import threading
import time
import random
import datetime

try:
    import ujson as json
except:
    import json

from hoshino import R, logger

ImageFile.LOAD_TRUNCATED_IMAGES = True

session = requests.session()
apikey = '435221525ed48358ebab15'

_setu_quene_file = os.path.expanduser('~/.hoshino/setu_quene_config.json')
_setu_list = []
try:
    with open(_setu_quene_file, encoding='utf8') as f:
        _setu_list = json.load(f)
        logger.info(f'initial {len(_setu_list)} setu is put into the setu list')
except FileNotFoundError as e:
    logger.warning('setu_quene_config.json not found, will create when needed.')


def dump_setu_config():
    with open(_setu_quene_file, 'w', encoding='utf8') as f:
        json.dump(_setu_list, f, ensure_ascii=False)


def get_setu():
    url = 'https://api.lolicon.app/setu/'
    params = {
        'apikey': apikey,
        'r18': 0,
        'num': 5,
        'size1200': True
    }
    try:
        r = session.get(url=url, params=params, timeout=10)
    except (requests.exceptions.RequestException) as e:
        logger.error(f'[lolicon.app connect failed]{e}')
        return []
    
    results = r.json()
    setu_list = []
    for setu in results['data']:
        title = setu['title']
        pic_url = setu['url']
        pic_url=pic_url.replace("cat","re")
        try:
            r = session.get(url=pic_url, timeout=20)
        except (requests.exceptions.RequestException) as e:
            logger.error(f'[pixiv.cat connect failed]{e}')
            continue

        try:
            pic = Image.open(BytesIO(r.content))
            pic = pic.convert('RGB')
            title = title.replace('/','-')
            date = datetime.datetime.now().strftime('%Y%m%d')
            setu['date'] = date
            datePath = f'/home/res/img/setu/{date}'
            if not os.path.exists(datePath):
                os.makedirs(datePath)
            pic.save(R.img(f'setu/{date}/', f'{title}.jpg').path)
        except OSError as e:
            logger.error(f'[pic save failed]{e}')
            continue

        setu_list.append(setu)
    return setu_list


def setu_producer():
    while True:
        if len(_setu_list) > 10:
            setu_list = get_setu()
            for setu in setu_list:
                _setu_list.append(setu)
            dump_setu_config()
            logger.info(f'{len(setu_list)} setu is put into the setu list')
        time.sleep(30)

    
async def setu_consumer():
    if not _setu_list:
        setudir=random.choice(os.listdir('/home/res/img/setu'))
        setuold=random.choice(os.listdir(os.path.join('/home/res/img/setu',setudir)))
        titleold=setuold.replace(".jpg","")
        msg = [
        f"标题: {titleold}",
        f"{R.img(f'setu/{setudir}/', f'{setuold}').cqcode}",
        ]  
        return '\n'.join(msg)
    setu = _setu_list.pop(0)
    dump_setu_config()
    logger.info('1 setu is take out from the setu list')
    pid = setu['pid']
    title = setu['title']
    tags = setu['tags']
    author = setu['author']
    date = setu['date']
    msg = [
    f"标题: {title}",
    f"画师: {author}",
    f"{R.img(f'setu/{date}/', f'{title}.jpg').cqcode}",
    f"源地址: https://pixiv.net/i/{pid}"
    ]   
    return '\n'.join(msg)

thread = threading.Thread(name='Thread-setu', target=setu_producer)
thread.start()

def setu_reset():
    if thread.isAlive():
        return "涩图服务运行正常"
    else:
        thread.start()
        return "重启涩图成功"
