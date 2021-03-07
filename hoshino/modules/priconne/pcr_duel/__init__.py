import asyncio
import base64
import os
import random
from collections import defaultdict
import sqlite3
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
from hoshino import Service, priv
from hoshino.typing import *
from hoshino.modules.priconne.pcr_duel import _pcr_duel_data as _pcr_data
from hoshino.modules.priconne.pcr_duel import duel_chara as chara
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter, concat_pic, pic2b64
import copy
import json

sv_help = '''
贵族决斗帮助：请查看帮助
'''.strip()
sv = Service('pcr_duel', help_=sv_help, bundle='pcr娱乐', enable_on_default=True, visible=True)

DB_PATH = os.path.expanduser("~/.hoshino/pcr_duel.db")
SCORE_DB_PATH = os.path.expanduser('~/.hoshino/pcr_running_counter.db')
BLACKLIST_ID = [1000, 1067, 1069, 1072, 1073, 1908, 4031, 9000, 9401]  # 黑名单ID
WAIT_TIME = 15  # 决斗接受等待时间
DUEL_SUPPORT_TIME = 30  # 赌钱等待时间
WAIT_TIME_TRADE = 15 # 交易接受等待时间
SIGN_DAILY_LIMIT = 1  # 机器人每天签到的次数
DUEL_DAILY_LIMIT = 5  #每个人每日发起决斗上限
DATE_DAILY_LIMIT = 1  #每天女友约会次数上限
GIFT_DAILY_LIMIT = 5  #每日购买礼物次数上限
RESET_HOUR = 4  # 每日使用次数的重置时间，0代表凌晨0点，1代表凌晨1点，以此类推
GACHA_COST = 300  # 抽老婆需求
ZERO_GET_AMOUNT = 50  # 没钱补给量
WIN_NUM = 1  #下注获胜赢得的倍率
BREAK_UP_SWITCH = True  #分手系统开关
WAIT_TIME_CHANGE = 30  #礼物交换等待时间
SHANGXIAN_NUM = 1000  #增加女友上限所需金币
WAREHOUSE_NUM = 20  #仓库增加上限
LEVEL_GIRL_NEED = {
    "1": 3,
    "2": 5,
    "3": 7,
    "4": 10,
    "5": 15,
    "6": 20,
    "7": 40,
    "8": 99
}  # 升级所需要的老婆，格式为["等级“: 需求]
LEVEL_COST_DICT = {
    "1": 0,
    "2": 100,
    "3": 300,
    "4": 500,
    "5": 1000,
    "6": 2000,
    "7": 5000
}  # 升级所需要的钱钱，格式为["等级“: 需求]
LEVEL_PRESTIGE_NEED = {
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 1000,
    "6": 2000,
    "7": 5000
    } # 升级所需要的声望，格式为["等级“: 需求]
RELATIONSHIP_DICT = {
    0: ["初见", "浣花溪上见卿卿，脸波明，黛眉轻。"],
    30: ["相识", "有美一人，清扬婉兮。邂逅相遇，适我愿兮。"],
    60: ["熟悉", "夕阳谁唤下楼梯，一握香荑。回头忍笑阶前立，总无语，也依依。"],
    100: ["朋友", "锦幄初温，兽烟不断，相对坐调笙。"],
    150: ["朦胧", "和羞走，倚门回首，却把青梅嗅。"],
    200: ["喜欢", "夜月一帘幽梦，春风十里柔情。"],
    300: ["依恋", "愿我如星君如月，夜夜流光相皎洁。"],
    500: ["挚爱", "江山看不尽，最美镜中人。"]
}

GIFT_DICT = {
    "玩偶": 0,
    "礼服": 1,
    "歌剧门票": 2,
    "水晶球": 3,
    "耳环": 4,
    "发饰": 5,
    "小裙子": 6,
    "热牛奶": 7,
    "书": 8,
    "鲜花": 9
}
GIFTCHOICE_DICT = {
    0: [0, 2, 1],
    1: [1, 0, 2],
    2: [2, 1, 0],
}

Gift10 = [
    "这个真的可以送给我吗，谢谢(害羞的低下了头)。", "你是专门为我准备的吗，你怎么知道我喜欢这个呀，谢谢你！", "啊，我最喜欢这个，真的谢谢你。"
]
Gift5 = ["谢谢送我这个，我很开心。", "这个我很喜欢，谢谢。", "你的礼物我都很喜欢哦，谢谢。"]
Gift2 = ["送我的吗，谢谢你。", "谢谢你的礼物。", "为我准备了礼物吗，谢谢。"]
Gift1 = ["不用为我特意准备礼物啦，不过还是谢谢你哦。", "嗯，谢谢。", "嗯，我收下了，谢谢你。"]

Addgirlfail = [
    '你参加了一场贵族舞会，热闹的舞会场今天竟然没人同你跳舞。', '你邀请到了心仪的女友跳舞，可是跳舞时却踩掉了她的鞋，她生气的离开了。',
    '你为这次舞会准备了很久，结果一不小心在桌子上睡着了，醒来时只看到了过期的邀请函。',
    '你参加了一场贵族舞会，可是舞会上只有一名男性向你一直眨眼。', '你准备参加一场贵族舞会，可惜因为忘记穿礼服，被拦在了门外。',
    '你沉浸在舞会的美食之中，忘了此行的目的。', '你本准备参加舞会，却被会长拉去出了一晚上刀。',
    '舞会上你和另一个贵族发生了争吵，你一拳打破了他的鼻子，两人都被请出了舞会。', '舞会上你很快约到了一名女伴跳舞，但是她不是你喜欢的类型。',
    '你约到了一位心仪的女伴，但是她拒绝了与你回家，说想再给你一个考验。', '你和另一位贵族同时看中了一个女孩，但是在三人交谈时，你渐渐的失去了话题。'
]
Addgirlsuccess = [
    '你参加了一场贵族舞会，你优雅的舞姿让每位年轻女孩都望向了你。', '你参加了一场贵族舞会，你的帅气使你成为了舞会的宠儿。',
    '你在舞会门口就遇到了一位女孩，你挽着她的手走进了舞会。', '你在舞会的闲聊中无意中谈到了自己显赫的家室，你成为了舞会的宠儿。',
    '没有人比你更懂舞会，每一个女孩都为你的风度倾倒。', '舞会上你没有约到女伴，但是舞会后却有个女孩偷偷跟着你回了家。',
    '舞会上你和另一个贵族发生了争吵，一位女孩站出来为你撑腰，你第一次的注意到了这个可爱的女孩。',
    '你强壮的体魄让女孩们赞叹不已，她们纷纷来问你是不是一位军官。', '你擅长在舞会上温柔地对待每一个人，女孩们也向你投来了爱意。',
    '一个可爱的女孩一直在舞会上望着你，你犹豫了一会，向她发出了邀请。'
]

Login100 = [
    '今天是练习击剑的一天，不过你感觉你的剑法毫无提升。', '优雅的贵族从不晚起，可是你今天一直睡到了中午。',
    '今天你点了一份豪华的午餐却忘记了带钱，窘迫的你毫无贵族的姿态。', '今天你在路上看上了别人的女友，却没有鼓起勇气向他决斗。',
    '今天你十分抑郁，因为发现自己最近上升的只有体重。'
]
Login200 = [
    '今天是练习击剑的一天，你感觉到了你的剑法有所提升。', '早起的你站在镜子前许久，天底下竟然有人可以这么帅气。',
    '今天你搞到了一瓶不错的红酒，你的酒窖又多了一件存货。', '今天巡视领地时，一个小孩子崇拜地望着你，你感觉十分开心。',
    '今天一个朋友送你一张音乐会的门票，你打算邀请你的女友同去。', '今天一位国王的女友在路上向你抛媚眼，也许这就是个人魅力吧。'
]
Login300 = [
    '今天是练习击剑的一天，你感觉到了你的剑法大有长进。', '今天你救下了一个落水的小孩，他的家人说什么也要你收下一份心意。',
    '今天你巡视领地时，听到几个小女孩说想长大嫁给帅气的领主，你心里高兴极了。', '今天你打猎时猎到了一只鹿，你骄傲的把鹿角加入了收藏。',
    '今天你得到了一匹不错的马，说不定可以送去比赛。'
]
Login600 = [
    '今天是练习击剑的一天，你觉得自己已经可谓是当世剑圣。', '今天你因为领地治理有方，获得了皇帝的嘉奖。',
    '今天你的一位叔叔去世了，无儿无女的他，留给了你一大笔遗产。', '今天你在比武大会上获得了优胜，获得了全场的喝彩。',
    '今天你名下的马夺得了赛马的冠军，你感到无比的自豪。'
]

Date5 = [
    '你比约会的时间晚到了十分钟，嘟着嘴的她看起来不太满意。', '一向善于言辞的你，今天的约会却不时冷场，她看起来不是很开心。',
    '今天的约会上你频频打哈欠，被她瞪了好几次，早知道昨晚不该晚睡的。',
    '“为您旁边的这个姐姐买朵花吧。”你们被卖花的男孩拦下，你本想买花却发现自己忘记了带钱，她看起来不是很开心。'
]
Date10 = [
    '你带她去熟悉的餐厅吃饭，她觉得今天过得很开心。', '你带她去看了一场马术表演，并约她找机会一起骑马出去，她愉快的答应了。',
    '“为您旁边的这个姐姐买朵花吧。”你们被卖花的男孩拦下，你买了一束花还给了小孩一笔小费，你的女友看起来很开心。',
    '你邀请她去看一场歌剧，歌剧中她不时微笑，看起来十分开心。'
]
Date15 = [
    '你和她一同骑马出行，两个人一同去了很多地方，度过了愉快的一天。', '你新定做了一件最新款的礼服，约会中她称赞你比往常更加帅气。',
    '你邀请她共赴一场宴会，宴会上你们无所不谈，彼此间的了解增加了。', '你邀请她去看一场歌剧，歌剧中她一直轻轻地握着你的手。'
]
Date20 = [
    '你邀请她共赴一场宴会，宴会中她亲吻了你的脸颊后，害羞的低下了头，这必然是你和她难忘的一天。',
    '约会中你们被一群暴民劫路，你为了保护她手臂受了伤。之后她心疼的抱住了你，并为你包扎了伤口。',
    '你邀请她去看你的赛马比赛，你骑着爱马轻松了夺取了第一名，冲过终点后，你大声地向着看台喊出了她的名字，她红着脸低下了头。',
    '你和她共同参加了一场盛大的舞会，两人的舞步轻盈而优雅，被评为了舞会第一名，上台时你注视着微笑的她，觉得她今天真是美极了。'
]


#帮助中猜角色猜头像获胜加金币为个人魔改，如果不魔改可以删掉这两行描述。
@sv.on_fullmatch(['贵族决斗帮助', '贵族帮助'])
async def duel_help(bot, ev: CQEvent):
    msg = '''
╔                                       ╗    
        贵族决斗相关指令

   1.贵族签到(每日一次)
   2.查询贵族
   3.贵族决斗+@
   4.领金币
   5.查金币
   6.贵族舞会(招募女友)
   7.查女友+角色名
   8.查名字+序号(查询女友的名字)
   9.升级贵族
   10.贵族转生
   11.分手女友+角色名(需分手费)
   12.转账金币+@(为@qq转账xxx金币)
   13.购买女友上限(国王以上，增加女友上限)
   14.dlc帮助(增加dlc角色)
   15.好感帮助(好感系统指令)
   16.声望帮助(声望系统帮助)
   17.女友交易(用xxx金币与@qq交易女友+角色名)，需要收10%交易手续费

   a.重置金币+@ (限群主)
   b.重置角色+@ (限群主)
   c.重置决斗(限管理，决斗卡住时用)

  一个女友只属于一位群友
  猜卡面获胜
  每日可各获得3次200金币（还没加）
  猜语音获胜
  每日可获得1次300金币（还没加）
╚                                        ╝
'''
    data ={
            "type": "node",
            "data": {
                "name": '佩可莉姆',
                "uin": '2651026038',
                "content": msg
            }
            }
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)

@sv.on_fullmatch(['贵族等级表'])
async def duel_rank(bot, ev: CQEvent):
    msg='''"1": "男爵",  最多可持有3名女友，每日签到额外获得50金币，初始等级。
"2": "子爵",升级需要500金币，最多可持有5名女友，每日签到额外获得100金币。
"3": "伯爵",升级需要1000金币，最多可持有7名女友，每日签到额外获得150金币。
"4": "侯爵",升级需要3000金币，最多可持有10名女友，每日签到额外获得200金币。
"5": "公爵",升级需要1000声望和5000金币，最多可持有15名女友，每日签到额外获得250金币。
"6": "国王",升级需要1500声望和10000金币，最多可持有20名女友，每日签到额外获得300金币，不再会掉级，可拥有一名妻子。
"7": "皇帝",升级需要2000声望和15000金币，最多可持有40名女友，每日签到额外获得350金币，不再会掉级，可拥有一名妻子。
"8": "神"升级需要2500声望和20000金币，最多可持有60名女友，每日签到额外获得400金币，暂时不再会掉级，可拥有一名妻子。
'''  
    await bot.send(ev, msg)


#加载DLC部分代码
#这里记录每个dlc的列表范围
fgolist = range(8001, 8301)

#这里记录dlc名字和对应列表
dlcdict = {'fgo': fgolist}

#这里记录每个dlc的介绍
dlcintro = {
    'fgo': 'FGO手游角色包',
}

# 这个字典保存保存每个DLC开启的群列表，pcr默认一直开启。
dlc_switch_file = os.path.join(os.path.dirname(__file__),
                               'dlc_config.json')  #用于加载dlcjson
dlc_switch = {}
try:
    with open(dlc_switch_file, 'r', encoding='UTF-8') as f:
        dlc_switch = json.load(f, strict=False)
except FileNotFoundError as e:
    sv.logger.warning(
        'dlc_switch_config.json not found, will create when needed.')
