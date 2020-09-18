from io import BytesIO
import requests
from PIL import Image, ImageFile
import threading
import time
import random
import string
from urllib.parse import urlencode
from hashlib import md5
import base64

APPKEY = '0U4fBhJ0EJSi2YOw'
session = requests.session()

def setu_distinguish(img_url):
    img = pic2b64(img_url)
    url = 'https://api.ai.qq.com/fcgi-bin/vision/vision_porn'
    time_stamp = int(time.time())
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    params = {
        'app_id': '2156804300',
        'image': img,
        'time_stamp': time_stamp,
        'nonce_str': nonce_str, 
    }
    params['sign'] = getReqSign(params=params)
    r = session.post(url=url, data=params)
    j = r.json()
    if not j['ret']:
        confidence = j['data']['tag_list'][9]['tag_confidence']
        return confidence
    else:
        return 0


def getReqSign(params):
    r = urlencode(sorted(params.items(), key=lambda value: value[0]))
    r += '&app_key=' + APPKEY
    sign = str(md5(r.encode()).hexdigest()).upper()
    return sign


def pic2b64(img_url):
    r = session.get(url=img_url, timeout=20)
    pic = Image.open(BytesIO(r.content))
    buf = BytesIO()
    pic.save(buf, format='PNG')
    img = base64.b64encode(buf.getvalue()).decode()
    return img