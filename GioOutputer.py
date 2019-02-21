#!/usr/local/bin/python3

import time
import numpy
import pandas
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

import Utils
import GrowingIO
import Imager

import GioOutputer_nRbX0Lzo
import GioOutputer_EoZLXeqR
import GioOutputer_lPQqm4vP
import GioOutputer_39lYy4dR


class GioOutputer:
    project: str = None  # 项目
    dashboard: str = None  # 看板
    chart_configs: dict = None  # 图表配置

    outputs = {}  #输出内容

    def __init__(self, projects: dict, dashboards: dict, handle: dict, outputs: dict):
        if projects is None:
            raise RuntimeError('projects is None')

        if dashboards is None:
            raise RuntimeError('dashboards is None')

        if handle is None:
            raise RuntimeError('handle is None')

        if '(项目)' not in handle.keys():
            raise RuntimeError('not found (项目)')

        if '(看板)' not in handle.keys():
            raise RuntimeError('not found (看板)')

        if outputs is None:
            raise RuntimeError('outputs is None')

        self.project = projects[handle['(项目)']]
        self.dashboard = dashboards[handle['(看板)']]
        self.chart_configs = handle['(配置)']
        self.outputs = outputs

    # lines: {metric: line}
    def create_single_chart(self, title: str, x_axis: list, lines: dict):
        fig: Figure = pyplot.figure(figsize=(12, 6))  # 创建绘图对象
        ax: Axes = fig.add_subplot(1, 1, 1)

        colors = Utils.colors()
        color_index = 0
        for legend, line in lines.items():
            # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，折点，线宽度，标题）
            ax.plot(x_axis, line, color=colors[color_index], marker='o', linewidth=1.5, label=legend)
            color_index += 1

        ax.set_title(title)  # 图标题
        ax.set_xlabel('时间')  # X轴标签
        ax.set_ylabel('数量')  # Y轴标签

        # # x轴时间格式转化
        # x_labels = []
        # x_locs = ax.get_xticks()
        # for x_loc in x_locs:
        #     x_labels.append(time.strftime('%m-%d', time.localtime(x_loc / 1000.)))
        # ax.set_xticklabels(labels=x_labels)

        box = ax.get_position()
        ax.set_position([box.x0, box.height * 0.4, box.width, box.height * 0.7])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)

        # pyplot.show()  # 显示图

        path = Utils.outputs_path(title)
        fig.savefig(path, dpi=200)

        self.outputs[Utils.outputs_name(title)] = path

    def create_table(self, title: str, column_titles: list, rows: list, metrics: list):
        array = numpy.array(rows)
        data_frame = pandas.DataFrame(data=array, columns=column_titles)
        data_frame = data_frame[column_titles]
        data_frame.sort_values(by=metrics)

        path = Utils.outputs_path(title)
        Imager.data_frame_to_jpg(title, data_frame, path)

        self.outputs[Utils.outputs_name(title)] = path

    # "meta":[{"name":"目标用户","dimension":true},
    #         {"name":"时间","dimension":true},
    #         {"name":"页面浏览量","metric":true},
    #         {"name":"访问量","metric":true},
    #         {"name":"用户量","metric":true}]
    # datas: [["全部访问用户", 1546873200000, 55186.0, 5974.0, 2708.0]]
    def single_chart(self, title: str, datas: list, dimensions: list, metrics: list):
        x_axis = []
        y_axis = []
        lines: dict = {}  # {metric: line}

        # dimensions中第一个是 '目标用户'
        dimension_count = len(dimensions)

        for data in datas:
            x = Utils.unix_timestamp_MD(int(data[1]))
            if x not in x_axis:
                x_axis.append(x)

            for index in range(len(metrics)):
                y = data[dimension_count + index]

                legend = metrics[index]
                if legend not in lines.keys():
                    lines[legend] = []

                line: list = lines[legend]
                line.append(y)

        self.create_single_chart(title, x_axis, lines)

    # "meta":[{"name": "目标用户", "dimension": true},
    #         {"name": "时间", "dimension": true},
    #         {"name": "国家名称", "dimension": true},
    #         {"name": "用户量", "metric": true},
    #         {"name": "访问量", "metric": true}]
    # "data": [["全部访问用户", 1546876800000, "中国", 1547, 3529]]
    def double_chart(self, title: str, datas: list, dimensions: list, metrics: list):
        x_axis = []
        y_axis = []

        left_lines: dict = {}  # {legend: line}
        right_lines: dict = {}  # {legend: line}

        # dimensions中第一个是 '目标用户'
        dimension_count = len(dimensions)

        left_title = metrics[0]
        right_title = metrics[-1]

        for data in datas:
            x = Utils.unix_timestamp_MD(int(data[1]))
            if x not in x_axis:
                x_axis.append(x)

            # 标注
            legend = data[dimension_count - 1]

            left_y = data[dimension_count]
            if legend not in left_lines.keys():
                left_lines[legend] = []
            left_line: list = left_lines[legend]
            left_line.append(left_y)

            right_y = data[-1]
            if legend not in right_lines.keys():
                right_lines[legend] = []
            right_line: list = right_lines[legend]
            right_line.append(right_y)

        colors = Utils.colors()

        fig: Figure = pyplot.figure(figsize=(12, 6))  # 创建绘图对象

        left_ax: Axes = fig.add_subplot(1, 2, 1)
        pyplot.sca(left_ax)

        left_ax.set_title(left_title)  # 图标题
        left_ax.set_xlabel('时间')  # X轴标签
        left_ax.set_ylabel('数量')  # Y轴标签

        left_legend_counts = {}  # {legend, count}
        for legend, line in left_lines.items():
            total = 0
            for count in line:
                total += count
            left_legend_counts[legend] = total

        # 按照总量排序
        left_sort_legend_counts = sorted(left_legend_counts.items(), reverse=True, key=lambda item: item[1])

        left_total_legend_length = 0

        left_color_index = 0
        for legend, count in left_sort_legend_counts[0:9]:
            left_total_legend_length += len(legend)

            # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，折点，线宽度，标题）
            left_ax.plot(x_axis,
                         left_lines[legend],
                         color=colors[left_color_index],
                         marker='o',
                         linewidth=1.5,
                         label=legend)
            left_color_index += 1

        average_length = left_total_legend_length / 9

        left_box = left_ax.get_position()
        if average_length <= 10:
            left_ax.set_position([left_box.x0, left_box.height * 0.3, left_box.width, left_box.height * 0.7])
            left_ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)
        else:
            left_ax.set_position([left_box.x0, left_box.height * 0.4, left_box.width, left_box.height * 0.6])
            left_ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)

        right_ax: Axes = fig.add_subplot(1, 2, 2)
        pyplot.sca(right_ax)

        right_ax.set_title(right_title)  # 图标题
        right_ax.set_xlabel('时间')  # X轴标签
        right_ax.set_ylabel('数量')  # Y轴标签

        right_legend_counts = {}
        for legend, line in right_lines.items():
            total = 0
            for count in line:
                total += count
            right_legend_counts[legend] = total

        # 按照总量排序
        right_sort_legend_counts = sorted(right_legend_counts.items(), reverse=True, key=lambda item: item[1])

        right_total_legend_length = 0

        right_color_index = 0
        for legend, count in right_sort_legend_counts[0:9]:
            right_total_legend_length += len(legend)

            # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，折点，线宽度，标题）
            right_ax.plot(x_axis, right_lines[legend], color=colors[right_color_index], marker='o', linewidth=1.5, label=legend)
            right_color_index += 1

        right_average_length = right_total_legend_length / 9

        right_box = right_ax.get_position()
        if right_average_length < 5:
            right_ax.set_position([right_box.x0, right_box.height * 0.3, right_box.width, right_box.height * 0.7])
            right_ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)
        else:
            right_ax.set_position([right_box.x0, right_box.height * 0.4, right_box.width, right_box.height * 0.6])
            right_ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)

        # pyplot.show()  # 显示图

        path = Utils.outputs_path(title)
        fig.savefig(path, dpi=200)

        self.outputs[Utils.outputs_name(title)] = path

    # "meta":[{"name":"目标用户","dimension":true},
    #         {"name":"时间","dimension":true},
    #         {"name":"访问来源","dimension":true},
    #         {"name":"访问量","metric":true},
    #         {"name":"用户量","metric":true},
    #         {"name":"跳出率","metric":true}]
    # [["全部访问用户", "不适用", "不适用", "不适用", "不适用", 8817.0, 30012.0]]
    def table(self, title: str, datas: list, dimensions: list, metrics: list):
        # dimensions中第一个是 '目标用户'

        # 判断目标用户有几种
        user_types = []
        for data in datas:
            if data[0] not in user_types:
                user_types.append(data[0])
        count = len(user_types) * 10

        # 查找时间字段的Index
        for i in range(len(dimensions)):
            dimension = dimensions[i]
            if dimension == "时间":
                time_dimension_index = i

        titles = dimensions + metrics
        rows = []

        for data in datas[0:count]:
            row = data
            for index in range(len(data)):
                if index == time_dimension_index:
                    row[index] = Utils.unix_timestamp_MD(row[index])
                elif index >= len(dimensions):
                    if row[index] == int(row[index]):
                        row[index] = int(row[index])
                    else:
                        row[index] = round(float(row[index]), 2)

            rows.append(row)

        self.create_table(title, titles, rows, metrics)
        #
        # columns = {}
        # for index in range(len(titles)):
        #     column = []
        #     for row in rows:
        #         column.append(row[index])
        #     columns[titles[index]] = column
        #
        # data_frame = pandas.DataFrame(data=columns, columns=titles)
        # data_frame = data_frame[titles]
        # data_frame.sort_values(by=metrics)
        #
        # path = Utils.outputs_path(title)
        # Imager.data_frame_to_jpg(title, data_frame, path)
        #
        # self.outputs[Utils.outputs_name(title)] = path

    def create_chart(self, chart: dict):
        if 'id' not in chart.keys():
            raise RuntimeError('not found id')

        if 'name' not in chart.keys():
            raise RuntimeError('not found name')

        chart_id = chart['id']
        chart_name = chart['name']

        # if chart_name != '广告监测':
        #     return

        if chart_name not in self.chart_configs.keys():
            return

        days = 7
        interval = 86400000

        config: dict = self.chart_configs[chart_name]
        if config is not None:
            if '(天)' in config.keys():
                days = config['(天)']
                if days == 1:
                    interval = 3600000

            if '(单位)' in config.keys():
                if config['(单位)'] == '(天)':
                    interval = 86400000
                elif config['(单位)'] == '(小时)':
                    interval = 3600000

        response = GrowingIO.get_chart(self.project, chart_id, days, interval)

        # 这里判断是图表还是表格

        if 'meta' not in response.keys():
            raise RuntimeError('not found meta')

        if 'data' not in response.keys():
            raise RuntimeError('not found data')

        metas: dict = response['meta']
        datas: list = response['data']

        if chart_id == 'nRbX0Lzo':
            GioOutputer_nRbX0Lzo.output(chart_name, metas, datas, self)
        elif chart_id == 'EoZLXeqR':
            GioOutputer_EoZLXeqR.output(chart_name, metas, datas, self)
        elif chart_id == 'lPQqm4vP':
            GioOutputer_lPQqm4vP.output(chart_name, metas, datas, self)
        elif chart_id == '39lYy4dR':
            GioOutputer_39lYy4dR.output(chart_name, metas, datas, self)
        else:
            dimensions = []
            metrics = []
            for meta in metas:
                if 'name' not in meta.keys():
                    raise RuntimeError('not found meta')

                name = meta['name']
                if 'dimension' in meta.keys():
                    dimensions.append(name)
                elif 'metric' in meta.keys():
                    metrics.append(name)
                else:
                    raise RuntimeError('not found dimension or metric')

            # 如果维度=(目标用户+其他)，则为单趋势图
            # 如果维度=(目标用户+其他+其他)且有两个变量，则为双趋势图，两个变量分两个图表
            # 如果维度=(目标用户+其他+其他...)，则为表格

            if len(dimensions) < 2:
                raise RuntimeError('dimensions count error')

            if len(metrics) < 1:
                raise RuntimeError('metrics count error')

            if len(dimensions) == 2:
                if dimensions[0] == '目标用户':
                    # pass
                    self.single_chart(chart_name, datas, dimensions, metrics)
                else:
                    pass
                    # raise RuntimeError('dimensions error')
            elif len(dimensions) == 3 and len(metrics) == 2:
                if dimensions[0] == '目标用户':
                    # pass
                    self.double_chart(chart_name, datas, dimensions, metrics)
                else:
                    self.table(chart_name, datas, dimensions, metrics)
            else:
                self.table(chart_name, datas, dimensions, metrics)

    def run(self):
        response = GrowingIO.get_dashboard(self.project, self.dashboard)

        if response is None:
            raise RuntimeError('response is None')

        if 'charts' not in response.keys():
            raise RuntimeError('not find charts')

        charts = response['charts']
        for chart in charts:
            self.create_chart(chart)
            time.sleep(2)
