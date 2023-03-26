from app.views import UpdateAvailability
import time
import os
while True:
    current_time = time.strftime("%H:%M:%S");
    print(current_time);
    if current_time == "10:20:00":
        print("Update");
        UpdateAvailability();
        time.sleep(1);
