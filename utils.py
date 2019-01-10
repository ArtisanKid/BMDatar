import datetime
import time


def yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday

def yesterday_YMD():
    return time.strftime('%Y-%m-%d', yesterday().timetuple())

def today():
    return datetime.date.today()

def today_YMD():
    return time.strftime('%Y-%m-%d', today().timetuple())
