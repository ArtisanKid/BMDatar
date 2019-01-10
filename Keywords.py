import Utils


# 替换日期关键字
def active_date(str):
    if str.count('(TODAY)'):
        str = str.replace('(TODAY)', Utils.today_YMD())

    if str.count('(YESTERDAY)'):
        str = str.replace('(YESTERDAY)', Utils.yesterday_YMD())

    return str
