#!/usr/local/bin/python3

import time
import Imager
import Exceler


class Outputer:
    inputs = {}  # 数据
    handles = {}  # 连接

    # inputs格式 {变量名: [{}]}
    def __init__(self, inputs={}, handles={}):
        if len(inputs) == 0:
            raise RuntimeError('未找到数据')

        if len(handles.keys()) == 0:
            raise RuntimeError('未找到输出')

        self.inputs = inputs
        self.handles = handles

    def run(self):
        for input_name, configs in self.handles.items():
            if input_name not in self.inputs.keys():
                raise RuntimeError('未找到数据集' + input_name)

            # 一个用于output的数据集
            input_items = self.inputs[input_name]

            # 校验是否空数据集
            if input_items is None or len(input_items) == 0:
                print('空数据集' + input_name)
                continue

            keys = list(input_items[0].keys())
            for output_type, config in configs.items():
                name = config['(输出值)']
                if name.count('(TODAY)'):
                    name = name.replace('(TODAY)', time.strftime('%Y-%m-%d', time.localtime()))

                path = config['(输入值)']
                if path.count('(TODAY)'):
                    path = path.replace('(TODAY)', time.strftime('%Y-%m-%d', time.localtime()))

                if output_type == '(IMAGE)':
                    Imager.data2jpg(input_items, keys, path)
                    self.inputs[name] = path
                elif output_type == '(EXCEL)':
                    Exceler.data2sheet(input_items, keys, 'Test', path)
                    # self.inputs[name] = path
