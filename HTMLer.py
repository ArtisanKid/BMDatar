import pandas


# rows是[row]类型，row是{title:value}类型
# titles是[title]类型
# 需要进行数据转换
def table(rows=[{}], titles=[]):
    columns = {}
    for title in titles:
        column_datas = []
        for i in range(len(rows)):
            row = rows[i]
            column_datas.append(row[title])
        columns[title] = column_datas

    data_frame = pandas.DataFrame(columns)
    data_frame = data_frame[titles]
    html = data_frame.to_html(index=False)
    page = "<head><meta charset='UTF-8'></head><body>%s</body>" % html
    return page
