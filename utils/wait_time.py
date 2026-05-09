from datetime import datetime, timedelta
import time 

def sleep_until_next_15min():
    now = datetime.now()
    next_15min = (now + timedelta(minutes=15 - now.minute % 15)).replace(second=0, microsecond=0)
    sleep_time = (next_15min - now).total_seconds() + 5
    time.sleep(sleep_time)


def sleep_until_next_30min():
    now = datetime.now()
    next_30min = (now + timedelta(minutes=30 - now.minute % 30)).replace(second=0, microsecond=0)
    sleep_time = (next_30min - now).total_seconds() + 5  # +5 sec buffer
    time.sleep(sleep_time)


def minutes_for_hour_check():
    now = datetime.now()
    next_15min = (now + timedelta(minutes=15 - now.minute % 15)).replace(second=0, microsecond=0)
    return next_15min

def is_15min_wait_completed(order_time):
    if(order_time):
        elapsed = datetime.now() - order_time
        remaining_sleep = (15 * 60) - elapsed.total_seconds()

        if remaining_sleep > 0:
            return False
        else:
            return True
        
    else:
        return False

def is_30min_wait_completed(order_time):
    if order_time:
        elapsed = datetime.now() - order_time
        remaining_sleep = (30 * 60) - elapsed.total_seconds()

        return remaining_sleep <= 0
    else:
        return False
# 