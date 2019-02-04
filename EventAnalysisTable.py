#!/usr/local/bin/python3

import Utils
import GrowingIO
import requests
import pandas
import numpy
from matplotlib import pyplot
import imgkit
import pdfkit


def draw(data):
    # "meta": [{"name": "目标用户", "dimension": true},
    #          {"name": "广告来源", "dimension": true},
    #          {"name": "广告名称", "dimension": true},
    #          {"name": "广告内容", "dimension": true},
    #          {"name": "广告媒介", "dimension": true},
    #          {"name": "用户量", "metric": true},
    #          {"name": "访问量", "metric": true}]

    titles = []
    rows = []
    metrics = []

    for meta in data['meta']:
        if meta['name'] == "目标用户":
            continue
        else:
            titles.append(meta['name'])
            if 'metric' in meta.keys():
                metrics.append(meta['name'])

    for row in data['data']:
        # ["全部访问用户","不适用","不适用","不适用","不适用",8817.0,30012.0]
        _row = row[1:]
        rows.append(_row)

    columns = {}
    for index in range(len(titles)):
        column = []
        for row in rows:
            column.append(row[index])
        columns[titles[index]] = column

    data_frame = pandas.DataFrame(data=columns, columns=titles)
    data_frame = data_frame[titles]
    data_frame.sort_values(by=metrics)

    name = data['name']
    path = Utils.outputs_path(name)

    # ax = data_frame.plot()
    # fig = ax.get_figure()
    # fig.savefig(path)

    # html = data_frame.to_html()
    # page = "<head><meta charset='UTF-8'></head><body>%s</body>" % html
    # print(page)
    #
    # pdfkit.from_string(page, path)

    fig = pyplot.figure(figsize=(len(columns), len(rows) * 0.2))  # 创建绘图对象
    ax = fig.add_subplot(1, 1, 1)
    ax.axis('off')
    table = ax.table(cellText=data_frame.values,
                     cellLoc='center',  # colWidths=[2] * data_frame.values.shape[1],
                     # rowLabels=data_frame.index,
                     colLabels=data_frame.columns, colLoc='center',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1)
    # pyplot.show()
    fig.savefig(path, dpi=400)


# 广告监测
def draw_by_ad_channel():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/qPkLDXwo.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 全部访问用户跳出率
def draw_by_leave():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/j9yAxnm9.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 登录访问用户跳出率
def draw_by_login_leave():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/1R3rw169.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# draw_by_ad_channel()
draw_by_leave()
# draw_by_login_leave()
