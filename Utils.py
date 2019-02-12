#!/usr/local/bin/python3

import os
import datetime
import time


# 今天。datetime
def today():
    return datetime.date.today()


# 昨天。datetime
def yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday


# 前天。datetime
def day_before_today(days: int):
    today = datetime.date.today()
    target_day = today - datetime.timedelta(days=days)
    return target_day


# 昨天起始。timestamp
def yesterday_begin_timestamp():
    target_next_day = yesterday()
    yesterday_end = time.mktime(target_next_day.timetuple()) * 1000
    return int(yesterday_end)


# 昨天结束。timestamp
def yesterday_end_timestamp():
    target_next_day = datetime.date.today()
    yesterday_end = time.mktime(target_next_day.timetuple()) * 1000 - 1
    return int(yesterday_end)


# 前 m 天开始。timestamp
def day_before_today_begin_timestamp(days: int):
    target_day = day_before_today(days)
    target_day_begin = time.mktime(target_day.timetuple()) * 1000
    return int(target_day_begin)


# 前 m 天结束。timestamp
def day_before_today_end_timestamp(days: int):
    target_next_day = day_before_today(days-1)
    target_day_end = time.mktime(target_next_day.timetuple()) * 1000 - 1
    return int(target_day_end)


def yesterday_YMD():
    return time.strftime('%Y-%m-%d', yesterday().timetuple())


def today_YMD():
    return time.strftime('%Y-%m-%d', today().timetuple())


# Unix时间戳转换 月-日
def unix_timestamp_MD(unix_timestamp: int):
    return time.strftime('%m-%d', time.localtime(unix_timestamp / 1000.))


# Unix时间戳转换 时-分
def unix_timestamp_HS(unix_timestamp: int):
    return time.strftime('%H-%m', time.localtime(unix_timestamp / 1000.))


def outputs_name(name: str):
    output_name = name + yesterday_YMD() + '.png'
    return output_name


def outputs_path(name: str):
    outputs_dir = os.path.join(os.path.dirname(__file__), "outputs")
    if os.path.exists(outputs_dir) is False:
        os.makedirs(outputs_dir)

    output_name = outputs_name(name)
    path = os.path.join(outputs_dir, output_name)
    return path


def gio_path(dashboard, name: str):
    outputs_dir = os.path.join(os.path.dirname(__file__), "gios")
    outputs_dir = os.path.join(outputs_dir, "dashboard")
    if os.path.exists(outputs_dir) is False:
        os.makedirs(outputs_dir)

    output_name = outputs_name(name)
    path = os.path.join(outputs_dir, output_name)
    return path


def colors():
    cnames = [
        "#e91e63",
        "#9c27b0",
        "#3f51b5",
        "#2196f3",
        "#009688",
        "#8bc34a",
        "#cddc39",
        "#ffeb3b",
        "#ffc107",
        "#ff5722",
        "#9e9e9e",
        "#607d8b",
        "#795548",
        "black",
        "#ff0097"]
    return cnames
