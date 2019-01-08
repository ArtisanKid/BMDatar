#!/usr/local/bin/python3


class Adder:
    inputs = {}  # 数据
    handles = {}  # 加法

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

            # 用于add的数据集
            input_items = self.inputs[input_name]
            for input_item in input_items:
                for key, add_keys in output_rules.items():
                    sum = 0
                    for add_key in add_keys:
                        if add_key not in input_item.keys():
                            raise RuntimeError('未找到字段' + add_key)

                        sum += input_item[add_key]

                    input_item[key] = sum

            self.inputs[output_name] = input_items
