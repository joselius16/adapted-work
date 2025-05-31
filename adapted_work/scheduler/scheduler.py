import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from adapted_work.router.comunities.andalucia.save_andalucia.extract import \
    save_andalucia
from adapted_work.router.comunities.aragon.save_aragon.extract import \
    save_aragon
from adapted_work.router.comunities.extremadura.save_extremadura.extract import \
    save_extremadura
from adapted_work.router.comunities.murcia.save_murcia.extract import \
    save_murcia
from adapted_work.settings import settings


def save_data():
    save_andalucia(settings.base_url_andalucia, settings.start_id, settings.end_id)
    save_aragon(settings.base_url_andalucia, settings.start_id, settings.end_id)
    save_extremadura(settings.base_url_andalucia, settings.start_id, settings.end_id)
    save_murcia(settings.base_url_andalucia, settings.start_id, settings.end_id)


scheduler = BackgroundScheduler()
# The function is going to be executed every day at 10:00
scheduler.add_job(save_data, CronTrigger(hour=10, minute=0))

# Init scheduler
scheduler.start()

# Keep alive the process
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
