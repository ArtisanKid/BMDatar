#!/usr/local/bin/python3


class Unioner:
    inputs = {}  # 数据
    handles = []  # 联合

    def __init__(self, inputs={}, handles=[]):
        if len(inputs) is 0:
            raise RuntimeError('未找到数据')

        if len(handles) is 0:
            raise RuntimeError('未找到联合')

        self.inputs = inputs
        self.handles = handles

    def run(self):
        for handle in self.handles:
            input_names = handle['(输入值)']
            output_name = handle['(输出值)']

            output_items = []
            for input_name in input_names:
                if input_name not in self.inputs.keys():
                    raise RuntimeError('未找到数据集' + input_name)

                # 用于union的数据集
                input_items = self.inputs[input_name]
                output_items += input_items

            self.inputs[output_name] = output_items
