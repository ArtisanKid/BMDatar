#!/usr/local/bin/python3

import time
import Utils
import GrowingIO
import requests
import numpy
from matplotlib import pyplot


def draw(data):
    # "meta": [{"name": "目标用户", "dimension": true}
    #          {"name": "时间", "dimension": true},
    #          {"name": "页面浏览量", "metric": true}]

    line_x = []
    line_ys = []  # [line]
    line_titles = []

    for meta in data['meta']:
        if 'metric' in meta.keys():
            line_titles.append(meta['name'])
            line_ys.append([])

    for point in data['data']:
        # ["全部访问用户", 1546873200000, 55186.0, 5974.0, 2708.0]
        timestamp = point[1]
        if timestamp not in line_x:
            line_x.append(timestamp)

        for index in range(len(point)):
            if index == 0 or index == 1:
                pass
            else:
                line_y = line_ys[index - 2]
                line_y.append(point[index])

    colors = Utils.colors()

    pyplot.figure(figsize=(12, 6))  # 创建绘图对象

    ax1 = pyplot.subplot(1, 1, 1)
    pyplot.sca(ax1)

    for index in range(len(line_ys)):
        # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，折点，线宽度，标题）
        pyplot.plot(line_x, line_ys[index], color=colors[index], marker='o', linewidth=1.5, label=line_titles[index])

    pyplot.xlabel('时间')  # X轴标签
    pyplot.ylabel('数量')  # Y轴标签
    pyplot.title(data['name'])  # 图标题

    x_labels = []
    x_locs, labels = pyplot.xticks()
    for x_loc in x_locs:
        x_labels.append(time.strftime('%m-%d', time.localtime(x_loc / 1000.)))
    pyplot.xticks(ticks=x_locs, labels=x_labels)

    box = ax1.get_position()
    ax1.set_position([box.x0, box.height * 0.3, box.width, box.height * 0.7])
    pyplot.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)

    pyplot.show()  # 显示图
    pyplot.savefig()


# 页面浏览量趋势图
def draw_by_dimensions():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/noqL2nAP.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    # draw(chart)


# 登录用户页面浏览量
def draw_by_login_dimensions():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/nRbXvYlo.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    # draw(chart)


draw_by_dimensions()
