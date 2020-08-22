from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

TOP_MANUAL = '''
新增功能：
[点歌+关键字] 关键字点歌
[猜语音] 维护中,暂不开放
=====================
- 七七群Bot使用说明 -
=====================
发送方括号[]内的关键词即可触发
※功能采取模块化管理，群管理可控制开关

[#来发十连] 转蛋模拟
[会战面板] http://140.143.169.143/yobot/user/ 
[会战帮助] http://140.143.169.143/yobot/help/ 
[会战手册] http://140.143.169.143/yobot/manual/ 
[lssv] 查看功能模块的开关状态（群管理限定）

发送以下关键词查看更多：
[帮助pcr查询]
[帮助pcr娱乐]
[帮助pcr订阅]
[帮助通用]
========
※除这里中写明外 另有其他隐藏功能:)
'''.strip()

def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for sv in service_list:
        if sv.visible:
            spit_line = '=' * max(0, 18 - len(sv.name))
            manual.append(f"|{'○' if sv.check_enabled(gid) else '×'}| {sv.name} {spit_line}")
            if sv.help:
                manual.append(sv.help)
    return '\n'.join(manual)


@sv.on_prefix(('help', '帮助', '幫助'))
async def send_help(bot, ev: CQEvent):
    bundle_name = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    if not bundle_name:
        await bot.send(ev, TOP_MANUAL)
    elif bundle_name in bundles:
        msg = gen_bundle_manual(bundle_name, bundles[bundle_name], ev.group_id)
        await bot.send(ev, msg)
    # else: ignore
