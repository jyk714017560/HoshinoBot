# -*- coding: utf-8 -*-
import os
import re
import asyncio
from collections import defaultdict

import hoshino
from hoshino import R, Service, util, priv
from hoshino.typing import *

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

try:
    import ujson as json
except:
    import json

sv_help = '''
修改海豹阈值[海豹判定阈值]：如果不输入参数，默认阈值是100
'''.strip()
sv = Service('pcrsealkiller', help_=sv_help, bundle='pcr娱乐', enable_on_default=False, visible=True)

GACHA_KEYWORDS = ['所持角色交换Pt', '持有的角色交換Pt', '所持キャラ交換Pt', '持有的角色交换Pt', '所持キャラ交换Pt', '所持CSPキャラ交換Pt']
DEFAULT_GACHA_THRESHOLD = 100  # 海豹判定阈值, 如果抽卡次数小于这个阈值，则被判定为海豹
EMOJI_CRITERION = 70  #表情包判定标准
BIG_CRITERION = 5000  #表情包判定标准

SecretId = ''
SecretKey = ''
Region = ''

_gacha_thershold_file = os.path.expanduser('~/.hoshino/gacha_thershold_config.json')
_gacha_thershold = {}
try:
    with open(_gacha_thershold_file, encoding='utf8') as f:
        _gacha_thershold = json.load(f)
except FileNotFoundError as e:
    sv.logger.warning('gacha_thershold_config.json not found, will create when needed.')
_gacha_thershold = defaultdict(lambda: DEFAULT_GACHA_THRESHOLD, _gacha_thershold)


def dump_threshold_config():
    with open(_gacha_thershold_file, 'w', encoding='utf8') as f:
        json.dump(_gacha_thershold, f, ensure_ascii=False)


GACHA_THRESHOLD_TIP = '请输入1-300之间的整数作为海豹判定阈值哦~'
@sv.on_prefix(('修改海豹阈值'))
async def set_gacha_threshold(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '只有群管理才能修改海豹判定阈值哦~', at_sender=True)
    threshold = ev.message.extract_plain_text()
    if not threshold:
        await bot.finish(ev, GACHA_THRESHOLD_TIP, at_sender=True)
        return
    if threshold.isdigit() and 0 < int(threshold) < 301:
        gid = str(ev.group_id)
        _gacha_thershold[gid] = threshold
        dump_threshold_config()
    else:
        await bot.finish(ev, GACHA_THRESHOLD_TIP, at_sender=True)


@sv.on_message()
async def pcrsealkiller(bot, ev: CQEvent):
    if len(ev.message) == 1:
        m = ev.message[0]
        if m.type == 'image':
            img = m.data['file']
            pic = await bot.get_image(file=img)
            if pic['filename'].endswith('gif') or pic['size'] / 1024 < EMOJI_CRITERION or pic['size'] / 1024 > BIG_CRITERION:
                return
            try:
                if ev.group_id == 1058019377 or ev.group_id == 602138153:
                    result = await ocr(pic['url'])
                else:
                    result = await bot.call_action(action='.ocr_image', image=img)
            except:
                return
            resultString = str(result)

            #抽卡界面判定
            isGacha = False
            for kw in GACHA_KEYWORDS:
                if kw in resultString:
                    keyword = kw
                    isGacha = True
                    break
            if not isGacha:
                return
            
            #抽卡次数判定
            verdictString = re.search('[0-9]+.\+[0-9]+', resultString)
            if not verdictString:
                return
            gachaAmount = int(re.match('[0-9]+', verdictString.group(0)).group(0))
            gid = str(ev.group_id)
            gachaThershold = _gacha_thershold[gid]          
            
            #抽卡new判定
            isNewGacha = False
            for r in result['TextDetections']:
                if r['text'] == keyword:
                    horizon = r['ItemPolygon']['Y']
                    break
            for r in result['texts']:
                if r['text'] == 'NEW' and r['coordinates'][0]['y'] < horizon:
                    isNewGacha = True
                    break
          
            #海豹审判
            if not isNewGacha and gachaAmount > gachaThershold:
                return
            if isNewGacha and gachaAmount <= gachaThershold:
                await bot.send(ev, f"检测到海豹行为(╯‵□′)╯︵┻━┻\n{R.img('sealkiller.png').cqcode}")
                await util.silence(ev, 6 * gachaAmount)
                await asyncio.sleep(gachaAmount)
                await bot.delete_msg(self_id=ev.self_id, message_id=ev.message_id)
                return
            else:
                await bot.send(ev, "注意！疑似海豹出没中_(:3」」")
                return


async def ocr(url):
    try: 
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, Region, clientProfile)

        req = models.GeneralBasicOCRRequest()
        params = {
            "ImageUrl": url,
            "LanguageType": "auto"
        }
        req.from_json_string(json.dumps(params))

        resp = client.GeneralBasicOCR(req) 
        return resp

    except TencentCloudSDKException as err: 
        sv.logger.warning(err)
