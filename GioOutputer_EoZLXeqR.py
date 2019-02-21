#!/usr/local/bin/python3

# from GioOutputer import GioOutputer


# web端新访问用户转化（来源分布）-gio
#
# "meta":[{"name":"目标用户","dimension":true},
#         {"name":"时间","dimension":true},
#         {"name":"访问来源","dimension":true},
#         {"name":"用户量","metric":true},
#         {"name":"注册成功_人","metric":true},
#         {"name":"交易成功_人","metric":true}]
# "data":[["新访问用户",1550678400000,"直接访问",1491.0,62.0,47.0]]
def output(title: str, metas: list, datas: list, outputer):
    target_user_index = 0
    time_index = 0
    user_count_index = 0
    register_count_index = 0
    trade_count_index = 0

    titles = []
    for i in range(len(metas)):
        name = metas[i]["name"]
        if name == "目标用户":
            target_user_index = i
        elif name == "时间":
            time_index = i
        else:
            if name == "用户量":
                user_count_index = i
            elif name == "注册成功_人":
                register_count_index = i
            elif name == "交易成功_人":
                trade_count_index = i
            titles.append(name)

    rows = []
    for data in datas:
        row = []
        for index in range(len(data)):
            if index == target_user_index or index == time_index:
                continue
            elif index == user_count_index or index == register_count_index or index == trade_count_index:
                row.append(int(data[index]))
            else:
                row.append(data[index])
        rows.append(row)

    outputer.create_table(title, titles, rows[0:10], ["用户量"])