dlc_switch = defaultdict(lambda: [], dlc_switch)
def dump_dlc_switch():
    with open(dlc_switch_file, 'w', encoding='UTF-8') as f:
        json.dump(dlc_switch, f, ensure_ascii=False)


@sv.on_prefix(['加载dlc', '加载DLC', '开启dlc', '开启DLC'])
async def add_dlc(bot, ev: CQEvent):
    gid = ev.group_id
    if not priv.check_priv(ev, priv.OWNER):
        await bot.finish(ev, '只有群主才能加载dlc哦。', at_sender=True)
    args = ev.message.extract_plain_text().split()
    if len(args) >= 2:
        await bot.finish(ev, '指令格式错误。', at_sender=True)
    if len(args) == 0:
        await bot.finish(ev, '请输入加载dlc+dlc名。', at_sender=True)
    dlcname = args[0]
    if dlcname not in dlcdict.keys():
        await bot.finish(ev, 'DLC名填写错误。', at_sender=True)
    if gid in dlc_switch[dlcname]:
        await bot.finish(ev, '本群已开启此dlc哦。', at_sender=True)
    dlc_switch[dlcname].append(gid)
    dump_dlc_switch()
    await bot.finish(ev, f'加载dlc {dlcname}  成功!', at_sender=True)


@sv.on_prefix(['卸载dlc', '卸载DLC', '关闭dlc', '关闭DLC'])
async def delete_dlc(bot, ev: CQEvent):
    gid = ev.group_id
    if not priv.check_priv(ev, priv.OWNER):
        await bot.finish(ev, '只有群主才能卸载dlc哦。', at_sender=True)
    args = ev.message.extract_plain_text().split()
    if len(args) >= 2:
        await bot.finish(ev, '指令格式错误', at_sender=True)
    if len(args) == 0:
        await bot.finish(ev, '请输入卸载dlc+dlc名。', at_sender=True)
    dlcname = args[0]
    if dlcname not in dlcdict.keys():
        await bot.finish(ev, 'DLC名填写错误', at_sender=True)
    if gid not in dlc_switch[dlcname]:
        await bot.finish(ev, '本群没有开启此dlc哦。', at_sender=True)
    dlc_switch[dlcname].remove(gid)
    dump_dlc_switch()
    await bot.finish(ev, f'卸载dlc {dlcname}  成功!', at_sender=True)


@sv.on_fullmatch(['dlc列表', 'DLC列表'])
async def intro_dlc(bot, ev: CQEvent):
    msg = '可用DLC列表：\n\n'
    i = 1
    for dlc in dlcdict.keys():
        msg += f'{i}.{dlc}:\n'
        intro = dlcintro[dlc]
        msg += f'介绍:{intro}\n'
        num = len(dlcdict[dlc])
        msg += f'共有{num}名角色\n'
        i += 1
    msg += '发送 加载\卸载dlc+dlc名\n可加载\卸载dlc\n卸载的dlc不会被抽到，但是角色仍留在玩家仓库，可以被抢走。'
    await bot.finish(ev, msg)


@sv.on_fullmatch(['dlc帮助', 'DLC帮助'])
async def help_dlc(bot, ev: CQEvent):
    msg = '''
╔                                 ╗
         DLC帮助
      
  1.加载\卸载dlc+dlc名
  2.dlc列表(查看介绍)
  
  卸载的dlc不会被抽到
  但是角色仍留在仓库
  可以被他人抢走
  
╚                                 ╝    
'''
    data ={
            "type": "node",
            "data": {
                "name": '佩可莉姆',
                "uin": '2651026038',
                "content": msg
            }
            }
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)


#取得该群未开启的dlc所形成的黑名单
def get_dlc_blacklist(gid):
    dlc_blacklist = []
    for dlc in dlcdict.keys():
        if gid not in dlc_switch[dlc]:
            dlc_blacklist += dlcdict[dlc]
    return dlc_blacklist


#检查有没有没加到json里的dlc
def check_dlc():
    for dlc in dlcdict.keys():
        if dlc not in dlc_switch.keys():
            dlc_switch[dlc] = []
    dump_dlc_switch()
check_dlc()


# noinspection SqlResolve
class RecordDuel:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_table()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self.connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS limiter"
                "(key TEXT NOT NULL, num INT NOT NULL, date INT, PRIMARY KEY(key))"
            )

    def exist_check(self, key):
        try:
            key = str(key)
            with self.connect() as conn:
                conn.execute(
                    "INSERT INTO limiter (key,num,date) VALUES (?, 0,-1)",
                    (key, ),
                )
            return
        except:
            return

    def get_num(self, key):
        self.exist_check(key)
        key = str(key)
        with self.connect() as conn:
            r = conn.execute("SELECT num FROM limiter WHERE key=? ",
                             (key, )).fetchall()
            r2 = r[0]
        return r2[0]

    def clear_key(self, key):
        key = str(key)
        self.exist_check(key)
        with self.connect() as conn:
            conn.execute(
                "UPDATE limiter SET num=0 WHERE key=?",
                (key, ),
            )
        return

    def increment_key(self, key, num):
        self.exist_check(key)
        key = str(key)
        with self.connect() as conn:
            conn.execute("UPDATE limiter SET num=num+? WHERE key=?", (
                num,
                key,
            ))
        return

    def get_date(self, key):
        self.exist_check(key)
        key = str(key)
        with self.connect() as conn:
            r = conn.execute("SELECT date FROM limiter WHERE key=? ",
                             (key, )).fetchall()
            r2 = r[0]
        return r2[0]

    def set_date(self, date, key):
        print(date)
        self.exist_check(key)
        key = str(key)
        with self.connect() as conn:
            conn.execute(
                "UPDATE limiter SET date=? WHERE key=?",
                (
                    date,
                    key,
                ),
            )
        return

db = RecordDuel(DB_PATH)


class DailyAmountLimiter(DailyNumberLimiter):
    def __init__(self, types, max_num, reset_hour):
        super().__init__(max_num)
        self.reset_hour = reset_hour
        self.type = types

    def check(self, key) -> bool:
        now = datetime.now(self.tz)
        key = list(key)
        key.append(self.type)
        key = tuple(key)
        day = (now - timedelta(hours=self.reset_hour)).day
        if day != db.get_date(key):
            db.set_date(day, key)
            db.clear_key(key)
        return bool(db.get_num(key) < self.max)

    def get_num(self, key):
        key = list(key)
        key.append(self.type)
        key = tuple(key)
        return db.get_num(key)

    def increase(self, key, num=1):
        key = list(key)
        key.append(self.type)
        key = tuple(key)
        db.increment_key(key, num)

    def reset(self, key):
        key = list(key)
        key.append(self.type)
        key = tuple(key)
        db.clear_key(key)


daily_sign_limiter = DailyAmountLimiter("sign", SIGN_DAILY_LIMIT, RESET_HOUR)
daily_duel_limiter = DailyAmountLimiter("duel", DUEL_DAILY_LIMIT, RESET_HOUR)
daily_date_limiter = DailyAmountLimiter("date", DATE_DAILY_LIMIT, RESET_HOUR)
daily_gift_limiter = DailyAmountLimiter("gift", GIFT_DAILY_LIMIT, RESET_HOUR)


# 用于与赛跑金币互通
class ScoreCounter2:
    def __init__(self):
        os.makedirs(os.path.dirname(SCORE_DB_PATH), exist_ok=True)
        self._create_table()
        self._create_pres_table()

    def _connect(self):
        return sqlite3.connect(SCORE_DB_PATH)

    def _create_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS SCORECOUNTER
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           SCORE           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建表发生错误')

    def _add_score(self, gid, uid, score):
        try:
            current_score = self._get_score(gid, uid)
            conn = self._connect()
            conn.execute(
                "INSERT OR REPLACE INTO SCORECOUNTER (GID,UID,SCORE) \
                                VALUES (?,?,?)",
                (gid, uid, current_score + score))
            conn.commit()
        except:
            raise Exception('更新表发生错误')

    def _reduce_score(self, gid, uid, score):
        try:
            current_score = self._get_score(gid, uid)
            if current_score >= score:
                conn = self._connect()
                conn.execute(
                    "INSERT OR REPLACE INTO SCORECOUNTER (GID,UID,SCORE) \
                                VALUES (?,?,?)",
                    (gid, uid, current_score - score))
                conn.commit()
            else:
                conn = self._connect()
                conn.execute(
                    "INSERT OR REPLACE INTO SCORECOUNTER (GID,UID,SCORE) \
                                VALUES (?,?,?)", (gid, uid, 0))
                conn.commit()
        except:
            raise Exception('更新表发生错误')

    def _get_score(self, gid, uid):
        try:
            r = self._connect().execute(
                "SELECT SCORE FROM SCORECOUNTER WHERE GID=? AND UID=?",
                (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')

    # 判断金币是否足够下注
    def _judge_score(self, gid, uid, score):
        try:
            current_score = self._get_score(gid, uid)
            if current_score >= score:
                return 1
            else:
                return 0
        except Exception as e:
            raise Exception(str(e))

    #记录国王声望数据
    def _create_pres_table(self):
        try:
            self._connect().execute(
                '''CREATE TABLE IF NOT EXISTS PRESTIGECOUNTER
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           PRESTIGE           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建表发生错误')

    def _set_prestige(self, gid, uid, prestige):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO PRESTIGECOUNTER (GID, UID, PRESTIGE) VALUES (?, ?, ?)",
                (gid, uid, prestige),
            )

    def _get_prestige(self, gid, uid):
        try:
            r = self._connect().execute(
                "SELECT PRESTIGE FROM PRESTIGECOUNTER WHERE GID=? AND UID=?",
                (gid, uid)).fetchone()
            return None if r is None else r[0]
        except:
            raise Exception('查找声望发生错误')

    def _add_prestige(self, gid, uid, num):
        prestige = self._get_prestige(gid, uid)
        prestige += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO PRESTIGECOUNTER (GID, UID, PRESTIGE) VALUES (?, ?, ?)",
                (gid, uid, prestige),
            )

    def _reduce_prestige(self, gid, uid, num):
        prestige = self._get_prestige(gid, uid)
        prestige -= num
        prestige = max(prestige, 0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO PRESTIGECOUNTER (GID, UID, PRESTIGE) VALUES (?, ?, ?)",
                (gid, uid, prestige),
            )


# 记录贵族相关数据
class DuelCounter:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._create_charatable()
        self._create_uidtable()
        self._create_leveltable()
        self._create_wifetable()
        self._create_favortable()
        self._create_gifttable()
        self._create_warehousetable()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _create_charatable(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS CHARATABLE
                          (GID             INT    NOT NULL,
                           CID             INT    NOT NULL,
                           UID           INT    NOT NULL,
                           PRIMARY KEY(GID, CID));''')
        except:
            raise Exception('创建角色表发生错误')

    def _create_uidtable(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS UIDTABLE
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           CID           INT    NOT NULL,
                           NUM           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, CID));''')
        except:
            raise Exception('创建UID表发生错误')

    def _create_leveltable(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS LEVELTABLE
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           LEVEL           INT    NOT NULL,
                           
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建等级表发生错误')

    def _get_card_owner(self, gid, cid):
        try:
            r = self._connect().execute(
                "SELECT UID FROM CHARATABLE WHERE GID=? AND CID=?",
                (gid, cid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找角色归属发生错误')

    def _set_card_owner(self, gid, cid, uid):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CHARATABLE (GID, CID, UID) VALUES (?, ?, ?)",
                (gid, cid, uid),
            )

    def _delete_card_owner(self, gid, cid):
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM CHARATABLE  WHERE GID=? AND CID=?",
                (gid, cid),
            )

# 查询已被邀请的女友列表

    def _get_card_list(self, gid):
        with self._connect() as conn:
            r = conn.execute(
                f"SELECT CID FROM CHARATABLE WHERE GID={gid}").fetchall()
            return [c[0] for c in r] if r else {}

    def _get_level(self, gid, uid):
        try:
            r = self._connect().execute(
                "SELECT LEVEL FROM LEVELTABLE WHERE GID=? AND UID=?",
                (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找等级发生错误')

    def _get_cards(self, gid, uid):
        with self._connect() as conn:
            r = conn.execute(
                "SELECT CID, NUM FROM UIDTABLE WHERE GID=? AND UID=? AND NUM>0 ",
                (gid, uid)).fetchall()
        return [c[0] for c in r] if r else {}

    def _get_card_num(self, gid, uid, cid):
        with self._connect() as conn:
            r = conn.execute(
                "SELECT NUM FROM UIDTABLE WHERE GID=? AND UID=? AND CID=?",
                (gid, uid, cid)).fetchone()
            return r[0] if r else 0

    def _add_card(self, gid, uid, cid, increment=1):
        num = self._get_card_num(gid, uid, cid)
        num += increment
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO UIDTABLE (GID, UID, CID, NUM) VALUES (?, ?, ?, ?)",
                (gid, uid, cid, num),
            )
        if cid != 9999:
            self._set_card_owner(gid, cid, uid)
            self._set_favor(gid, uid, cid, 0)

    def _delete_card(self, gid, uid, cid, increment=1):
        num = self._get_card_num(gid, uid, cid)
        num -= increment
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO UIDTABLE (GID, UID, CID, NUM) VALUES (?, ?, ?, ?)",
                (gid, uid, cid, num),
            )
        self._delete_card_owner(gid, cid)
        self._delete_favor(gid, uid, cid)

    def _add_level(self, gid, uid, increment=1):
        level = self._get_level(gid, uid)
        level += increment
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO LEVELTABLE (GID, UID, LEVEL) VALUES (?, ?, ?)",
                (gid, uid, level),
            )

    def _reduce_level(self, gid, uid, increment=1):
        level = self._get_level(gid, uid)
        level -= increment
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO LEVELTABLE (GID, UID, LEVEL) VALUES (?, ?, ?)",
                (gid, uid, level),
            )

    def _set_level(self, gid, uid, level):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO LEVELTABLE (GID, UID, LEVEL) VALUES (?, ?, ?)",
                (gid, uid, level),
            )

    def _get_level_num(self, gid, level):
        with self._connect() as conn:
            r = conn.execute(
                "SELECT COUNT(UID) FROM LEVELTABLE WHERE GID=? AND LEVEL=? ",
                (gid, level)).fetchone()
            return r[0] if r else 0

#妻子部分

    def _create_wifetable(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS WIFETABLE
                          (GID             INT    NOT NULL,
                           CID             INT    NOT NULL,
                           UID           INT    NOT NULL,
                           PRIMARY KEY(GID, CID));''')
        except:
            raise Exception('创建妻子表发生错误')

    def _get_wife_owner(self, gid, cid):
        try:
            r = self._connect().execute(
                "SELECT UID FROM WIFETABLE WHERE GID=? AND CID=?",
                (gid, cid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找妻子归属发生错误')

    def _set_wife_owner(self, gid, cid, uid):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO WIFETABLE (GID, CID, UID) VALUES (?, ?, ?)",
                (gid, cid, uid),
            )

    def _delete_wife_owner(self, gid, cid):
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM WIFETABLE  WHERE GID=? AND CID=?",
                (gid, cid),
            )

    def _get_wife_list(self, gid):
        with self._connect() as conn:
            r = conn.execute(
                f"SELECT CID FROM WIFETABLE WHERE GID={gid}").fetchall()
            return [c[0] for c in r] if r else {}

