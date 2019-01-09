#!/usr/local/bin/python3

import os
import time
import Imager
import Exceler
import utils


class Outputer:
    inputs = {}  # 数据
    outputs = {}  # 连接

    # inputs格式 {变量名: [{}]}
    def __init__(self, inputs, handles):
        if inputs is None or len(inputs) is 0:
            raise RuntimeError('未找到上下文数据')

        if handles is None or len(handles) is 0:
            raise RuntimeError('未找到加法配置')

        self.inputs = inputs
        self.outputs = handles

    def run(self):
        for input_name, configs in self.outputs.items():
            self.operate(input_name, configs)

    def operate(self, input_name, configs):
        # (输出):
        #   交易数据:
        #     (IMAGE):
        #       #(输入值): '/Users/LiXiangYu/Desktop/交易数据-(TODAY).jpg'
        #       (输出值): '交易数据-(TODAY).jpg'
        #     (EXCEL):
        #       #(输入值): '/Users/LiXiangYu/Desktop/交易数据-(TODAY).xls'
        #       (输出值): '交易数据-(TODAY).xls'

        # 一个用于output的数据集
        input_items = self.inputs[input_name]

        # 校验是否空数据集
        if len(input_items) == 0:
            print('空数据集' + input_name)
            return

        keys = list(input_items[0].keys())
        for output_type, config in configs.items():
            output_name = config['(输出值)']
            if len(output_name) == 0:
                raise RuntimeError('输出值长度0')

            if output_name.count('(TODAY)'):
                output_name = output_name.replace('(TODAY)', time.strftime('%Y-%m-%d', time.localtime()))

            if output_name.count('(YESTERDAY)'):
                output_name = output_name.replace('(YESTERDAY)', time.strftime('%Y-%m-%d', utils.yesterday()))

            # 如果有path，那么用path作为输出路径，否则自定义路径
            if '(输入值)' in config.keys():
                path = config['(输入值)']

                if path.count('(TODAY)'):
                    path = path.replace('(TODAY)', time.strftime('%Y-%m-%d', time.localtime()))

                if path.count('(YESTERDAY)'):
                    path = path.replace('(YESTERDAY)', time.strftime('%Y-%m-%d', utils.yesterday()))
            else:
                outputs_dir = os.path.join(os.path.dirname(__file__), "outputs")
                if os.path.exists(outputs_dir) is False:
                    os.makedirs(outputs_dir)

                path = os.path.join(outputs_dir, output_name)

            # 如果已经存在输出，则删除输出
            if os.path.exists(path):
                os.remove(path)

            if output_type == '(IMAGE)':
                Imager.data2jpg(input_items, keys, path)
                self.inputs[output_name] = path
            elif output_type == '(EXCEL)':
                Exceler.data2sheet(input_items, keys, 'sheet1', path)
                # self.inputs[output_name] = path
