import os
from io import BytesIO
import re
import requests
from PIL import Image, ImageDraw, ImageFont

import hoshino
from hoshino.typing import *
from hoshino import Service, R
from hoshino.util import pic2b64, FreqLimiter, DailyNumberLimiter

sv = Service('fake_message', help_='', bundle='pcr娱乐', enable_on_default=True, visible=False)

SPLIT_TEXT = "\n"

def split_mes(mes:str):
    # 把整条消息分割成列表
    #mes = mes.replace("[CQ:at,qq=","").replace("]","")
    mes = mes.replace("\r\n","\n")
    mes_list = mes.split(SPLIT_TEXT)

    for i in range(len(mes_list)):
        # 按空格分割指令段
        temp_txt = mes_list[i].split(" ")

        # 去除多余的空字符串
        temp_list = [txt for txt in temp_txt if txt != ""]

        mes_list[i] = temp_list

    return mes_list


def produce_fake_mes(mes:str):
    # 生成假消息

    mes_list = split_mes(mes)

    data_list = []

    for mes in mes_list:
        uid,name,message = mes
        uid = uid.replace("[CQ:at,qq=","").replace("]","")

        data = {
            "type": "node",
            "data": {
                "name": name,
                "uin": uid,
                "content": message
            }
        }
        data_list.append(data)
    return data_list




@sv.on_prefix("假消息")
async def fake_mes(bot, ev):

    mes = ev["raw_message"][3:].strip()
    print(mes)
    data = produce_fake_mes(mes)
    print(data)
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)