#查询某人的妻子，无则返回0
    def _search_wife(self, gid, uid):
        try:
            r = self._connect().execute(
                "SELECT CID FROM WIFETABLE WHERE GID=? AND UID=?",
                (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找妻子发生错误')

#好感度部分
    def _create_favortable(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS FAVORTABLE
                          (
                           GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           CID             INT    NOT NULL,
                           FAVOR           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, CID));''')
        except:
            raise Exception('创建好感表发生错误')

    def _set_favor(self, gid, uid, cid, favor):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO FAVORTABLE (GID, UID, CID, FAVOR) VALUES (?, ?, ?, ?)",
                (gid, uid, cid, favor),
            )

    def _get_favor(self, gid, uid, cid):
        try:
            r = self._connect().execute(
                "SELECT FAVOR FROM FAVORTABLE WHERE GID=? AND UID=? AND CID=?",
                (gid, uid, cid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找好感发生错误')

    def _add_favor(self, gid, uid, cid, num):
        favor = self._get_favor(gid, uid, cid)
        if favor == None:
            favor = 0
        favor += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO FAVORTABLE (GID, UID, CID, FAVOR) VALUES (?, ?, ?, ?)",
                (gid, uid, cid, favor),
            )

    def _reduce_favor(self, gid, uid, cid, num):
        favor = self._get_favor(gid, uid, cid)
        favor -= num
        favor = max(favor, 0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO FAVORTABLE (GID, UID, CID, FAVOR) VALUES (?, ?, ?, ?)",
                (gid, uid, cid, favor),
            )

    def _delete_favor(self, gid, uid, cid):
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM FAVORTABLE  WHERE GID=? AND UID=? AND CID=?",
                (gid, uid, cid),
            )

#礼物仓库部分
    def _create_gifttable(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS GIFTTABLE
                          (
                           GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           GFID             INT    NOT NULL,
                           NUM           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, GFID));''')
        except:
            raise Exception('创建礼物表发生错误')

    def _get_gift_num(self, gid, uid, gfid):
        try:
            r = self._connect().execute(
                "SELECT NUM FROM GIFTTABLE WHERE GID=? AND UID=? AND GFID=?",
                (gid, uid, gfid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找礼物发生错误')

    def _add_gift(self, gid, uid, gfid, num=1):
        giftnum = self._get_gift_num(gid, uid, gfid)
        if giftnum == None:
            giftnum = 0
        giftnum += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO GIFTTABLE (GID, UID, GFID, NUM) VALUES (?, ?, ?, ?)",
                (gid, uid, gfid, giftnum),
            )

    def _reduce_gift(self, gid, uid, gfid, num=1):
        giftnum = self._get_gift_num(gid, uid, gfid)
        giftnum -= num
        giftnum = max(giftnum, 0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO GIFTTABLE (GID, UID, GFID, NUM) VALUES (?, ?, ?, ?)",
                (gid, uid, gfid, giftnum),
            )

#角色上限部分
    def _create_warehousetable(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS WAREHOUSE
                          (GID             INT    NOT NULL,
                           UID           INT    NOT NULL,
                           NUM           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建仓库上限表发生错误')

    def _get_warehouse(self, gid, uid):
        try:
            r = self._connect().execute(
                "SELECT NUM FROM WAREHOUSE WHERE GID=? AND UID=?",
                (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找上限发生错误')

    def _add_warehouse(self, gid, uid, num):
        housenum = self._get_warehouse(gid, uid)
        housenum += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO WAREHOUSE (GID, UID, NUM) VALUES (?, ?, ?)",
                (gid, uid, housenum),
            )


# 记录决斗和下注数据
class DuelJudger:
    def __init__(self):
        self.on = {}
        self.accept_on = {}
        self.support_on = {}
        self.fire_on = {}
        self.deadnum = {}
        self.support = {}
        self.turn = {}
        self.duelid = {}
        self.isaccept = {}
        self.hasfired_on = {}

    def set_support(self, gid):
        self.support[gid] = {}

    def get_support(self, gid):
        return self.support[gid] if self.support.get(gid) is not None else 0

    def add_support(self, gid, uid, id, score):
        self.support[gid][uid] = [id, score]

    def get_support_id(self, gid, uid):
        if self.support[gid].get(uid) is not None:
            return self.support[gid][uid][0]
        else:
            return 0

    def get_support_score(self, gid, uid):
        if self.support[gid].get(uid) is not None:
            return self.support[gid][uid][1]
        else:
            return 0

    # 五个开关：决斗，接受，下注， 开枪, 是否已经开枪

    def get_on_off_status(self, gid):
        return self.on[gid] if self.on.get(gid) is not None else False

    def turn_on(self, gid):
        self.on[gid] = True

    def turn_off(self, gid):
        self.on[gid] = False

    def get_on_off_accept_status(self, gid):
        return self.accept_on[gid] if self.accept_on.get(
            gid) is not None else False

    def turn_on_accept(self, gid):
        self.accept_on[gid] = True

    def turn_off_accept(self, gid):
        self.accept_on[gid] = False

    def get_on_off_support_status(self, gid):
        return self.support_on[gid] if self.support_on.get(
            gid) is not None else False

    def turn_on_support(self, gid):
        self.support_on[gid] = True

    def turn_off_support(self, gid):
        self.support_on[gid] = False

    def get_on_off_fire_status(self, gid):
        return self.fire_on[gid] if self.fire_on.get(
            gid) is not None else False

    def turn_on_fire(self, gid):
        self.fire_on[gid] = True

    def turn_off_fire(self, gid):
        self.fire_on[gid] = False

    def get_on_off_hasfired_status(self, gid):
        return self.hasfired_on[gid] if self.hasfired_on.get(
            gid) is not None else False

    def turn_on_hasfired(self, gid):
        self.hasfired_on[gid] = True

    def turn_off_hasfired(self, gid):
        self.hasfired_on[gid] = False

    # 记录决斗者id
    def init_duelid(self, gid):
        self.duelid[gid] = []

    def set_duelid(self, gid, id1, id2):
        self.duelid[gid] = [id1, id2]

    def get_duelid(self, gid):
        return self.duelid[gid] if self.accept_on.get(gid) is not None else [
            0, 0
        ]

    # 查询一个决斗者是1号还是2号
    def get_duelnum(self, gid, uid):
        return self.duelid[gid].index(uid) + 1

    # 记录由谁开枪
    def init_turn(self, gid):
        self.turn[gid] = 1

    def get_turn(self, gid):
        return self.turn[gid] if self.turn[gid] is not None else 0

    def change_turn(self, gid):
        if self.get_turn(gid) == 1:
            self.turn[gid] = 2
            return 2
        else:
            self.turn[gid] = 1
            return 1

    # 记录子弹位置
    def init_deadnum(self, gid):
        self.deadnum[gid] = None

    def set_deadnum(self, gid, num):
        self.deadnum[gid] = num

    def get_deadnum(self, gid):
        return self.deadnum[gid] if self.deadnum[gid] is not None else False

    # 记录是否接受
    def init_isaccept(self, gid):
        self.isaccept[gid] = False

    def on_isaccept(self, gid):
        self.isaccept[gid] = True

    def off_isaccept(self, gid):
        self.isaccept[gid] = False

    def get_isaccept(self, gid):
        return self.isaccept[gid] if self.isaccept[gid] is not None else False


class GiftChange:
    def __init__(self):
        self.giftchange_on = {}
        self.waitchange = {}
        self.isaccept = {}
        self.changeid = {}

    #礼物交换开关
    def get_on_off_giftchange_status(self, gid):
        return self.giftchange_on[gid] if self.giftchange_on.get(
            gid) is not None else False

    def turn_on_giftchange(self, gid):
        self.giftchange_on[gid] = True

    def turn_off_giftchange(self, gid):
        self.giftchange_on[gid] = False

    #礼物交换发起开关
    def get_on_off_waitchange_status(self, gid):
        return self.waitchange[gid] if self.waitchange.get(
            gid) is not None else False

    def turn_on_waitchange(self, gid):
        self.waitchange[gid] = True

    def turn_off_waitchange(self, gid):
        self.waitchange[gid] = False

    #礼物交换是否接受开关
    def turn_on_accept_giftchange(self, gid):
        self.isaccept[gid] = True

    def turn_off_accept_giftchange(self, gid):
        self.isaccept[gid] = False

    def get_isaccept_giftchange(self, gid):
        return self.isaccept[gid] if self.isaccept[gid] is not None else False

    #记录礼物交换请求接收者id
    def init_changeid(self, gid):
        self.changeid[gid] = []

    def set_changeid(self, gid, id2):
        self.changeid[gid] = id2

    def get_changeid(self, gid):
        return self.changeid[gid] if self.changeid.get(gid) is not None else 0

class CardTrade:
    def __init__(self):
        self.tradeon = {}
        self.tradeflag = {}
        self.tradeid = {}
        self.tradename = {}
        self.trade_on = {}
        
    def get_trade_on_off_status(self, gid):
        return self.tradeon[gid] if self.tradeon.get(gid) is not None else False
    # 记录群交易开关
    def turn_tradeon(self, gid):
        self.tradeon[gid] = True

    def turn_tradeoff(self, gid):
        self.tradeon[gid] = False
    
    # 记录群交易是否接受开关
    def turn_on_trade(self, gid):
        self.trade_on[gid] = True

    def turn_off_trade(self, gid):
        self.trade_on[gid] = False
    
    # 记录交易者id
    def init_tradeid(self, gid):
        self.tradeid[gid] = []

    def set_tradeid(self, gid, id1, id2, cid):
        self.tradeid[gid] = [id1, id2, cid]

    def get_tradeid(self, gid):
        return self.tradeid[gid] if self.trade_on.get(gid) is not None else[0, 0, 0]

    # 记录是否接受交易
    def init_tradeflag(self, gid):
        self.tradeflag[gid] = False

    def on_tradeflag(self, gid):
        self.tradeflag[gid] = True

    def off_tradeflag(self, gid):
        self.tradeflag[gid] = False

    def get_tradeflag(self, gid):
        return self.tradeflag[gid] if self.tradeflag[gid] is not None else False


duel_judger = DuelJudger()
gift_change = GiftChange()
card_trade = CardTrade()


# 生成没被约过的角色列表
def get_newgirl_list(gid):
    chara_id_list = list(_pcr_data.CHARA_NAME.keys())
    duel = DuelCounter()
    old_list = duel._get_card_list(gid)
    dlc_blacklist = get_dlc_blacklist(gid)
    new_list = []
    for card in chara_id_list:
        if card not in BLACKLIST_ID and card not in old_list and card not in dlc_blacklist:
            new_list.append(card)
    return new_list


# 取爵位名
def get_noblename(level: int):
    namedict = {
        "1": "男爵",
        "2": "子爵",
        "3": "伯爵",
        "4": "侯爵",
        "5": "公爵",
        "6": "国王",
        "7": "皇帝",
        "8": "已成神",
    }
    return namedict[str(level)]


# 返回某人的女友上限,包括爵位的上限和额外购买的上限
def get_girlnum(gid, uid):
    duel = DuelCounter()
    level = duel._get_level(gid, uid)
    level_num = LEVEL_GIRL_NEED[str(level)]
    addition_num = duel._get_warehouse(gid, uid)
    num = level_num + addition_num
    return num


# 返回升级到爵位所需要的金币数
def get_noblescore(level: int):
    numdict = LEVEL_COST_DICT
    return numdict[str(level)]

# 返回升级到爵位所需要的声望数
def get_nobleprestige(level: int):
    numdict = LEVEL_PRESTIGE_NEED
    return numdict[str(level)]

# 判断当前女友数是否大于等于女友上限
def girl_outlimit(gid, uid):
    duel = DuelCounter()
    level = duel._get_level(gid, uid)
    girlnum = get_girlnum(gid, uid)
    cidlist = duel._get_cards(gid, uid)
    cidnum = len(cidlist)
    if cidnum >= girlnum:
        return True
    else:
        return False


@sv.on_fullmatch(['查询本群贵族'])
async def group_noble_status(bot, ev: CQEvent):
    gid = ev.group_id
    duel = DuelCounter()
    newgirllist = get_newgirl_list(gid)
    newgirlnum = len(newgirllist)
    l1_num = duel._get_level_num(gid, 1)
    l2_num = duel._get_level_num(gid, 2)
    l3_num = duel._get_level_num(gid, 3)
    l4_num = duel._get_level_num(gid, 4)
    l5_num = duel._get_level_num(gid, 5)
    l6_num = duel._get_level_num(gid, 6)
    l7_num = duel._get_level_num(gid, 7)
    l8_num = duel._get_level_num(gid, 8)
    dlctext = ''
    for dlc in dlcdict.keys():
        if gid in dlc_switch[dlc]:
            dlctext += f'{dlc},'
    msg = f'''
╔                          ╗
         本群贵族
      
  神：{l8_num}名
  皇帝：{l7_num}名
  国王：{l6_num}名
  公爵：{l5_num}名
  侯爵：{l4_num}名
  伯爵：{l3_num}名
  子爵：{l2_num}名
  男爵：{l1_num}名
  已开启DLC:
  {dlctext}
  还有{newgirlnum}名单身女友 
╚                          ╝
'''
    await bot.send(ev, msg)


@sv.on_fullmatch('贵族签到')
async def noblelogin(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    guid = gid, uid
    if not daily_sign_limiter.check(guid):
        await bot.send(ev, '今天已经签到过了哦，明天再来吧。', at_sender=True)
        return
    duel = DuelCounter()

    if duel._get_level(gid, uid) == 0:
        msg = '您还未在本群创建过贵族，请发送 创建贵族 开始您的贵族之旅。'
        await bot.send(ev, msg, at_sender=True)
        return
    #根据概率随机获得收益。
    score_counter = ScoreCounter2()
    daily_sign_limiter.increase(guid)
    loginnum_ = ['1', '2', '3', '4']
    r_ = [0.3, 0.4, 0.2, 0.1]
    sum_ = 0
    ran = random.random()
    for num, r in zip(loginnum_, r_):
        sum_ += r
        if ran < sum_: break
    Bonus = {
        '1': [100, Login100],
        '2': [200, Login200],
        '3': [300, Login300],
        '4': [600, Login600]
    }
    score1 = Bonus[num][0]
    text1 = random.choice(Bonus[num][1])

    #根据爵位的每日固定收入
    level = duel._get_level(gid, uid)
    score2 = 50 * level
    scoresum = score1 + score2
    score_counter._add_score(gid, uid, scoresum)
    noblename = get_noblename(level)
    score = score_counter._get_score(gid, uid)
    msg = f'\n{text1}\n签到成功！您领取了：\n\n{score1}金币(随机)和\n{score2}金币({noblename}爵位)'
    cidlist = duel._get_cards(gid, uid)
    cidnum = len(cidlist)
    #随机获得一件礼物
    select_gift = random.choice(list(GIFT_DICT.keys()))
    gfid = GIFT_DICT[select_gift]
    duel._add_gift(gid, uid, gfid)
    msg += f'\n随机获得了礼物[{select_gift}]'

    if cidnum > 0:
        cid = random.choice(cidlist)
        c = chara.fromid(cid)
        msg += f'\n\n今天向您请安的是\n{c.name}{c.icon.cqcode}'

    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch('创建贵族')
async def add_noble(bot, ev: CQEvent):
    try:
        gid = ev.group_id
        uid = ev.user_id
        duel = DuelCounter()
        if duel._get_level(gid, uid) != 0:
            msg = '您已经在本群创建过贵族了，请发送 查询贵族 查询。'
            await bot.send(ev, msg, at_sender=True)
            return

        #判定本群女友是否已空，如果空则分配一个复制人可可萝。
        newgirllist = get_newgirl_list(gid)
        if len(newgirllist) == 0:
            cid = 9999
            c = chara.fromid(1059)
            girlmsg = f'本群已经没有可以约的女友了哦，一位神秘的可可萝在你孤单时来到了你身边。{c.icon.cqcode}'
        else:
            cid = random.choice(newgirllist)
            c = chara.fromid(cid)
            girlmsg = f'为您分配的初始女友为：{c.name}{c.icon.cqcode}'
        duel._add_card(gid, uid, cid)
        duel._set_level(gid, uid, 1)
        msg = f'\n创建贵族成功！\n您的初始爵位是男爵\n可以拥有3名女友。\n{girlmsg}'
        await bot.send(ev, msg, at_sender=True)

    except Exception as e:
        await bot.send(ev, '错误:\n' + str(e))


@sv.on_fullmatch(['贵族查询','查询贵族'])
async def inquire_noble(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    score_counter = ScoreCounter2()
    if duel._get_level(gid, uid) == 0:
        msg = '您还未在本群创建过贵族，请发送 创建贵族 开始您的贵族之旅。'
        await bot.send(ev, msg, at_sender=True)
        return
    level = duel._get_level(gid, uid)
    noblename = get_noblename(level)
    girlnum = get_girlnum(gid, uid)
    score = score_counter._get_score(gid, uid)
    charalist = []

    cidlist = duel._get_cards(gid, uid)
    cidnum = len(cidlist)
    if cidnum == 0:
        msg = f'''
╔                          ╗
  您的爵位为{noblename}
  您的金币为{score}
  您共可拥有{girlnum}名女友
  您目前没有女友。
  发送[贵族约会]
  可以招募女友哦。
  
╚                          ╝
'''
        await bot.send(ev, msg, at_sender=True)

    else:
        for cid in cidlist:
            #替换复制人可可萝
            if cid == 9999:
                cid = 1059
            charalist.append(chara.Chara(cid, 0, 0))

        #制图部分，五个一行
        num = copy.deepcopy(cidnum)
        step = 5
        pics = []
        for i in range(0, num, step):
            j = min(num, i + step)
            pics.append(chara.gen_team_pic(charalist[i:j], star_slot_verbose=False))
        res = concat_pic(pics)
        res = pic2b64(res)
        res = MessageSegment.image(res)

        #判断是否开启声望
        prestige = score_counter._get_prestige(gid, uid)
        if prestige == None:
            partmsg = '未开启声望系统'
        else:
            partmsg = f'您的声望为{prestige}点'

        msg = f'''
╔                          ╗
  您的爵位为{noblename}
  您的金币为{score}
  {partmsg}
  您共可拥有{girlnum}名女友
  您已拥有{cidnum}名女友
  她们是：
    {res}   
╚                          ╝
'''
        #判断有无妻子
        wife = duel._search_wife(gid, uid)
        if wife != 0:
            c = chara.fromid(wife)

            msg = f'''
╔                          ╗
  您的爵位为{noblename}
  您的金币为{score}
  {partmsg}
  您的妻子是{c.name}
  您共可拥有{girlnum}名女友
  您已拥有{cidnum}名女友
  她们是：
    {res}
    
╚                          ╝
'''

        await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(['贵族舞会','招募女友'])
async def add_girl(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    score_counter = ScoreCounter2()
    if duel_judger.get_on_off_status(ev.group_id):
        msg = '现在正在决斗中哦，请决斗后再参加舞会吧。'
        await bot.send(ev, msg, at_sender=True)
        return
    if duel._get_level(gid, uid) == 8:
        msg = '你已成神，神不能招募女友。'
        await bot.send(ev, msg, at_sender=True)
        return 
    if duel._get_level(gid, uid) == 0:
        msg = '您还未在本群创建过贵族，请发送 创建贵族 开始您的贵族之旅。'
        duel_judger.turn_off(ev.group_id)

        await bot.send(ev, msg, at_sender=True)
        return
    else:
        # 防止女友数超过上限
        level = duel._get_level(gid, uid)
        noblename = get_noblename(level)
        girlnum = get_girlnum(gid, uid)
        cidlist = duel._get_cards(gid, uid)
        cidnum = len(cidlist)
        if cidnum >= girlnum:
            msg = '您的女友已经满了哦，快点发送[升级贵族]进行升级吧。'
            await bot.send(ev, msg, at_sender=True)
            return
        score = score_counter._get_score(gid, uid)
        if score < GACHA_COST:
            msg = f'您的金币不足{GACHA_COST}哦。'
            await bot.send(ev, msg, at_sender=True)
            return
        prestige = score_counter._get_prestige(gid,uid)
        if prestige == None:
           score_counter._set_prestige(gid, uid, 0)
        prestige = score_counter._get_prestige(gid,uid)
        if prestige < 0 and level >4:
            msg = f'您现在身败名裂（声望为负），无法招募女友！。'
            await bot.send(ev, msg, at_sender=True)
            return
        newgirllist = get_newgirl_list(gid)
        # 判断女友是否被抢没和该用户是否已经没有女友
        if len(newgirllist) == 0:
            # if cidnum != 0:
            #     await bot.send(ev, '这个群已经没有可以约到的新女友了哦。', at_sender=True)
            #     return
            # else:
            score_counter._reduce_score(gid, uid, GACHA_COST)
            cid = 9999
            c = chara.fromid(1059)
            duel._add_card(gid, uid, cid)
            msg = f'本群已经没有可以约的女友了哦，一位神秘的可可萝在你孤单时来到了你身边。{c.icon.cqcode}。'
            await bot.send(ev, msg, at_sender=True)
            return

        score_counter._reduce_score(gid, uid, GACHA_COST)

        # 招募女友失败
        if random.random() < 0.4:
            losetext = random.choice(Addgirlfail)
            msg = f'\n{losetext}\n您花费了{GACHA_COST}金币，但是没有约到新的女友。'
            await bot.send(ev, msg, at_sender=True)
            return

        # 招募女友成功
        cid = random.choice(newgirllist)
        duel._add_card(gid, uid, cid)
        c = chara.fromid(cid)
        wintext = random.choice(Addgirlsuccess)
        mes = c.icon.cqcode
        msg = f'\n{wintext}\n招募女友成功！\n您花费了{GACHA_COST}金币\n新招募的女友为：{c.name}{mes}'

        await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(['升级贵族', '贵族升级'])
async def add_girl(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    score_counter = ScoreCounter2()
    score = score_counter._get_score(gid, uid)
    level = duel._get_level(gid, uid)
    noblename = get_noblename(level)
    girlnum = LEVEL_GIRL_NEED[str(level)]
    cidlist = duel._get_cards(gid, uid)
    cidnum = len(cidlist)

    if duel_judger.get_on_off_status(ev.group_id):
        msg = '现在正在决斗中哦，请决斗后再升级爵位吧。'
        await bot.send(ev, msg, at_sender=True)
        return
    if duel._get_level(gid, uid) == 0:
        msg = '您还未在本群创建过贵族，请发送 创建贵族 开始您的贵族之旅。'
        await bot.send(ev, msg, at_sender=True)
        return

    if level == 6:
        msg = f'您已经是国王了， 需要通过声望加冕称帝哦，请“加冕称帝”。'
        await bot.send(ev, msg, at_sender=True)
        return

    if level == 7:
        msg = f'您是本群的皇帝，  再往前一步就能成神了，请“飞升成神”。'
        await bot.send(ev, msg, at_sender=True)
        return
    
    if level == 8:
        msg = f'您已经到达了世界的巅峰， 无法再继续提升了。'
        await bot.send(ev, msg, at_sender=True)
        return    

    if cidnum < girlnum:
        msg = f'您的女友没满哦。\n需要达到{girlnum}名女友\n您现在有{cidnum}名。'
        await bot.send(ev, msg, at_sender=True)
        return
    needscore = get_noblescore(level + 1)
    futurename = get_noblename(level + 1)
    needprestige = get_nobleprestige(level + 1)

    if score < needscore:
        msg = f'您的金币不足哦。\n升级到{futurename}需要{needscore}金币'
        await bot.send(ev, msg, at_sender=True)
        return
    
    prestige = score_counter._get_prestige(gid,uid)
    if level > 4 :
        if prestige == None:
            score_counter._set_prestige(gid,uid,0)
            await bot.finish(ev, '您还未开启声望系统哦，已为您开启！', at_sender=True)
            
        if prestige < needprestige: 
            await bot.finish(ev, f'您的声望不足哦。\n升级到{futurename}需要{needprestige}声望', at_sender=True)
            return

    score_counter._reduce_score(gid, uid, needscore)
    duel._add_level(gid, uid)
    newlevel = duel._get_level(gid, uid)
    newnoblename = get_noblename(newlevel)
    newgirlnum = get_girlnum(gid, uid)
    msg = f'花费了{needscore}金币\n您成功由{noblename}升到了{newnoblename}\n可以拥有{newgirlnum}名女友了哦。'
    await bot.send(ev, msg, at_sender=True)


@sv.on_prefix('贵族决斗')
async def nobleduel(bot, ev: CQEvent):
    if ev.message[0].type == 'at':
        id2 = int(ev.message[0].data['qq'])
    else:
        await bot.finish(ev, '参数格式错误, 请重试')
    if duel_judger.get_on_off_status(ev.group_id):
        await bot.send(ev, "此轮决斗还没结束，请勿重复使用指令。")
        return

    gid = ev.group_id
    duel_judger.turn_on(gid)
    id1 = ev.user_id
    duel = DuelCounter()
    is_overtime = 0
    if id2 == id1:
        await bot.send(ev, "不能和自己决斗！", at_sender=True)
        duel_judger.turn_off(ev.group_id)
        return

    if duel._get_level(gid, id1) == 0:
        msg = f'[CQ:at,qq={id1}]决斗发起者还未在创建过贵族\n请发送 创建贵族 开始您的贵族之旅。'
        duel_judger.turn_off(ev.group_id)
        await bot.send(ev, msg)
        return
    if duel._get_cards(gid, id1) == {}:
        msg = f'[CQ:at,qq={id1}]您没有女友，不能参与决斗哦。'
        duel_judger.turn_off(ev.group_id)
        await bot.send(ev, msg)
        return

    if duel._get_level(gid, id2) == 0:
        msg = f'[CQ:at,qq={id2}]被决斗者还未在本群创建过贵族\n请发送 创建贵族 开始您的贵族之旅。'
        duel_judger.turn_off(ev.group_id)
        await bot.send(ev, msg)
        return
    if duel._get_cards(gid, id2) == {}:
        msg = f'[CQ:at,qq={id2}]您没有女友，不能参与决斗哦。'
        duel_judger.turn_off(ev.group_id)
        await bot.send(ev, msg)
        return
    #判定每日上限
    guid = gid, id1
    if not daily_duel_limiter.check(guid):
        await bot.send(ev, '今天的决斗次数已经超过上限了哦，明天再来吧。', at_sender=True)
        duel_judger.turn_off(ev.group_id)
        return

    # 判定双方的女友是否已经超过上限

    # 这里设定大于才会提醒，就是可以超上限1名，可以自己改成大于等于。
    if girl_outlimit(gid, id1):
        msg = f'[CQ:at,qq={id1}]您的女友超过了爵位上限，本次决斗获胜只能获得金币哦。'
        await bot.send(ev, msg)
    if girl_outlimit(gid, id2):
        msg = f'[CQ:at,qq={id2}]您的女友超过了爵位上限，本次决斗获胜只能获得金币哦。'
        await bot.send(ev, msg)
    duel_judger.init_isaccept(gid)
    duel_judger.set_duelid(gid, id1, id2)
    duel_judger.turn_on_accept(gid)
    msg = f'[CQ:at,qq={id2}]对方向您发起了优雅的贵族决斗，请在{WAIT_TIME}秒内[接受/拒绝]。'

    await bot.send(ev, msg)
    await asyncio.sleep(WAIT_TIME)
    duel_judger.turn_off_accept(gid)
    if duel_judger.get_isaccept(gid) is False:
        msg = '决斗被拒绝。'
        duel_judger.turn_off(gid)
        await bot.send(ev, msg, at_sender=True)
        return
    daily_duel_limiter.increase(guid)
    duel = DuelCounter()
    level1 = duel._get_level(gid, id1)
    noblename1 = get_noblename(level1)
    level2 = duel._get_level(gid, id2)
    noblename2 = get_noblename(level2)
    msg = f'''对方接受了决斗！    
1号：[CQ:at,qq={id1}]
爵位为：{noblename1}
2号：[CQ:at,qq={id2}]
爵位为：{noblename2}
其他人请在{DUEL_SUPPORT_TIME}秒选择支持的对象。
[支持1/2号xxx金币]'''

    await bot.send(ev, msg)
    duel_judger.turn_on_support(gid)
    await asyncio.sleep(DUEL_SUPPORT_TIME)
    duel_judger.turn_off_support(gid)
    deadnum = random.randint(1, 6)
    duel_judger.set_deadnum(gid, deadnum)
    duel_judger.init_turn(gid)
    duel_judger.turn_on_fire(gid)
    duel_judger.turn_off_hasfired(gid)
    msg = f'支持环节结束，下面请决斗双方轮流[开枪]。\n[CQ:at,qq={id1}]先开枪，30秒未开枪自动认输'

    await bot.send(ev, msg)
    n = 1
    while (n <= 6):
        wait_n = 0
        while (wait_n < 30):
            if duel_judger.get_on_off_hasfired_status(gid):
                break

            wait_n += 1
            await asyncio.sleep(1)
        if wait_n >= 30:
            # 超时未开枪的胜负判定
            loser = duel_judger.get_duelid(gid)[duel_judger.get_turn(gid) - 1]
            winner = duel_judger.get_duelid(gid)[2 - duel_judger.get_turn(gid)]
            msg = f'[CQ:at,qq={loser}]\n你明智的选择了认输。'
            await bot.send(ev, msg)

            #记录本局为超时局。
            is_overtime = 1

            break
        else:
            if n == duel_judger.get_deadnum(gid):
                # 被子弹打到的胜负判定
                loser = duel_judger.get_duelid(gid)[duel_judger.get_turn(gid) -
                                                    1]
                winner = duel_judger.get_duelid(gid)[2 -
                                                     duel_judger.get_turn(gid)]
                msg = f'[CQ:at,qq={loser}]\n砰！你死了。'
                await bot.send(ev, msg)
                break
            else:
                id = duel_judger.get_duelid(gid)[duel_judger.get_turn(gid) - 1]
                id2 = duel_judger.get_duelid(gid)[2 -
                                                  duel_judger.get_turn(gid)]
                msg = f'[CQ:at,qq={id}]\n砰！松了一口气，你并没有死。\n[CQ:at,qq={id2}]\n轮到你开枪了哦。'
                await bot.send(ev, msg)
                n += 1
                duel_judger.change_turn(gid)
                duel_judger.turn_off_hasfired(gid)
                duel_judger.turn_on_fire(gid)
    score_counter = ScoreCounter2()
    cidlist = duel._get_cards(gid, loser)
    selected_girl = random.choice(cidlist)
    wife = duel._search_wife(gid, loser)

    #结算下注金币，判定是否为超时局。
    if is_overtime == 1 and n != 6:
        msg = '本局为超时局，不进行金币结算，支持的金币全部返还。'
        await bot.send(ev, msg)
        duel_judger.set_support(ev.group_id)
        duel_judger.turn_off(ev.group_id)
        return

    #判定被输掉的是否是复制人可可萝，是则换成金币。
    if selected_girl == 9999:
        score_counter._add_score(gid, winner, 300)
        c = chara.fromid(1059)
        duel._delete_card(gid, loser, selected_girl)
        msg = f'[CQ:at,qq={winner}]\n您赢得了神秘的可可萝，但是她微笑着消失了。\n本次决斗获得了300金币。'
        await bot.send(ev, msg)
        msg = f'[CQ:at,qq={loser}]\n您输掉了贵族决斗，被抢走了女友\n{c.name}，\n只要招募，她就还会来到你的身边哦。{c.icon.cqcode}'
        await bot.send(ev, msg)

    #判断被输掉的是否为妻子。
    elif selected_girl == wife:
        score_counter._add_score(gid, winner, 300)
        msg = f'[CQ:at,qq={winner}]您赢得的角色为对方的妻子，\n您改为获得300金币。'
        await bot.send(ev, msg)
        score_counter._reduce_prestige(gid, loser, 500)
        msg = f'[CQ:at,qq={loser}]您差点输掉了妻子，失去了500声望。'
        await bot.send(ev, msg)

    elif girl_outlimit(gid, winner):
        score_counter._add_score(gid, winner, 300)
        msg = f'[CQ:at,qq={winner}]您的女友超过了爵位上限，\n本次决斗获得了300金币。'
        await bot.send(ev, msg)
        c = chara.fromid(selected_girl)
        #判断好感是否足够，足够则扣掉好感
        favor = duel._get_favor(gid, loser, selected_girl)
        if favor >= 50:
            duel._reduce_favor(gid, loser, selected_girl, 50)
            msg = f'[CQ:at,qq={loser}]您输掉了贵族决斗，您与{c.name}的好感下降了50点。\n{c.icon.cqcode}'
            await bot.send(ev, msg)
        else:
            duel._delete_card(gid, loser, selected_girl)
            msg = f'[CQ:at,qq={loser}]您输掉了贵族决斗且对方超过了爵位上限，您的女友恢复了单身。\n{c.name}{c.icon.cqcode}'
            await bot.send(ev, msg)

    else:
        #判断好感是否足够，足够则扣掉好感
        favor = duel._get_favor(gid, loser, selected_girl)
        if favor >= 50:
            c = chara.fromid(selected_girl)
            duel._reduce_favor(gid, loser, selected_girl, 50)
            msg = f'[CQ:at,qq={loser}]您输掉了贵族决斗，您与{c.name}的好感下降了50点。\n{c.icon.cqcode}'
            await bot.send(ev, msg)
            score_counter._add_score(gid, winner, 300)
            msg = f'[CQ:at,qq={winner}]您赢得了决斗，对方女友仍有一定好感。\n本次决斗获得了300金币。'
            await bot.send(ev, msg)
        else:
            c = chara.fromid(selected_girl)
            duel._delete_card(gid, loser, selected_girl)
            duel._add_card(gid, winner, selected_girl)
            msg = f'[CQ:at,qq={loser}]您输掉了贵族决斗，您被抢走了女友\n{c.name}{c.icon.cqcode}'
            await bot.send(ev, msg)
            #判断赢家的角色列表里是否有复制人可可萝。
            wincidlist = duel._get_cards(gid, winner)
            if 9999 in wincidlist:
                duel._delete_card(gid, winner, 9999)
                score_counter._add_score(gid, winner, 300)
                msg = f'[CQ:at,qq={winner}]\n“主人有了女友已经不再孤单了，我暂时离开了哦。”\n您赢得了{c.name},可可萝微笑着消失了。\n您获得了300金币。'
                await bot.send(ev, msg)

    #判断胜者败者是否需要增减声望
    winprestige = score_counter._get_prestige(gid, winner)
    if winprestige != None:
        score_counter._add_prestige(gid, winner, 200)
        msg = f'[CQ:at,qq={winner}]决斗胜利使您的声望上升了200点。'
        await bot.send(ev, msg)
    loseprestige = score_counter._get_prestige(gid, loser)
    if loseprestige != None:
        score_counter._reduce_prestige(gid, loser, 100)
        msg = f'[CQ:at,qq={loser}]决斗失败使您的声望下降了100点。'
        await bot.send(ev, msg)

    #判定败者是否掉爵位，国王以上不会因为决斗掉爵位。
    level_loser = duel._get_level(gid, loser)
    if level_loser > 1 and level_loser < 6:
        noblename_loser = get_noblename(level_loser)
        girlnum_loser = LEVEL_GIRL_NEED[str(level_loser - 1)]
        cidlist_loser = duel._get_cards(gid, loser)
        cidnum_loser = len(cidlist_loser)
        if cidnum_loser < girlnum_loser:
            duel._reduce_level(gid, loser)
            new_noblename = get_noblename(level_loser - 1)
            msg = f'[CQ:at,qq={loser}]\n您的女友数为{cidnum_loser}名\n小于爵位需要的女友数{girlnum_loser}名\n您的爵位下降到了{new_noblename}'
            await bot.send(ev, msg)
    
    #结算下注金币
    support = duel_judger.get_support(gid)
    winuid = []
    supportmsg = '金币结算:\n'
    winnum = duel_judger.get_duelnum(gid, winner)

    if support != 0:
        for uid in support:
            support_id = support[uid][0]
            support_score = support[uid][1]
            if support_id == winnum:
                winuid.append(uid)
                #这里是赢家获得的金币结算，可以自己修改倍率。
                winscore = support_score * WIN_NUM
                score_counter._add_score(gid, uid, winscore)
                supportmsg += f'[CQ:at,qq={uid}]+{winscore}金币\n'
            else:
                score_counter._reduce_score(gid, uid, support_score)
                supportmsg += f'[CQ:at,qq={uid}]-{support_score}金币\n'
    await bot.send(ev, supportmsg)
    duel_judger.set_support(ev.group_id)
    duel_judger.turn_off(ev.group_id)
    return


@sv.on_fullmatch('接受')
async def duelaccept(bot, ev: CQEvent):
    gid = ev.group_id
    if duel_judger.get_on_off_accept_status(gid):
        if ev.user_id == duel_judger.get_duelid(gid)[1]:
            gid = ev.group_id
            msg = '贵族决斗接受成功，请耐心等待决斗开始。'
            await bot.send(ev, msg, at_sender=True)
            duel_judger.turn_off_accept(gid)
            duel_judger.on_isaccept(gid)
        else:
            print('不是被决斗者')
    else:
        print('现在不在决斗期间')


@sv.on_fullmatch('拒绝')
async def duelrefuse(bot, ev: CQEvent):
    gid = ev.group_id
    if duel_judger.get_on_off_accept_status(gid):
        if ev.user_id == duel_judger.get_duelid(gid)[1]:
            gid = ev.group_id
            msg = '您已拒绝贵族决斗。'
            await bot.send(ev, msg, at_sender=True)
            duel_judger.turn_off_accept(gid)
            duel_judger.off_isaccept(gid)


@sv.on_fullmatch('开枪')
async def duelfire(bot, ev: CQEvent):
    gid = ev.group_id
    if duel_judger.get_on_off_fire_status(gid):
        if ev.user_id == duel_judger.get_duelid(gid)[duel_judger.get_turn(gid)
                                                     - 1]:
            duel_judger.turn_on_hasfired(gid)
            duel_judger.turn_off_fire(gid)


@sv.on_rex(r'^支持(1|2)号(\d+)(金币|币)$')
async def on_input_duel_score(bot, ev: CQEvent):
    try:
        if duel_judger.get_on_off_support_status(ev.group_id):
            gid = ev.group_id
            uid = ev.user_id

            match = ev['match']
            select_id = int(match.group(1))
            input_score = int(match.group(2))
            print(select_id, input_score)
            score_counter = ScoreCounter2()
            # 若下注该群下注字典不存在则创建
            if duel_judger.get_support(gid) == 0:
                duel_judger.set_support(gid)
            support = duel_judger.get_support(gid)
            # 检查是否重复下注
            if uid in support:
                msg = '您已经支持过了。'
                await bot.send(ev, msg, at_sender=True)
                return
            # 检查是否是决斗人员
            duellist = duel_judger.get_duelid(gid)
            if uid in duellist:
                msg = '决斗参与者不能支持。'
                await bot.send(ev, msg, at_sender=True)
                return

                # 检查金币是否足够下注
            if score_counter._judge_score(gid, uid, input_score) == 0:
                msg = '您的金币不足。'
                await bot.send(ev, msg, at_sender=True)
                return
            else:
                duel_judger.add_support(gid, uid, select_id, input_score)
                msg = f'支持{select_id}号成功。'
                await bot.send(ev, msg, at_sender=True)
    except Exception as e:
        await bot.send(ev, '错误:\n' + str(e))


# 以下部分与赛跑的重合，有一个即可，两个插件都装建议注释掉。
@sv.on_prefix(['领金币', '领取金币'])
async def add_score(bot, ev: CQEvent):
    try:
        score_counter = ScoreCounter2()
        gid = ev.group_id
        uid = ev.user_id

        current_score = score_counter._get_score(gid, uid)
        if current_score <50:
            score_counter._add_score(gid, uid, ZERO_GET_AMOUNT)
            msg = f'您已领取{ZERO_GET_AMOUNT}金币'
            await bot.send(ev, msg, at_sender=True)
            return
        else:
            msg = '金币小于50才能领取哦。'
            await bot.send(ev, msg, at_sender=True)
            return
    except Exception as e:
        await bot.send(ev, '错误:\n' + str(e))


@sv.on_prefix(['查金币', '查询金币'])
async def get_score(bot, ev: CQEvent):
    try:
        score_counter = ScoreCounter2()
        gid = ev.group_id
        uid = ev.user_id

        current_score = score_counter._get_score(gid, uid)
        msg = f'您的金币为{current_score}'
        await bot.send(ev, msg, at_sender=True)
        return
    except Exception as e:
        await bot.send(ev, '错误:\n' + str(e))

@sv.on_prefix(('充值金币'))
async def cheat_score(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.finish(ev, '不要想着走捷径哦', at_sender=True)
    gid = ev.group_id
    uid = ev.user_id
    id = None
    num = ev.message.extract_plain_text().strip()
    if not num.isdigit() and '*' not in num:
        await bot.send(ev, '请正确输入充值金币的数量')
        return
    num = eval(num)
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            id = int(m.data['qq'])
    if id is None:
        id = uid
    duel = DuelCounter()
    score_counter = ScoreCounter2()
    if duel._get_level(gid, id) == 0:
        await bot.finish(ev, '该用户还未在本群创建贵族哦', at_sender=True)
    score_counter._add_score(gid, id, num)
    score = score_counter._get_score(gid, id)
    msg = f'已为[CQ:at,qq={id}]充值{num}金币\n现在共有{score}金币'
    await bot.send(ev, msg)

@sv.on_prefix(('转账金币'))
async def trade_score(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    id = None
    num = ev.message.extract_plain_text().strip()
    if not num.isdigit() and '*' not in num:
        await bot.send(ev, '请正确输入转账金币的数量')
        return
    num = eval(num)
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            id = int(m.data['qq'])
    if sid is None:
        await bot.send(ev, '请正确at转账人')
        return
    duel = DuelCounter()
    score_counter = ScoreCounter2()
    if duel._get_level(gid, id) == 0:
        await bot.finish(ev, '该用户还未在本群创建贵族哦。', at_sender=True)
    score = score_counter._get_score(gid, uid)
    if score < num:
        msg = f'您的金币不足{num}哦。'
        await bot.send(ev, msg, at_sender=True)
        return
    else:
        score_counter._add_score(gid, id, num)
        score = score_counter._get_score(gid, id)
        score_counter._reduce_score(gid, uid, num)
        scoreyou = score_counter._get_score(gid, uid)
        msg = f'已为[CQ:at,qq={id}]转账{num}金币。\n您的金币剩余{scoreyou}金币，对方金币剩余{score}金币。'
        await bot.send(ev, msg)


@sv.on_fullmatch('重置决斗')
async def init_duel(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '只有群管理才能使用重置决斗哦。', at_sender=True)
    duel_judger.turn_off(ev.group_id)
    msg = '已重置本群决斗状态！'
    await bot.send(ev, msg, at_sender=True)


@sv.on_prefix(['查女友', '查询女友'])
async def search_girl(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    gid = ev.group_id
    if not args:
        await bot.send(ev, '请输入查女友+pcr角色名。', at_sender=True)
        return
    name = args[0]
    cid = chara.name2id(name)
    if cid == 1000:
        await bot.send(ev, '请输入正确的pcr角色名。', at_sender=True)
        return
    duel = DuelCounter()
    owner = duel._get_card_owner(gid, cid)
    c = chara.fromid(cid)
    mes = c.icon.cqcode
    #判断是否是妻子。
    if duel._get_wife_owner(gid, cid) != 0:
        owner = duel._get_wife_owner(gid, cid)
        await bot.finish(ev,
                         f'\n{c.name}现在是\n[CQ:at,qq={owner}]的妻子哦。{mes}',
                         at_sender=True)

    if owner == 0:
        await bot.send(ev, f'{c.name}现在还是单身哦，快去约到她吧。{mes}', at_sender=True)
        return
    else:
        msg = f'{c.name}现在正在\n[CQ:at,qq={owner}]的身边哦。{mes}'
        await bot.send(ev, msg)


#重置某一用户的金币，只用做必要时删库用。
@sv.on_prefix('重置金币')
async def reset_score(bot, ev: CQEvent):
    gid = ev.group_id
    if not priv.check_priv(ev, priv.OWNER):
        await bot.finish(ev, '只有群主才能使用重置金币功能哦。', at_sender=True)
    args = ev.message.extract_plain_text().split()
    if len(args) >= 2:
        await bot.finish(ev, '指令格式错误', at_sender=True)
    if len(args) == 0:
        await bot.finish(ev, '请输入重置金币+被重置者QQ', at_sender=True)
    else:
        id = args[0]
        duel = DuelCounter()
        if duel._get_level(gid, id) == 0:
            await bot.finish(ev, '该用户还未在本群创建贵族哦。', at_sender=True)
        score_counter = ScoreCounter2()
        current_score = score_counter._get_score(gid, id)
        score_counter._reduce_score(gid, id, current_score)
        await bot.finish(ev, f'已清空用户{id}的金币。', at_sender=True)


#注意会清空此人的角色以及贵族等级，只用做必要时删库用。
@sv.on_prefix(['重置角色','贵族转生'])
async def reset_chara(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    args = ev.message.extract_plain_text().split()
    if len(args) >= 2:
        await bot.finish(ev, '指令格式错误', at_sender=True)
    if len(args) == 0:
        duel = DuelCounter()
        if duel._get_level(gid, uid) == 0:
            await bot.finish(ev, '该用户还未在本群创建贵族哦。', at_sender=True)
        cidlist = duel._get_cards(gid, uid)
        for cid in cidlist:
            duel._delete_card(gid, uid, cid)
        wife = duel._search_wife(gid, uid)
        duel._delete_wife_owner(gid, wife)
        duel._set_level(gid, uid, 0)
        await bot.finish(ev, f'已清空用户{uid}的女友和贵族等级。', at_sender=True)
    else:
        if not priv.check_priv(ev, priv.OWNER):
            await bot.finish(ev, '只有群主才能重置别人的角色哦。', at_sender=True)
        id = args[0]
        duel = DuelCounter()
        if duel._get_level(gid, id) == 0:
            await bot.finish(ev, '该用户还未在本群创建贵族哦。', at_sender=True)
        cidlist = duel._get_cards(gid, id)
        for cid in cidlist:
            duel._delete_card(gid, id, cid)
        wife = duel._search_wife(gid, id)
        duel._delete_wife_owner(gid, wife)
        duel._set_level(gid, id, 0)
        await bot.finish(ev, f'已清空用户{id}的女友和贵族等级。', at_sender=True)


@sv.on_prefix(['分手','分手女友'])
async def breakup(bot, ev: CQEvent):
    if BREAK_UP_SWITCH == True:
        args = ev.message.extract_plain_text().split()
        gid = ev.group_id
        uid = ev.user_id
        duel = DuelCounter()
        level = duel._get_level(gid, uid)
        if duel_judger.get_on_off_status(ev.group_id):
            msg = '现在正在决斗中哦，请决斗后再来谈分手事宜吧。'
            await bot.finish(ev, msg, at_sender=True)
        if level == 0:
            await bot.finish(ev, '该用户还未在本群创建贵族哦。', at_sender=True)
        if not args:
            await bot.finish(ev, '请输入分手女友+pcr角色名。', at_sender=True)
        name = args[0]
        cid = chara.name2id(name)
        if cid == 1000:
            await bot.finish(ev, '请输入正确的pcr角色名。', at_sender=True)
        score_counter = ScoreCounter2()
        needscore = 400 + level * 100
        score = score_counter._get_score(gid, uid)
        cidlist = duel._get_cards(gid, uid)
        if cid not in cidlist:
            await bot.finish(ev, '该角色不在你的身边哦。', at_sender=True)
        #检测是否是妻子
        wife = duel._search_wife(gid, uid)
        if cid == wife:
            await bot.finish(ev, '不可以和您的妻子分手哦。', at_sender=True)
        if score < needscore:
            msg = f'您的爵位分手一位女友需要{needscore}金币哦。\n分手不易，做好准备再来吧。'
            await bot.finish(ev, msg, at_sender=True)
        score_counter._reduce_score(gid, uid, needscore)
        duel._delete_card(gid, uid, cid)
        c = chara.fromid(cid)
        msg = f'\n“真正离开的那次，关门声最小。”\n你和{c.name}分手了。失去了{needscore}金币分手费。\n{c.icon.cqcode}'
        await bot.send(ev, msg, at_sender=True)


#国王以上声望部分
@sv.on_fullmatch('开启声望系统')
async def open_prestige(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    level = duel._get_level(gid, uid)
    score_counter = ScoreCounter2()
    prestige = score_counter._get_prestige(gid, uid)
    if prestige != None:
        await bot.finish(ev, '您已经开启了声望系统哦。', at_sender=True)
    if level < 5:
        await bot.finish(ev, '只有公爵及以上才可以开启声望系统哦。', at_sender=True)
    score_counter._set_prestige(gid, uid, 0)
    msg = '成功开启声望系统！殿下，向着成为皇帝的目标进发吧。'
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(['声望系统帮助','声望帮助'])
async def prestige_help(bot, ev: CQEvent):
    msg = '''
成为公爵后才可以开启声望系统
开启后可以通过决斗等方式获取声望
声望系统相关指令如下
1. 开启声望系统
2. 查询声望
3. 加冕称帝(需要5000声望，5000金币）
4. 皇室婚礼+角色名(需3000声望，3000金币)
5.飞升成神(需要5000声望，10000金币）

决斗胜利+200声望
决斗失败-100声望
皇室婚礼需皇帝才能举办
每位皇帝只能举办一次
妻子不会因决斗被抢走

 '''
    data ={
            "type": "node",
            "data": {
                "name": '佩可莉姆',
                "uin": '2651026038',
                "content": msg
            }
            }
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)


@sv.on_fullmatch(['查询声望','查声望'])
async def inquire_prestige(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    level = duel._get_level(gid, uid)
    score_counter = ScoreCounter2()
    prestige = score_counter._get_prestige(gid, uid)
    if prestige == None:
        await bot.finish(ev, '您还未开启声望系统哦。', at_sender=True)
    msg = f'您的声望为{prestige}点。'
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(['加冕称帝', '加冕仪式'])
async def be_emperor(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    level = duel._get_level(gid, uid)
    score_counter = ScoreCounter2()
    prestige = score_counter._get_prestige(gid, uid)

    if prestige == None:
        await bot.finish(ev, '您还未开启声望系统哦。', at_sender=True)
    if level != 6:
        await bot.finish(ev, '只有国王才能进行加冕仪式哦。', at_sender=True)

    if prestige < 5000:
        await bot.finish(ev, '加冕仪式需要5000声望，您的声望不足哦。', at_sender=True)
    score = score_counter._get_score(gid, uid)
    if score < 5000:
        await bot.finish(ev, '加冕仪式需要5000金币，您的金币不足哦。', at_sender=True)
    score_counter._reduce_score(gid, uid, 5000)
    score_counter._reduce_prestige(gid, uid, 5000)
    duel._set_level(gid, uid, 7)
    msg = '\n礼炮鸣响，教皇领唱“感恩赞美歌”。“皇帝万岁！”\n在民众的欢呼声中，你加冕为了皇帝。\n花费了5000点声望，5000金币。'
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(['飞升成神'])
async def be_god(bot, ev: CQEvent): 
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    level = duel._get_level(gid, uid)
    score_counter = ScoreCounter2()  
    prestige = score_counter._get_prestige(gid,uid)
    
    if level!=7:
        await bot.finish(ev, '只有皇帝才能飞升哦。', at_sender=True)

    if prestige < 5000: 
        await bot.finish(ev, '飞升成神需要5000声望，您的声望不足哦。', at_sender=True)
    score = score_counter._get_score(gid, uid)
    if score < 10000:
        await bot.finish(ev, '飞升成神需要10000金币，您的金币不足哦。', at_sender=True)
    score_counter._reduce_score(gid,uid,10000)
    score_counter._reduce_prestige(gid,uid,5000)
    duel._set_level(gid, uid, 8)
    msg = '\n光柱冲天，你感觉无尽的力量涌入了自己的体内。\n在民众的惊讶的目光中，你飞升成神了。\n花费了5000点声望，10000金币。'
    await bot.send(ev, msg, at_sender=True)


@sv.on_prefix('皇室婚礼')
async def marry_wife(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    level = duel._get_level(gid, uid)
    score_counter = ScoreCounter2()
    prestige = score_counter._get_prestige(gid, uid)
    if prestige == None:
        await bot.finish(ev, '您还未开启声望系统哦。', at_sender=True)
    if level < 5:
        await bot.finish(ev, '只有公爵及以上才可以举办皇室婚礼哦。', at_sender=True)
    if duel._search_wife(gid, uid) != 0:
        await bot.finish(ev, '只可以举办一次皇室婚礼哦。', at_sender=True)
    if not args:
        await bot.finish(ev, '请输入皇室婚礼+pcr角色名。', at_sender=True)
    name = args[0]
    cid = chara.name2id(name)
    if cid == 1000:
        await bot.finish(ev, '请输入正确的pcr角色名。', at_sender=True)
    cidlist = duel._get_cards(gid, uid)
    if cid not in cidlist:
        await bot.finish(ev, '该角色不在你的身边哦。', at_sender=True)
    if prestige < 3000:
        await bot.finish(ev, '皇室婚礼需要3000声望，您的声望不足哦。', at_sender=True)
    score = score_counter._get_score(gid, uid)
    if score < 3000:
        await bot.finish(ev, '皇室婚礼需要3000金币，您的金币不足哦。', at_sender=True)
    favor = duel._get_favor(gid, uid, cid)
    if favor < 300:
        await bot.finish(ev, '举办婚礼的女友需要达到300好感，您的好感不足哦。', at_sender=True)

    score_counter._reduce_prestige(gid, uid, 3000)
    score_counter._reduce_score(gid, uid, 3000)
    duel._set_wife_owner(gid, cid, uid)
    c = chara.fromid(cid)
    msg = f'繁杂的皇室礼仪过后\n\n{c.name}与[CQ:at,qq={uid}]\n\n正式踏上了婚礼的殿堂\n成为了他的妻子。\n让我们为他们表示祝贺！\n妻子不会因决斗被抢走了哦。\n{c.icon.cqcode}'
    await bot.send(ev, msg)


#返回好感对应的关系和文本
def get_relationship(favor):
    for relation in RELATIONSHIP_DICT.keys():
        if favor >= relation:
            relationship = RELATIONSHIP_DICT[relation]
    return relationship[0], relationship[1]

@sv.on_fullmatch(['好感系统帮助' '好感帮助'])
async def gift_help(bot, ev: CQEvent):
    msg = '''
╔                                        ╗  

             好感系统帮助

1. 查好感+女友名
2. 贵族约会+女友名(1天限1次)
3. 买礼物(300金币，一天限5次）
4. 送礼物+女友名
5. 用xx与[艾特对象]交换xx
例: 用热牛奶与@七曜圣贤交换书
6. 购买情报+女友名(500金币，可了解女友喜好)
7. 礼物查询(查询礼物仓库)
8. 好感列表

注:
通过约会或者送礼可以提升好感
决斗输掉某女友会扣除50好感，不够则被抢走
与女友结婚需要是公爵以上且好感在依恋(300)以上
女友喜好与原角色无关，只是随机生成，仅供娱乐

╚                                        ╝

 '''
    data ={
            "type": "node",
            "data": {
                "name": '佩可莉姆',
                "uin": '2651026038',
                "content": msg
            }
            }
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=data)



@sv.on_prefix(['查好感', '查询好感'])
async def girl_story(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    if not args:
        await bot.finish(ev, '请输入查好感+女友名。', at_sender=True)
    name = args[0]
    cid = chara.name2id(name)
    if cid == 1000:
        await bot.finish(ev, '请输入正确的女友名。', at_sender=True)
    cidlist = duel._get_cards(gid, uid)
    if cid not in cidlist:
        await bot.finish(ev, '该女友不在你的身边哦。', at_sender=True)

    if duel._get_favor(gid, uid, cid) == None:
        duel._set_favor(gid, uid, cid, 0)
    favor = duel._get_favor(gid, uid, cid)
    relationship, text = get_relationship(favor)
    c = chara.fromid(cid)
    mes = c.icon.cqcode
    msg = f'\n{c.name}对你的好感是{favor}\n你们的关系是{relationship}\n“{text}”\n{mes}'
    await bot.send(ev, msg, at_sender=True)


@sv.on_prefix(['贵族约会'])
async def daily_date(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    if not args:
        await bot.finish(ev, '请输入贵族约会+女友名。', at_sender=True)
    name = args[0]
    cid = chara.name2id(name)
    if cid == 1000:
        await bot.finish(ev, '请输入正确的女友名。', at_sender=True)
    cidlist = duel._get_cards(gid, uid)
    if cid not in cidlist:
        await bot.finish(ev, '该女友不在你的身边哦。', at_sender=True)
    guid = gid, uid
    if not daily_date_limiter.check(guid):
        await bot.finish(ev, '今天已经和女友约会过了哦，明天再来吧。', at_sender=True)

    loginnum_ = ['1', '2', '3', '4']
    r_ = [0.2, 0.4, 0.35, 0.05]
    sum_ = 0
    ran = random.random()
    for num, r in zip(loginnum_, r_):
        sum_ += r
        if ran < sum_: break
    Bonus = {
        '1': [5, Date5],
        '2': [10, Date10],
        '3': [15, Date15],
        '4': [20, Date20]
    }
    favor = Bonus[num][0]
    text = random.choice(Bonus[num][1])
    duel._add_favor(gid, uid, cid, favor)
    c = chara.fromid(cid)
    current_favor = duel._get_favor(gid, uid, cid)
    relationship = get_relationship(current_favor)[0]
    msg = f'\n\n{text}\n\n你和{c.name}的好感上升了{favor}点\n她现在对你的好感是{current_favor}点\n你们现在的关系是{relationship}\n{c.icon.cqcode}'
    daily_date_limiter.increase(guid)
    await bot.send(ev, msg, at_sender=True)


#根据角色id和礼物id，返回增加的好感和文本
def check_gift(cid, giftid):
    lastnum = cid % 10
    if lastnum == giftid:
        favor = 10
        text = random.choice(Gift10)
        return favor, text
    num1 = lastnum % 3
    num2 = giftid % 3
    choicelist = GIFTCHOICE_DICT[num1]

    if num2 == choicelist[0]:
        favor = 5
        text = random.choice(Gift5)
        return favor, text
    if num2 == choicelist[1]:
        favor = 2
        text = random.choice(Gift2)
        return favor, text
    if num2 == choicelist[2]:
        favor = 1
        text = random.choice(Gift1)
        return favor, text


@sv.on_prefix(['送礼物'])
async def give_gift(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    if gift_change.get_on_off_giftchange_status(ev.group_id):
        await bot.finish(ev, "有正在进行的礼物交换，礼物交换结束再来送礼物吧。")
    if len(args) != 2:
        await bot.finish(ev, '请输入 送礼物+女友名+礼物名 中间用空格隔开。', at_sender=True)
    name = args[0]
    cid = chara.name2id(name)
    if cid == 1000:
        await bot.finish(ev, '请输入正确的女友名。', at_sender=True)
    cidlist = duel._get_cards(gid, uid)
    if cid not in cidlist:
        await bot.finish(ev, '该女友不在你的身边哦。', at_sender=True)
    gift = args[1]
    if gift not in GIFT_DICT.keys():
        await bot.finish(ev, '请输入正确的礼物名。', at_sender=True)
    gfid = GIFT_DICT[gift]
    if duel._get_gift_num(gid, uid, gfid) == 0:
        await bot.finish(ev, '你的这件礼物的库存不足哦。', at_sender=True)
    duel._reduce_gift(gid, uid, gfid)
    favor, text = check_gift(cid, gfid)
    duel._add_favor(gid, uid, cid, favor)
    current_favor = duel._get_favor(gid, uid, cid)
    relationship = get_relationship(current_favor)[0]
    c = chara.fromid(cid)
    msg = f'\n{c.name}:“{text}”\n\n你和{c.name}的好感上升了{favor}点\n她现在对你的好感是{current_favor}点\n你们现在的关系是{relationship}\n{c.icon.cqcode}'
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(['买礼物'])
async def buy_gift(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    score_counter = ScoreCounter2()
    guid = gid, uid
    if duel_judger.get_on_off_status(ev.group_id):
        msg = '现在正在决斗中哦，请决斗后再来买礼物吧。'
        await bot.finish(ev, msg, at_sender=True)
    score = score_counter._get_score(gid, uid)
    if score < 300:
        await bot.finish(ev, '购买礼物需要300金币，您的金币不足哦。', at_sender=True)
    if not daily_gift_limiter.check(guid):
        await bot.finish(ev,
                         f'今天购买礼物已经超过{GIFT_DAILY_LIMIT}次了哦，明天再来吧。',
                         at_sender=True)
    select_gift = random.choice(list(GIFT_DICT.keys()))
    gfid = GIFT_DICT[select_gift]
    duel._add_gift(gid, uid, gfid)
    msg = f'\n您花费了300金币，\n买到了[{select_gift}]哦，\n欢迎下次惠顾。'
    score_counter._reduce_score(gid, uid, 300)
    daily_gift_limiter.increase(guid)
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(['查询礼物', '礼物查询', '查礼物'])
async def my_gift(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    msg = f'\n您的礼物仓库如下:'
    giftmsg = ''
    for gift in GIFT_DICT.keys():
        gfid = GIFT_DICT[gift]
        num = duel._get_gift_num(gid, uid, gfid)
        if num != 0:
            #补空格方便对齐
            length = len(gift)
            msg_part = '    ' * (4 - length)
            giftmsg += f'\n{gift}{msg_part}: {num}件'
    if giftmsg == '':
        await bot.finish(ev, '您现在没有礼物哦，快去发送 买礼物 购买吧。', at_sender=True)
    msg += giftmsg

    await bot.send(ev, msg, at_sender=True)


@sv.on_rex(f'^用(.*)与(.*)交换(.*)$')
async def change_gift(bot, ev: CQEvent):
    gid = ev.group_id
    duel = DuelCounter()
    if gift_change.get_on_off_giftchange_status(ev.group_id):
        await bot.finish(ev, "有正在进行的礼物交换，请勿重复使用指令。")
    gift_change.turn_on_giftchange(gid)
    id1 = ev.user_id
    match = ev['match']
    try:
        id2 = int(ev.message[1].data['qq'])
    except:
        gift_change.turn_off_giftchange(ev.group_id)
        await bot.finish(ev, '参数格式错误')
    if id2 == id1:
        await bot.send(ev, "不能和自己交换礼物！", at_sender=True)
        gift_change.turn_off_giftchange(ev.group_id)
        return
    gift1 = match.group(1)
    gift2 = match.group(3)
    if gift1 not in GIFT_DICT.keys():
        gift_change.turn_off_giftchange(ev.group_id)
        await bot.finish(ev, f'礼物1不存在。')
    if gift2 not in GIFT_DICT.keys():
        gift_change.turn_off_giftchange(ev.group_id)
        await bot.finish(ev, f'礼物2不存在。')
    gfid1 = GIFT_DICT[gift1]
    gfid2 = GIFT_DICT[gift2]
    if gfid2 == gfid1:
        await bot.send(ev, "不能交换相同的礼物！", at_sender=True)
        gift_change.turn_off_giftchange(ev.group_id)
        return

    if duel._get_gift_num(gid, id1, gfid1) == 0:
        gift_change.turn_off_giftchange(ev.group_id)
        await bot.finish(ev, f'[CQ:at,qq={id1}]\n您的{gift1}的库存不足哦。')
    if duel._get_gift_num(gid, id2, gfid2) == 0:
        gift_change.turn_off_giftchange(ev.group_id)
        await bot.finish(ev, f'[CQ:at,qq={id2}]\n您的{gift2}的库存不足哦。')
    level2 = duel._get_level(gid, id2)
    noblename = get_noblename(level2)
    gift_change.turn_on_waitchange(gid)
    gift_change.set_changeid(gid, id2)
    gift_change.turn_off_accept_giftchange(gid)
    msg = f'[CQ:at,qq={id2}]\n尊敬的{noblename}您好：\n\n[CQ:at,qq={id1}]试图用[{gift1}]交换您的礼物[{gift2}]。\n\n请在{WAIT_TIME_CHANGE}秒内[接受交换/拒绝交换]。'
    await bot.send(ev, msg)
    await asyncio.sleep(WAIT_TIME_CHANGE)
    gift_change.turn_off_waitchange(gid)
    if gift_change.get_isaccept_giftchange(gid) is False:
        msg = '\n礼物交换被拒绝。'
        gift_change.init_changeid(gid)
        gift_change.turn_off_giftchange(gid)
        await bot.finish(ev, msg, at_sender=True)
    duel._reduce_gift(gid, id1, gfid1)
    duel._add_gift(gid, id1, gfid2)
    duel._reduce_gift(gid, id2, gfid2)
    duel._add_gift(gid, id2, gfid1)
    msg = f'\n礼物交换成功！\n您使用[{gift1}]交换了\n[CQ:at,qq={id2}]的[{gift2}]。'
    gift_change.init_changeid(gid)
    gift_change.turn_off_giftchange(gid)
    await bot.finish(ev, msg, at_sender=True)


@sv.on_fullmatch('接受交换')
async def giftchangeaccept(bot, ev: CQEvent):
    gid = ev.group_id
    if gift_change.get_on_off_waitchange_status(gid):
        if ev.user_id == gift_change.get_changeid(gid):
            msg = '\n礼物交换接受成功，请耐心等待礼物交换结束。'
            await bot.send(ev, msg, at_sender=True)
            gift_change.turn_off_waitchange(gid)
            gift_change.turn_on_accept_giftchange(gid)


@sv.on_fullmatch('拒绝交换')
async def giftchangerefuse(bot, ev: CQEvent):
    gid = ev.group_id
    if gift_change.get_on_off_waitchange_status(gid):
        if ev.user_id == gift_change.get_changeid(gid):
            msg = '\n礼物交换拒绝成功，请耐心等待礼物交换结束。'
            await bot.send(ev, msg, at_sender=True)
            gift_change.turn_off_waitchange(gid)
            gift_change.turn_off_accept_giftchange(gid)


@sv.on_prefix(['购买情报', '买情报'])
async def buy_information(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    score_counter = ScoreCounter2()
    if duel_judger.get_on_off_status(ev.group_id):
        msg = '现在正在决斗中哦，请决斗后再来买情报吧。'
        await bot.finish(ev, msg, at_sender=True)
    if not args:
        await bot.finish(ev, '请输入买情报+女友名。', at_sender=True)
    name = args[0]
    cid = chara.name2id(name)
    if cid == 1000:
        await bot.finish(ev, '请输入正确的女友名。', at_sender=True)
    score = score_counter._get_score(gid, uid)
    if score < 500:
        await bot.finish(ev, '购买女友情报需要500金币，您的金币不足哦。', at_sender=True)
    score_counter._reduce_score(gid, uid, 500)
    last_num = cid % 10
    like = ''
    normal = ''
    dislike = ''
    for gift in GIFT_DICT.keys():
        if GIFT_DICT[gift] == last_num:
            favorite = gift
            continue
        num1 = last_num % 3
        num2 = GIFT_DICT[gift] % 3
        choicelist = GIFTCHOICE_DICT[num1]

        if num2 == choicelist[0]:
            like += f'{gift}\n'
            continue
        if num2 == choicelist[1]:
            normal += f'{gift}\n'
            continue
        if num2 == choicelist[2]:
            dislike += f'{gift}\n'
            continue
    c = chara.fromid(cid)
    msg = f'\n花费了500金币，您买到了以下情报：\n{c.name}最喜欢的礼物是:\n{favorite}\n喜欢的礼物是:\n{like}一般喜欢的礼物是:\n{normal}不喜欢的礼物是:\n{dislike}{c.icon.cqcode}'
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch('重置礼物交换')
async def init_change(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '只有群管理才能使用重置礼物交换哦。', at_sender=True)
    gift_change.turn_off_giftchange(ev.group_id)
    msg = '已重置本群礼物交换状态！'
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(['好感列表'])
async def get_favorlist(bot, ev: CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    if duel._get_level(gid, uid) == 0:
        msg = '您还未在本群创建过贵族，请发送 创建贵族 开始您的贵族之旅。'
        await bot.send(ev, msg, at_sender=True)
        return
    cidlist = duel._get_cards(gid, uid)
    if len(cidlist) == 0:
        await bot.finish(ev, '您现在还没有女友哦。', at_sender=True)
    favorlist = []
    for cid in cidlist:
        favor = duel._get_favor(gid, uid, cid)
        if favor != 0 and favor != None:
            favorlist.append({"cid": cid, "favor": favor})
    if len(favorlist) == 0:
        await bot.finish(ev, '您的女友好感全部为0哦。', at_sender=True)
    rows_by_favor = sorted(favorlist, key=lambda r: r['favor'], reverse=True)
    msg = '\n您好感0以上的女友的前10名如下所示:\n'
    num = min(len(rows_by_favor), 10)
    for i in range(0, num):
        cid = rows_by_favor[i]["cid"]
        favor = rows_by_favor[i]["favor"]
        c = chara.fromid(cid)
        msg += f'{c.name}:{favor}点\n'
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(['购买女友上限'])
async def add_warehouse(bot, ev: CQEvent):
    duel = DuelCounter()
    score_counter = ScoreCounter2()
    gid = ev.group_id
    uid = ev.user_id
    level = duel._get_level(gid, uid)
    current_score = score_counter._get_score(gid, uid)
    if duel_judger.get_on_off_status(ev.group_id):
        msg = '现在正在决斗中哦，请决斗后再来购买上限吧。'
        await bot.finish(ev, msg, at_sender=True)
    if level < 6:
        await bot.finish(ev, '只有国王以上才能增加女友上限哦。', at_sender=True)

    if current_score < SHANGXIAN_NUM:
        msg = f'增加女友上限需要消耗{SHANGXIAN_NUM}金币，您的金币不足哦。'
        await bot.send(ev, msg, at_sender=True)
        return
    else:
        housenum = duel._get_warehouse(gid, uid)
        if housenum >= WAREHOUSE_NUM:
            msg = f'您已增加{WAREHOUSE_NUM}次上限，无法继续增加了哦。'
            await bot.finish(ev, msg, at_sender=True)
        duel._add_warehouse(gid, uid, 1)
        score_counter._reduce_score(gid, uid, SHANGXIAN_NUM)
        last_score = current_score - SHANGXIAN_NUM
        myhouse = get_girlnum(gid, uid)
        msg = f'您消耗了{SHANGXIAN_NUM}金币，增加了1个女友上限，目前剩余{last_score}金币，女友上限为{myhouse}名'
        await bot.send(ev, msg, at_sender=True)


@sv.on_prefix(['查姓名','查名字', '查昵称'])
async def get_girlname(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    gid = ev.group_id
    uid = ev.user_id
    duel = DuelCounter()
    if not args:
        await bot.finish(ev, '请输入查名字+女友序号(序号即查询贵族中女友排在第几位)。', at_sender=True)
    num = args[0]
    if not num.isdigit():
        await bot.finish(ev, '请输入查名字+女友序号(序号即查询贵族中女友排在第几位)。', at_sender=True)
    num_int = int(num)
    cidlist = duel._get_cards(gid, uid)
    girlnum = len(cidlist)

    if num_int > girlnum:
        await bot.finish(ev,
                         f'你所输入的女友序号{num_int}大于您的女友数{girlnum}名',
                         at_sender=True)
    cid = cidlist[num_int - 1]
    namelist = _pcr_data.CHARA_NAME[cid]
    namemsg = ''
    for name in namelist:
        namemsg += f'{name},'
    namemsg = namemsg[:-1]
    msg = f'\n您的第{num_int}名女友的昵称为:\n\n{namemsg}'

    await bot.send(ev, msg, at_sender=True)


#交易女友
@sv.on_rex(f'^用(\d+)金币与(.*)交易女友(.*)$')
async def cardtrade(bot, ev: CQEvent):
    gid = ev.group_id
    duel = DuelCounter()
    if card_trade.get_trade_on_off_status(ev.group_id):
        await bot.send(ev, "此轮交易还没结束，请勿重复使用指令。")
        return
    card_trade.turn_tradeon(gid)
    id1 = ev.user_id
    match = ev['match']
    try:
        id2 = int(ev.message[1].data['qq'])
    except:
        card_trade.turn_tradeoff(ev.group_id)
        await bot.finish(ev, '参数格式错误')
    if id2 == id1:
        await bot.send(ev, "不能和自己交易女友！", at_sender=True)
        card_trade.turn_tradeoff(ev.group_id)
        return 
        
    num = int(match.group(1))
    name = str(match.group(3))

    score_counter = ScoreCounter2()
    score = score_counter._get_score(gid, id1)
    prestige = score_counter._get_prestige(gid,id1)
    if score < num:
        msg = f'您的金币不足{num}，无法交易哦。'
        card_trade.turn_tradeoff(ev.group_id)
        await bot.send(ev, msg, at_sender=True)
        return
    if prestige < 0:
        msg = f'你现在身败名裂，无法交易哦。'
        card_trade.turn_tradeoff(ev.group_id)
        await bot.send(ev, msg, at_sender=True)
        return
    if girl_outlimit(gid,id1):
        await bot.send(ev, "您的女友超过了爵位上限，无法进行交易哦！", at_sender=True)
        card_trade.turn_tradeoff(ev.group_id)
        return  
    if duel._get_level(gid, id1) == 0:
        msg = f'[CQ:at,qq={id1}]交易发起者还未在创建过贵族\n请发送 创建贵族 开始您的贵族之旅。'
        card_trade.turn_tradeoff(ev.group_id)
        await bot.send(ev, msg)
        return

    if duel._get_level(gid, id2) == 0:
        msg = f'[CQ:at,qq={id2}]被交易者还未在本群创建过贵族'
        card_trade.turn_tradeoff(ev.group_id)
        await bot.send(ev, msg)
        return
        
    if not name:
        await bot.send(ev, f'请输入交易女友的名称\n发送查名字+序号查询女友昵称。', at_sender=True)
        card_trade.turn_tradeoff(ev.group_id)
        return
    cid = chara.name2id(name)
    if cid == 1000:
        await bot.send(ev, f'请输入正确的角色名\n发送查名字+序号查询女友昵称。', at_sender=True)
        card_trade.turn_tradeoff(ev.group_id)
        return
    owner = duel._get_card_owner(gid, cid)
    c = chara.fromid(cid)
    #判断是否是妻子。
    if duel._get_queen_owner(gid,cid) !=0 :
        owner = duel._get_queen_owner(gid,cid)
        card_trade.turn_tradeoff(ev.group_id)
        await bot.finish(ev, f'\n{c.name}现在是\n[CQ:at,qq={owner}]的妻子，无法交易哦。', at_sender=True)

    if owner == 0:
        await bot.send(ev, f'{c.name}现在还是单身哦，快去约到她吧。', at_sender=True)
        card_trade.turn_tradeoff(ev.group_id)
        return
    if id2!=owner:
        msg = f'{c.name}现在正在\n[CQ:at,qq={owner}]的身边哦，您需要与此人进行交易哦。'
        card_trade.turn_tradeoff(ev.group_id)
        await bot.send(ev, msg)
        return
    level2 = duel._get_level(gid, id2)
    noblename = get_noblename(level2)
    card_trade.init_tradeflag(gid)
    card_trade.set_tradeid(gid, id1, id2, cid)
    card_trade.turn_on_trade(gid)
    msg = f'[CQ:at,qq={id2}]尊敬的{noblename}您好\n[CQ:at,qq={id1}]试图以{num}金币的价格购买您的女友{c.name}，请在{WAIT_TIME_TRADE}秒内[接受交易/拒绝交易]，女友交易需要收10%手续费哦。'
    await bot.send(ev, msg)
    
    await asyncio.sleep(WAIT_TIME_TRADE)
    card_trade.turn_off_trade(gid)
    if card_trade.get_tradeflag(gid) is False:
        msg = '交易被拒绝。'
        card_trade.turn_tradeoff(gid)
        await bot.send(ev, msg, at_sender=True)
        return

    get_num=num*0.9
    score_counter._add_score(gid, id2, get_num)
    score = score_counter._get_score(gid, id2)
    
    score_counter._reduce_score(gid, id1, num)
    scoreyou = score_counter._get_score(gid, id1)
    duel._delete_card(gid, id2, cid)
    duel._add_card(gid, id1, cid)
    card_trade.turn_tradeoff(gid)
    msg = f'[CQ:at,qq={id1}]以{num}金币的价格购买了[CQ:at,qq={id2}]的女友{c.name}，交易成功\n[CQ:at,qq={id1}]您失去了{num}金币，{num2}声望，剩余{scoreyou}金币\n[CQ:at,qq={id2}]扣除10%手续费，您能得到了{get_num}金币，剩余{score}金币。{c.icon.cqcode}'
    await bot.send(ev, msg)


@sv.on_fullmatch('接受交易')
async def duelaccept(bot, ev: CQEvent):
    gid = ev.group_id
    if card_trade.get_trade_on_off_status(gid):
        if ev.user_id == card_trade.get_tradeid(gid)[1]:
            gid = ev.group_id
            msg = '女友交易接受成功，请耐心等待交易完成。'
            await bot.send(ev, msg, at_sender=True)
            card_trade.turn_off_trade(gid)
            card_trade.on_tradeflag(gid)

@sv.on_fullmatch('拒绝交易')
async def duelrefuse(bot, ev: CQEvent):
    gid = ev.group_id
    if card_trade.get_trade_on_off_status(gid):
        if ev.user_id == card_trade.get_tradeid(gid)[1]:
            gid = ev.group_id
            msg = '您已拒绝女友交易。'
            await bot.send(ev, msg, at_sender=True)
            card_trade.turn_off_trade(gid)
            card_trade.off_tradeflag(gid)

@sv.on_fullmatch('重置交易')
async def init_duel(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '只有群管理才能使用重置交易哦。', at_sender=True)
    card_trade.turn_tradeoff(ev.group_id)
    msg = '已重置本群交易状态！'
    await bot.send(ev, msg, at_sender=True)



#排行榜
async def get_user_card_dict(bot, group_id):
    mlist = await bot.get_group_member_list(group_id=group_id)
    name = {}
    for m in mlist:
        name[m['user_id']] = m['card'] if m['card']!='' else m['nickname']
    return name

@sv.on_fullmatch(('金币排行榜', '金币排行'))
async def Score_ranking(bot, ev: CQEvent):
    try:
        user_card_dict = await get_user_card_dict(bot, ev.group_id)
        score_dict = {}
        score_counter = ScoreCounter2()
        gid = ev.group_id
        for uid in user_card_dict.keys():
            if uid != ev.self_id:
                score_dict[user_card_dict[uid]] = score_counter._get_score(gid, uid)
        group_ranking = sorted(score_dict.items(), key = lambda x:x[1], reverse = True)
        msg = '此群贵族决斗金币排行为:\n'
        for i in range(min(len(group_ranking), 10)):
            if group_ranking[i][1] != 0:
                msg += f'第{i+1}名: {group_ranking[i][0]}, 金币: {group_ranking[i][1]}\n'
        await bot.send(ev, msg.strip())
    except Exception as e:
        await bot.send(ev, '错误:\n' + str(e))        
        
@sv.on_fullmatch(('声望排行榜', '声望排行'))
async def Prestige_ranking(bot, ev: CQEvent):
    try:
        user_card_dict = await get_user_card_dict(bot, ev.group_id)
        score_dict = {}
        score_counter = ScoreCounter2()
        gid = ev.group_id
        for uid in user_card_dict.keys():
            if uid != ev.self_id:
                score_dict[user_card_dict[uid]] = score_counter._get_prestige(gid, uid)
                if score_dict[user_card_dict[uid]] == None:
                   score_dict[user_card_dict[uid]] = 0
        group_ranking = sorted(score_dict.items(), key = lambda x:x[1], reverse = True)
        msg = '此群贵族对决声望排行为:\n'
        for i in range(min(len(group_ranking), 10)):
            if group_ranking[i][1] != 0:
                msg += f'第{i+1}名: {group_ranking[i][0]}, 声望: {group_ranking[i][1]}\n'
        await bot.send(ev, msg.strip())
    except Exception as e:
        await bot.send(ev, '错误:\n' + str(e))      

@sv.on_fullmatch(('女友排行榜', '女友排行'))
async def Card_ranking(bot, ev: CQEvent):
    try:
        user_card_dict = await get_user_card_dict(bot, ev.group_id)
        score_dict = {}
        score_counter = ScoreCounter2()
        duel = DuelCounter()
        gid = ev.group_id
        for uid in user_card_dict.keys():
            if uid != ev.self_id:
                cidlist = duel._get_cards(gid, uid)
                score_dict[user_card_dict[uid]] = cidnum = len(cidlist)
        group_ranking = sorted(score_dict.items(), key = lambda x:x[1], reverse = True)
        msg = '此群贵族对决女友数排行为:\n'
        for i in range(min(len(group_ranking), 10)):
            if group_ranking[i][1] != 0:
                msg += f'第{i+1}名: {group_ranking[i][0]}, 女友数: {group_ranking[i][1]}\n'
        await bot.send(ev, msg.strip())
    except Exception as e:
        await bot.send(ev, '错误:\n' + str(e))   