from apscheduler.schedulers.background import BackgroundScheduler
from .emails import cp_remainder


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cp_remainder, 'cron', hour=22, minute=30)
    scheduler.start()