from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from forecastUpdater.forecastApi import update_forecast

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_forecast, 'interval', minutes=1)
    scheduler.start()