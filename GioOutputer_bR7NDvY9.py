#!/usr/local/bin/python3

# from GioOutputer import GioOutputer
import Utils


# APP端访问用户趋势监控-IOS
# "meta":[{"name":"时间","dimension":true},
#         {"name":"目标用户","dimension":true},
#         {"name":"用户量","metric":true}]
# datas: [[1546873200000, "全部访问用户", 2708.0]]
def output(title: str, metas: list, datas: list, outputer):
    time_index = 0
    target_user_index = 0
    user_count_index = 0
    for i in range(len(metas)):
        if metas[i]["name"] == "时间":
            time_index = i
        elif metas[i]["name"] == "目标用户":
            target_user_index = i
        elif metas[i]["name"] == "用户量":
            user_count_index = i

    x_axis = []
    y_axis = []
    lines: dict = {}  # {metric: line}
    for data in datas:
        x = Utils.unix_timestamp_MD(int(data[time_index]))
        if x not in x_axis:
            x_axis.append(x)

        legend = data[target_user_index]
        if legend not in lines.keys():
            lines[legend] = []

        line: list = lines[legend]

        y = data[user_count_index]
        line.append(y)

    outputer.create_single_chart(title, x_axis, lines)
