import requests
import random
from io import BytesIO
from PIL import Image,ImageDraw, ImageFont

from hoshino import R, Service
from hoshino.typing import *
from hoshino.util import pic2b64, FreqLimiter, DailyNumberLimiter

sv = Service('fzl', visible=False)
fontPath = R.img('font/sakura.ttf').path
_nlmt = DailyNumberLimiter(15)
_flmt = FreqLimiter(15)
session = requests.session()

color = ['#0000ff', '#ff00f7','#00cc66']
el1 = ['废墟', '深海', '反应堆', '学园', '腐烂', '东京', '三维', '四次元', '少管所', '流星', '闪光', '南极', '消极', '幽浮', '网路', '暗狱', '离子态', '液态', '黑色', '抱抱', '暴力', '垃圾', '社会', '残暴', '残酷', '工口', '戮尸', '原味', '毛茸茸', '香香', '霹雳', '午夜', '美工刀', '爆浆', '机关枪', '无响应', '手术台', '麻风病', '虚拟', '速冻', '智能', '2000', '甜味', '华丽', '反社会', '玛利亚', '无', '梦之', '蔷薇', '无政府', '酷酷', '西伯利亚', '人造', '法外', '追杀', '通缉', '女子', '微型', '男子', '超', '毁灭', '大型', '绝望', '阴间', '死亡', '坟场', '高科技', '奇妙', '魔法', '极限', '社会主义', '无聊']
el2 = ['小丑', '仿生', '纳米', '原子', '丧', '电子', '十字架', '咩咩', '赛博', '野猪', '外星', '窒息', '变态', '触手', '小众', '悲情', '飞行', '绿色', '电动', '铁锈', '碎尸', '电音', '蠕动', '酸甜', '虚构', '乱码', '碳水', '内脏', '脑浆', '血管', '全裸', '绷带', '不合格', '光滑', '标本', '酸性', '碱性', '404', '变身', '反常', '樱桃', '碳基', '矫情', '病娇', '进化', '潮湿', '砂糖', '高潮', '变异', '复合盐', '伏特加', '抑郁', '暴躁', '不爱说话', '废物', '失败', '幻想型', '社恐', '苦涩', '粘液', '浓厚', '快乐', '强制', '中二病', '恶魔', 'emo', '激光', '发射', '限量版', '迷因', '堕落', '放射性']
el3 = ['天使', '精灵', '女孩', '男孩', '宝贝', '小妈咪', '虫', '菇', '公主', '少女', '少年', '1号机', '子', '恐龙', '蜈蚣', '蟑螂', '食人鱼', '小飞船', '舞女', '桃子', '团子', '精', '酱', '废料', '生物', '物质', '奶茶', '搅拌机', '液', '火锅', '祭司', '体', '实验品', '试验体', '小猫咪', '样本', '颗粒', '血块', '汽水', '蛙', '软体', '机器人', '人质', '小熊', '圣母', '胶囊', '乙女', '主义者', '屑', '垢', '污渍', '废人', '毛血旺', '怪人', '肉', '河豚', '豚', '藻类', '唾沫', '咒语', '建筑', '球', '小狗', '碳', '元素', '少先队员', '博士', '糖']

@sv.on_prefix(('取名'))
async def clock(bot, ev):
    if ev.message[0].type != 'image':
        await bot.send(ev, '必须要发送图片才能取名噢\n> 取名+图片: 取名', at_sender=True)
        return
    img_url = ev.message[0].data['url']
    if not _flmt.check(ev.user_id):
        await bot.send(ev, f'乖，要懂得节制噢，取名冷却中（剩余 {int(_flmt.left_time(ev.user_id)) + 1}秒）', at_sender=True)
        return
    if not _nlmt.check(ev.user_id):
        await bot.send(ev, '佩可今天不想为你取名啦，欢迎明早5点后再来！', at_sender=True)
        return
    _flmt.start_cd(ev.user_id)
    _nlmt.increase(ev.user_id, 1)

    #爬图片
    try:
        r = session.get(url=img_url, timeout=10)
    except:
        await bot.send(ev, '图片太大了惹_(:3」∠)_', at_sender=True)
        return
    try:
        img2 = Image.open(BytesIO(r.content))
    except:
        await bot.send(ev, '图片太大了惹_(:3」∠)_', at_sender=True)
        return

    #图片处理
    img1=Image.new("RGB", (500, 350), "#E1E1E1")
    w,h=img2.size
    if w>310 or h>310:
        if w/310>h/310:
            new_w=310
            new_h=int(h*new_w/w)
        else:
            new_h=310
            new_w=int(w*new_h/h)
    else:
        if 310/h>310/w:
            new_w=310
            new_h=int(h*new_w/w)
        else:
            new_h=310
            new_w=int(w*new_h/h)
    img3=img2.resize((new_w,new_h))
    imgFont1 = ImageFont.truetype(font=fontPath, size=18)
    imgFont2 = ImageFont.truetype(font=fontPath, size=40)
    fill2=random.choice(color)

    one = random.choice(el1)
    two = random.choice(el2)
    three = random.choice(el3)

    draw = ImageDraw.Draw(img1)
    img1.paste(img3,(170, 20))
    draw.text(xy=(10,150), text='你的亚名是',font=imgFont1, fill='#696969')
    draw.text(xy=(10,260), text=one + two + three,font=imgFont2, fill=fill2)

    res = pic2b64(img1)
    res = MessageSegment.image(res)
    await bot.send(ev, res)
