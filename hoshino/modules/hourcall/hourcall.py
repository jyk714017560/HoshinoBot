import pytz
from datetime import datetime
import hoshino
from hoshino import Service, priv, R

sv = Service('hourcall', enable_on_default=False, visible=False, help_='时报')

@sv.scheduled_job('cron', hour='17', minute='45')
async def remlin():
    return

