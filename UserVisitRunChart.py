#!/usr/local/bin/python3

import Utils
import GrowingIO
import requests
import numpy
from matplotlib import pyplot


# 并排数据源访问量趋势图
def draw(data):
    line_x = []
    user_line_ys = {}  # {source: line}
    visit_line_ys = {}  # {source: line}
    for point in data['data']:

        timestamp = point[1]
        if timestamp not in line_x:
            line_x.append(timestamp)

        source = point[2]

        if source in user_line_ys.keys():
            user_line_y = user_line_ys[source]
        else:
            user_line_y = []
            user_line_ys[source] = user_line_y

        if source in visit_line_ys.keys():
            visit_line_y = visit_line_ys[source]
        else:
            visit_line_y = []
            visit_line_ys[source] = visit_line_y

        user_line_y.append(point[3])
        visit_line_y.append(point[4])

    colors = Utils.colors()
    color_index = 0

    pyplot.figure(figsize=(12, 6))  # 创建绘图对象

    ax1 = pyplot.subplot(1, 2, 1)
    pyplot.sca(ax1)

    box = ax1.get_position()
    ax1.set_position([box.x0, box.height * 0.3, box.width, box.height * 0.7])

    legend_sources = {}

    for source, line_y in user_line_ys.items():
        # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，折点，线宽度，标题）
        line, = pyplot.plot(line_x, line_y, color=colors[color_index], marker='o', linewidth=1.5, label=source)
        color_index += 1

        total = 0
        for count in line_y:
            total += count

        legend_sources[line] = total

    pyplot.xlabel('时间')  # X轴标签
    pyplot.ylabel('数量')  # Y轴标签
    pyplot.title('A 用户量')  # 图标题

    sort_legend_sources = sorted(legend_sources.items(), reverse=True, key=lambda item: item[1])
    valid_legend_sources = []
    for line in sort_legend_sources:
        valid_legend_sources.append(line[0])
    pyplot.legend(handles=valid_legend_sources[0:9], loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)

    color_index = 0

    ax2 = pyplot.subplot(1, 2, 2)
    pyplot.sca(ax2)

    box = ax2.get_position()
    ax2.set_position([box.x0, box.height * 0.3, box.width, box.height * 0.7])

    legend_sources = {}

    for source, line_y in visit_line_ys.items():
        # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
        line, = pyplot.plot(line_x, line_y, color=colors[color_index], marker='o', linewidth=1.5, label=source)
        color_index += 1

        total = 0
        for count in line_y:
            total += count

        legend_sources[line] = total

    pyplot.xlabel('时间')  # X轴标签
    pyplot.ylabel('数量')  # Y轴标签
    pyplot.title('B 访问量')  # 图标题

    sort_legend_sources = sorted(legend_sources.items(), reverse=True, key=lambda item: item[1])
    valid_legend_sources = []
    for line in sort_legend_sources:
        valid_legend_sources.append(line[0])
    pyplot.legend(handles=valid_legend_sources[0:9], loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)

    pyplot.show()  # 显示图


# 不同国家用户用户访问量趋势图
def draw_by_countries():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/GR4N2G2o.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 全部访问量来源趋势图
def draw_by_channels():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/a9BBd5X9.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 付费渠道访问趋势
def draw_by_paid_channels():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/Y9JWOZ6R.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 一级访问来源趋势图
def draw_by_sources():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/L9GJDjBo.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 登录用户访问来源
def draw_by_login_channels():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/qPkA72k9.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 登录用户一级访问来源
def draw_by_login_sources():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/4PYmpX5P.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 搜索引擎访问来源
def draw_by_searches():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/5RpAXKjP.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 外部链接访问来源
def draw_by_links():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/nomAwrAo.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


# 社交媒体访问来源
def draw_by_socials():
    url = 'https://www.growingio.com/v2/projects/1P6j1bVP/charts/3oLV4XzR.json'
    headers = GrowingIO.get_headers()
    params = GrowingIO.get_params()
    response = requests.get(url, headers=headers, params=params)
    print('response is ' + response.text)

    chart = response.json()
    draw(chart)


draw_by_countries()
