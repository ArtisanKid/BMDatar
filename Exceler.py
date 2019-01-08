#!/usr/local/bin/python3

import os
import xlwt
import xlrd
from xlutils.copy import copy


def data2sheet(datas=[], titles=[], sheet_name='', path=''):
    # 判断是否有指定文件
    if os.path.exists(path):
        read_xls = xlrd.open_workbook(path)
        write_xls = copy(read_xls)
    else:
        write_xls = xlwt.Workbook()

    sheet = write_xls.add_sheet(sheet_name)
    for j in range(len(titles)):
        sheet.write(0, j, titles[j])

    for i in range(len(datas)):
        data = datas[i]
        for j in range(len(titles)):
            title = titles[j]
            sheet.write(i + 1, j, data[title])

    write_xls.save(path)
