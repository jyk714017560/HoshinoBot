from hoshino import Service, priv ,util

sv_help = '''
- [申请头衔XX] XX为头衔名
- [删除头衔] 
'''.strip()

sv = Service(
    name = 'Title',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助群管"])
async def bangzhu(bot, ev):
    await bot.send(ev, sv_help)
  
  
@sv.on_prefix('申请头衔')
async def set_title(bot, ev):
	uid = ev.user_id
	gid = ev.group_id
	title = ev.message.extract_plain_text()
	await bot.set_group_special_title(group_id=gid, user_id=uid, special_title=title)


@sv.on_fullmatch(('删除头衔','清除头衔','收回头衔','回收头衔','取消头衔'))
async def del_title(bot, ev):
    uid = ev.user_id
    gid = ev.group_id
    title =  None
    await bot.set_group_special_title(group_id=gid, user_id=uid, special_title=title)


@sv.on_prefix(('设置管理员','设置管理','右迁','升职'))
async def set_admin(bot, ev):
    if not priv.check_priv(ev,priv.ADMIN):
        return
    uid = ev.user_id
    sid = None
    gid = ev.group_id
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
        elif m.type == 'at' and m.data['qq'] == 'all':
            return
    if sid is None:
        return
    await bot.set_group_admin(group_id= gid, user_id= sid, enable= True)
    
        
@sv.on_prefix(('取消管理员','取消管理','左迁','降职'))
async def unset_admin(bot, ev):
    if not priv.check_priv(ev,priv.ADMIN):
        return
    uid = ev.user_id
    sid = None
    gid = ev.group_id
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
        elif m.type == 'at' and m.data['qq'] == 'all':
            return
    if sid is None:
        return
    await bot.set_group_admin(group_id= gid, user_id= sid, enable= False)