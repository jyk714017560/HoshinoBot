import os
import random
from collections import defaultdict
from functools import reduce
import pickle

from hoshino import Service, priv, util
from hoshino.typing import *
from hoshino.util import DailyNumberLimiter, concat_pic, pic2b64

from .. import chara
from .. import _pcr_data
from .gacha import Gacha
from .gachamaster import GachaMaster
from .exception import *

try:
    import ujson as json
except:
    import json

sv_help = '''
[#来发十连] 十连模拟
[#来发单抽] 单抽模拟
[#来一井] 4w5钻！
[查看卡池] 模拟卡池&出率
[切换卡池] 更换模拟卡池
'''.strip()
sv = Service('gacha', help_=sv_help, bundle='pcr娱乐')
jewel_limit = DailyNumberLimiter(7500)
tenjo_limit = DailyNumberLimiter(5)

JEWEL_EXCEED_NOTICE = f'你今天已经抽过{jewel_limit.max}钻了，欢迎明早5点后再来！'
TENJO_EXCEED_NOTICE = f'你今天已经抽过{tenjo_limit.max}张天井券了，欢迎明早5点后再来！'
JEWEL_EMPTY_NOTICE=f'う～ん,骑士君你的宝石不够呢~'
POOL = ('MIX', 'JP', 'TW', 'CN')
DEFAULT_POOL = POOL[3]

_pool_config_file = os.path.expanduser('~/.hoshino/group_pool_config.json')
_group_pool = {}
try:
    with open(_pool_config_file, encoding='utf8') as f:
        _group_pool = json.load(f)
except FileNotFoundError as e:
    sv.logger.warning('group_pool_config.json not found, will create when needed.')
_group_pool = defaultdict(lambda: DEFAULT_POOL, _group_pool)


_colle_config_file = os.path.expanduser('~/.hoshino/colle_enable_config.json')
_colle_enable = {}
try:
    with open(_colle_config_file, encoding='utf8') as f:
        _colle_enable = json.load(f)
except FileNotFoundError as e:
    sv.logger.warning('colle_enable_config.json not found, will create when needed.')
_colle_enable = defaultdict(lambda: False, _colle_enable)

def dump_pool_config():
    with open(_pool_config_file, 'w', encoding='utf8') as f:
        json.dump(_group_pool, f, ensure_ascii=False)


def dump_colle_config():
    with open(_colle_config_file, 'w', encoding='utf8') as f:
        json.dump(_colle_enable, f, ensure_ascii=False)


gacha_10_aliases = ('抽十连', '十连', '十连！', '十连抽', '来个十连', '来发十连', '来次十连', '抽个十连', '抽发十连', '抽次十连', '十连扭蛋', '扭蛋十连',
                    '10连', '10连！', '10连抽', '来个10连', '来发10连', '来次10连', '抽个10连', '抽发10连', '抽次10连', '10连扭蛋', '扭蛋10连')
gacha_1_aliases = ('单抽', '单抽！', '来发单抽', '来个单抽', '来次单抽', '扭蛋单抽', '单抽扭蛋')
gacha_300_aliases = ('抽一井', '来一井', '来发井', '抽发井', '天井扭蛋', '扭蛋天井')


