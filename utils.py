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
    cnames = {
        'antiquewhite': '#FAEBD7',
        'aqua': '#00FFFF',
        'aquamarine': '#7FFFD4',
        'azure': '#F0FFFF',
        'beige': '#F5F5DC',
        'bisque': '#FFE4C4',
        'black': '#000000',
        'blanchedalmond': '#FFEBCD',
        'blue': '#0000FF',
        'blueviolet': '#8A2BE2',
        'brown': '#A52A2A',
        'burlywood': '#DEB887',
        'cadetblue': '#5F9EA0',
        'chartreuse': '#7FFF00',
        'chocolate': '#D2691E',
        'coral': '#FF7F50',
        'cornflowerblue': '#6495ED',
        'cornsilk': '#FFF8DC',
        'crimson': '#DC143C',
        'cyan': '#00FFFF',
        'darkblue': '#00008B',
        'darkcyan': '#008B8B',
        'darkgoldenrod': '#B8860B',
        'darkgray': '#A9A9A9',
        'darkgreen': '#006400',
        'darkkhaki': '#BDB76B',
        'darkmagenta': '#8B008B',
        'darkolivegreen': '#556B2F',
        'darkorange': '#FF8C00',
        'darkorchid': '#9932CC',
        'darkred': '#8B0000',
        'darksalmon': '#E9967A',
        'darkseagreen': '#8FBC8F',
        'darkslateblue': '#483D8B',
        'darkslategray': '#2F4F4F',
        'darkturquoise': '#00CED1',
        'darkviolet': '#9400D3',
        'deeppink': '#FF1493',
        'deepskyblue': '#00BFFF',
        'dimgray': '#696969',
        'dodgerblue': '#1E90FF',
        'firebrick': '#B22222',
        'floralwhite': '#FFFAF0',
        'forestgreen': '#228B22',
        'fuchsia': '#FF00FF',
        'gainsboro': '#DCDCDC',
        'ghostwhite': '#F8F8FF',
        'gold': '#FFD700',
        'goldenrod': '#DAA520',
        'gray': '#808080',
        'green': '#008000',
        'greenyellow': '#ADFF2F',
        'honeydew': '#F0FFF0',
        'hotpink': '#FF69B4',
        'indianred': '#CD5C5C',
        'indigo': '#4B0082',
        'ivory': '#FFFFF0',
        'khaki': '#F0E68C',
        'lavender': '#E6E6FA',
        'lavenderblush': '#FFF0F5',
        'lawngreen': '#7CFC00',
        'lemonchiffon': '#FFFACD',
        'lightblue': '#ADD8E6',
        'lightcoral': '#F08080',
        'lightcyan': '#E0FFFF',
        'lightgoldenrodyellow': '#FAFAD2',
        'lightgreen': '#90EE90',
        'lightgray': '#D3D3D3',
        'lightpink': '#FFB6C1',
        'lightsalmon': '#FFA07A',
        'lightseagreen': '#20B2AA',
        'lightskyblue': '#87CEFA',
        'lightslategray': '#778899',
        'lightsteelblue': '#B0C4DE',
        'lightyellow': '#FFFFE0',
        'lime': '#00FF00',
        'limegreen': '#32CD32',
        'linen': '#FAF0E6',
        'magenta': '#FF00FF',
        'maroon': '#800000',
        'mediumaquamarine': '#66CDAA',
        'mediumblue': '#0000CD',
        'mediumorchid': '#BA55D3',
        'mediumpurple': '#9370DB',
        'mediumseagreen': '#3CB371',
        'mediumslateblue': '#7B68EE',
        'mediumspringgreen': '#00FA9A',
        'mediumturquoise': '#48D1CC',
        'mediumvioletred': '#C71585',
        'midnightblue': '#191970',
        'mintcream': '#F5FFFA',
        'mistyrose': '#FFE4E1',
        'moccasin': '#FFE4B5',
        'navajowhite': '#FFDEAD',
        'navy': '#000080',
        'oldlace': '#FDF5E6',
        'olive': '#808000',
        'olivedrab': '#6B8E23',
        'orange': '#FFA500',
        'orangered': '#FF4500',
        'orchid': '#DA70D6',
        'palegoldenrod': '#EEE8AA',
        'palegreen': '#98FB98',
        'paleturquoise': '#AFEEEE',
        'palevioletred': '#DB7093',
        'papayawhip': '#FFEFD5',
        'peachpuff': '#FFDAB9',
        'peru': '#CD853F',
        'pink': '#FFC0CB',
        'plum': '#DDA0DD',
        'powderblue': '#B0E0E6',
        'purple': '#800080',
        'red': '#FF0000',
        'rosybrown': '#BC8F8F',
        'royalblue': '#4169E1',
        'saddlebrown': '#8B4513',
        'salmon': '#FA8072',
        'sandybrown': '#FAA460',
        'seagreen': '#2E8B57',
        'seashell': '#FFF5EE',
        'sienna': '#A0522D',
        'silver': '#C0C0C0',
        'skyblue': '#87CEEB',
        'slateblue': '#6A5ACD',
        'slategray': '#708090',
        'snow': '#FFFAFA',
        'springgreen': '#00FF7F',
        'steelblue': '#4682B4',
        'tan': '#D2B48C',
        'teal': '#008080',
        'thistle': '#D8BFD8',
        'tomato': '#FF6347',
        'turquoise': '#40E0D0',
        'violet': '#EE82EE',
        'wheat': '#F5DEB3',
        'white': '#FFFFFF',
        'whitesmoke': '#F5F5F5',
        'yellow': '#FFFF00',
        'yellowgreen': '#9ACD32'}
    return list(cnames.keys())
