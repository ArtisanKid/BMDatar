#!/usr/local/bin/python3


class Minuser:
    inputs = {}  # 数据
    handles = {}  # 减法

    # inputs格式 {变量名: [{}]}
    def __init__(self, inputs={}, handles={}):
        if len(inputs) == 0:
            raise RuntimeError('未找到数据')

        if len(handles) == 0:
            raise RuntimeError('未找到减法')

        self.inputs = inputs
        self.handles = handles

    def run(self):
        for handle in self.handles:
            input_name = handle['(输入值)']
            output_name = handle['(输出值)']

            output_rules = handle['(规则)']

            if input_name not in self.inputs.keys():
                raise RuntimeError('未找到数据集' + input_name)

            # 用于minus的数据集
            input_items = self.inputs[input_name]
            for input_item in input_items:
                for key, config in output_rules.items():
                    minus_key = config['(减数)']
                    minused_key = config['(被减数)']

                    if minus_key not in input_item.keys():
                        raise RuntimeError('未找到字段' + minus_key)

                    if minused_key not in input_item.keys():
                        raise RuntimeError('未找到字段' + minused_key)

                    input_item[key] = input_item[minus_key] - input_item[minused_key]

            self.inputs[output_name] = input_items