@sv.on_prefix('建立仓库')
async def add_colle(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.finish(ev, '测试功能，仅限主人使用哦', at_sender=True)
    
    uid = str(ev.user_id)
    name = ev.sender['nickname']
    if not _colle_enable[uid]:
        await bot.finish(ev, f'{name}君你还没有开启仓库功能，请使用\"启用仓库\"开启功能')

    gm = GachaMaster(ev.user_id)
    if gm.has_colle():
        await bot.send(ev, '你已经有一个仓库了，不可以重复建立哦~', at_sender=True)
    else:
        colle = pickle.dumps({'贪吃佩可': 1, '可可萝': 1, '凯留': 1, '优衣': 1})
        try:
            gm.add_colle(colle, 45000, 0)
        except DatabaseError as e:
            await bot.finish(ev, f'DatabaseError: {e.message}\nごめんなさい！嘤嘤嘤(〒︿〒)', at_sender=True)
        await bot.send(ev, f'恭喜{name}君的仓库建立成功~')
        await list_colle(bot, ev)


@sv.on_prefix('查看仓库')
async def list_colle(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.finish(ev, '测试功能，仅限主人使用哦', at_sender=True)

    uid = str(ev.user_id)
    name = ev.sender['nickname']
    if not _colle_enable[uid]:
        await bot.finish(ev, f'{name}君你还没有开启仓库功能，请使用\"启用仓库\"开启功能')

    gm = GachaMaster(ev.user_id)
    try:
        db = gm.get_colle()
    except DatabaseError as e:
        await bot.finish(ev, f'DatabaseError: {e.message}\nごめんなさい！嘤嘤嘤(〒︿〒)', at_sender=True)
    if db:
        colle = pickle.loads(db['colle'])
        jewel = db['jewel']
        hiishi = db['hiishi']

        result = []
        pics = []
        collelen = len(colle)
        charalen = len(_pcr_data.CHARA_NAME) - 4

        if collelen <= 20:
            for k, v in colle.items():
                c = chara.fromname(k, v)
                result.append(c)

        else:
            for k, v in colle.items():
                if v >= 3:
                    c = chara.fromname(k, v)
                    result.append(c)
        
        if len(result):
            lenth = len(result)
            random.shuffle(result)
            for i in range(0, lenth, 5):
                j = min(lenth, i + 5)
                pics.append(chara.gen_team_pic(result[i:j], star_slot_verbose=False))
            result = concat_pic(pics)
            result = pic2b64(result)
            result = MessageSegment.image(result)
        
            msg = [f"{name}君的仓库为",
                f"{result}",
                f"图鉴完成度:{collelen}/{charalen}",
                f"宝石:{jewel}, 女神的秘石:{hiishi}"
            ]
            await bot.send(ev, '\n'.join(msg))
        else:
            msg = [f"やばいですね☆, {name}君的仓库一个三星都没有",
                f"图鉴完成度:{collelen}/{charalen}",
                f"宝石:{jewel}, 女神的秘石:{hiishi}"
            ]
            await bot.send(ev, '\n'.join(msg))
    else:
        await bot.send(ev,f'{name}君你还没有仓库，请使用\"建立仓库\"进行初始化')

    
@sv.on_fullmatch(('卡池资讯', '查看卡池', '看看卡池', '康康卡池', '看看up', '看看UP'))
async def gacha_info(bot, ev: CQEvent):
    gid = str(ev.group_id)
    gacha = Gacha(_group_pool[gid])
    up_chara = gacha.up
    up_star = gacha.up_star
    up_prob = gacha.up_prob
    if sv.bot.config.USE_CQPRO:
        up_chara = map(lambda x, y, z: str(chara.fromname(x, y).icon.cqcode) + x + ':' + str(z / 10) + '%', up_chara, up_star, up_prob)
    up_chara = '\n'.join(up_chara)
    await bot.send(ev, f"本期卡池主打的角色：\n{up_chara}\n3★出率={(gacha.s3_prob)/10:.1f}% 2★出率={(gacha.s2_prob)/10:.1f}%")


POOL_NAME_TIP = '请选择以下卡池\n> 切换卡池jp\n> 切换卡池tw\n> 切换卡池cn\n> 切换卡池mix'
@sv.on_prefix(('切换卡池', '选择卡池'))
async def set_pool(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '只有群管理才能切换卡池哦~', at_sender=True)
    name = util.normalize_str(ev.message.extract_plain_text())
    if not name:
        await bot.finish(ev, POOL_NAME_TIP, at_sender=True)
    elif name in ('b', 'b服', 'bl', 'bilibili', '国', '国服', 'cn'):
        name = 'CN'
    elif name in ('台', '台服', 'tw', 'sonet'):
        name = 'TW'
    elif name in ('日', '日服', 'jp', 'cy', 'cygames'):
        name = 'JP'
    elif name in ('混', '混合', 'mix'):
        name = 'MIX'
    else:
        await bot.finish(ev, f'未知服务器地区 {POOL_NAME_TIP}', at_sender=True)
    gid = str(ev.group_id)
    _group_pool[gid] = name
    dump_pool_config()
    await bot.send(ev, f'卡池已切换为{name}池', at_sender=True)
    await gacha_info(bot, ev)

@sv.on_prefix(('开启仓库', '启用仓库'))
async def enable_colle(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.finish(ev, '测试功能，仅限主人使用哦', at_sender=True)
    uid = str(ev.user_id)
    _colle_enable[uid] = True
    dump_colle_config()
    await bot.send(ev, f'已开启仓库，首次开启需要\"建立仓库\"哦', at_sender=True)

@sv.on_prefix(('关闭仓库', '禁用仓库'))
async def disable_colle(bot, ev: CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.finish(ev, '测试功能，仅限主人使用哦', at_sender=True)
    uid = str(ev.user_id)
    _colle_enable[uid] = False
    dump_colle_config()
    await bot.send(ev, f'已禁用仓库', at_sender=True)


async def modify_colle(bot, ev: CQEvent, gacha_result):
    name = ev.sender['nickname']
    gm = GachaMaster(ev.user_id)
    l = len(gacha_result)

    try:
        db = gm.get_colle()
    except DatabaseError as e:
        await bot.finish(ev, f'DatabaseError: {e.message}\nごめんなさい！嘤嘤嘤(〒︿〒)', at_sender=True)

    if db:
        colle = pickle.loads(db['colle'])
        jewel = db['jewel']
        hiishi = db['hiishi']

        if jewel >= 150 * l:
            jewel -= 150 * l

            for c in gacha_result:
                if c.name in colle:
                    if c.star == 1:
                        hiishi += 1
                    elif c.star == 2:
                        hiishi += 10
                    else:
                        hiishi += 100
                else:
                    colle[c.name] = c.star
            colle = pickle.dumps(colle)
            gm.mod_colle(colle, jewel, hiishi)
        else:
            await bot.finish(ev, JEWEL_EMPTY_NOTICE, at_sender=True)
    else:
        await bot.finish(ev, f'{name}君你还没有仓库，请使用\'建立仓库\'进行初始化')


async def check_jewel_num(bot, ev: CQEvent):
    if not jewel_limit.check(ev.user_id):
        await bot.finish(ev, JEWEL_EXCEED_NOTICE, at_sender=True)


async def check_tenjo_num(bot, ev: CQEvent):
    if not tenjo_limit.check(ev.user_id):
        await bot.finish(ev, TENJO_EXCEED_NOTICE, at_sender=True)


@sv.on_prefix(gacha_1_aliases, only_to_me=True)
async def gacha_1(bot, ev: CQEvent):
    
    await check_jewel_num(bot, ev)
    jewel_limit.increase(ev.user_id, 150)

    gid = str(ev.group_id)
    gacha = Gacha(_group_pool[gid])
    chara = gacha.gacha_one(gacha.up3_prob, gacha.up2_prob, gacha.up1_prob, gacha.s3_prob, gacha.s2_prob)

    uid = str(ev.user_id)
    if _colle_enable[uid]:
        await modify_colle(bot, ev, [chara])
            
    res = f'{chara.icon.cqcode} {chara.name} {"★"*chara.star}'
    
    await bot.send(ev, f'素敵な仲間が増えますよ！\n{res}', at_sender=True)


@sv.on_prefix(gacha_10_aliases, only_to_me=True)
async def gacha_10(bot, ev: CQEvent):

    await check_jewel_num(bot, ev)
    jewel_limit.increase(ev.user_id, 1500)
    
    gid = str(ev.group_id)
    gacha = Gacha(_group_pool[gid])
    result = gacha.gacha_ten()

    uid = str(ev.user_id)
    if _colle_enable[uid]:
        await modify_colle(bot, ev, result)

    res1 = chara.gen_team_pic(result[:5], star_slot_verbose=False)
    res2 = chara.gen_team_pic(result[5:], star_slot_verbose=False)
    res = concat_pic([res1, res2])
    res = pic2b64(res)
    res = MessageSegment.image(res)
    result = [f'{c.name}{"★"*c.star}' for c in result]
    res1 = ' '.join(result[0:5])
    res2 = ' '.join(result[5:])
    res = f'{res}\n{res1}\n{res2}'
    # 纯文字版
    # result = [f'{c.name}{"★"*c.star}' for c in result]
    # res1 = ' '.join(result[0:5])
    # res2 = ' '.join(result[5:])
    # res = f'{res1}\n{res2}'

    await bot.send(ev, f'素敵な仲間が増えますよ！\n{res}', at_sender=True)


@sv.on_prefix(gacha_300_aliases, only_to_me=True)
async def gacha_300(bot, ev: CQEvent):

    await check_tenjo_num(bot, ev)
    tenjo_limit.increase(ev.user_id)

    gid = str(ev.group_id)
    gacha = Gacha(_group_pool[gid])
    if _group_pool[gid]=='JP' or _group_pool[gid]=='MIX':
        result = gacha.gacha_tenjou_jp()
    else:
        result = gacha.gacha_tenjou()
    up = len(result['up'])
    s3 = len(result['s3'])
    s2 = len(result['s2'])
    s1 = len(result['s1'])

    uid = str(ev.user_id)
    if _colle_enable[uid]:
        await modify_colle(bot, ev, result['up'] + result['s3'] + result['s2'] + result['s1'])

    res = [*(result['up']), *(result['s3'])]
    random.shuffle(res)
    lenth = len(res)
    if lenth <= 0:
        res = "竟...竟然没有3★？！"
    else:
        step = 5
        pics = []
        for i in range(0, lenth, step):
            j = min(lenth, i + step)
            pics.append(chara.gen_team_pic(res[i:j], star_slot_verbose=False))
        res = concat_pic(pics)
        res = pic2b64(res)
        res = MessageSegment.image(res)

    msg = [
        f"\n素敵な仲間が増えますよ\n{res}",
        f"★★★×{up+s3} ★★×{s2} ★×{s1}",
        f"获得记忆碎片×{100*up}与女神秘石×{50*(up+s3) + 10*s2 + s1}！\n第{result['first_up_pos']}抽首次获得up角色" if up else f"获得女神秘石{50*(up+s3) + 10*s2 + s1}个！"
    ]
    if _group_pool[gid]=='JP' or _group_pool[gid]=='MIX':
        if up == 0 and s3 == 0:
            msg.append("太惨了，咱们还是退款删游吧...")
        elif up == 0 and s3 > 4:
            msg.append("up呢？我的up呢？")
        elif up == 0 and s3 <= 2:
            msg.append("这位酋长，梦幻包考虑一下？")
        elif up == 0:
            msg.append("据说天井的概率有24.54%")
        elif up <= 2:
            if result['first_up_pos'] < 33:
                msg.append("你的喜悦我收到了，滚去喂鲨鱼吧！")
            elif result['first_up_pos'] < 67:
                msg.append("已经可以了，您已经很欧了")
            elif result['first_up_pos'] > 190:
                msg.append("标 准 结 局")
            elif result['first_up_pos'] > 166:
                msg.append("补井还是不补井，这是一个问题...")
            else:
                msg.append("期望之内，亚洲水平")
        elif up == 3:
            msg.append("抽井母五一气呵成！多出30等专武～")
        elif up >= 4:
            msg.append("记忆碎片一大堆！您是托吧？")
    else:
        if up == 0 and s3 == 0:
            msg.append("太惨了，咱们还是退款删游吧...")
        elif up == 0 and s3 > 7:
            msg.append("up呢？我的up呢？")
        elif up == 0 and s3 <= 32:
            msg.append("这位酋长，梦幻包考虑一下？")
        elif up == 0:
            msg.append("据说天井的概率只有24.54%")
        elif up <= 2:
            if result['first_up_pos'] < 33:
                msg.append("你的喜悦我收到了，滚去喂鲨鱼吧！")
            elif result['first_up_pos'] < 67:
                msg.append("已经可以了，您已经很欧了")
            elif result['first_up_pos'] > 190:
                msg.append("标 准 结 局")
            elif result['first_up_pos'] > 166:
                msg.append("补井还是不补井，这是一个问题...")
            else:
                msg.append("期望之内，亚洲水平")
        elif up == 3:
            msg.append("抽井母五一气呵成！多出30等专武～")
        elif up >= 4:
            msg.append("记忆碎片一大堆！您是托吧？")

    await bot.send(ev, '\n'.join(msg), at_sender=True)


@sv.on_prefix('氪金')
async def kakin(bot, ev: CQEvent):
    if ev.user_id not in bot.config.SUPERUSERS:
        return
    count = 0
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            uid = int(m.data['qq'])
            jewel_limit.reset(uid)
            tenjo_limit.reset(uid)
            count += 1
    if count:
        await bot.send(ev, f"已为{count}位用户充值完毕！谢谢惠顾～")
        
