
import time
from datetime import datetime
from views import UpdateAvailability
import schedule

# while True:
#     current_time = time.strftime("%H:%M:%S");
#     print(current_time);
#     if current_time == "10:20:00":
#         print("Update");
#         UpdateAvailability();
#         time.sleep(1);
from celery import shared_task
@shared_task
def run_daily_function():
    schedule.every().day.at("10:00").do(UpdateAvailability)
    while True:
        schedule.run_pending()
        time.sleep(1)