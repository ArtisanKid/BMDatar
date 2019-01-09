#!/usr/local/bin/python3


class Adder:
    inputs = {}  # 数据
    adds = {}  # 加法

    # inputs格式 {变量名: [{}]}
    def __init__(self, inputs, handles):
        if inputs is None or len(inputs) is 0:
            raise RuntimeError('未找到上下文数据')

        if handles is None or len(handles) is 0:
            raise RuntimeError('未找到加法配置')

        self.inputs = inputs
        self.adds = handles

    def run(self):
        for add in self.adds:
            self.operate(add)

    def operate(self, handle):
        # (ADD):
        #   - (输入值): 目标充值提现数据
        #     (输出值): 目标充值提现数据
        #     (规则):
        #       总量:
        #         - 充值量
        #         - 提现量

        input_name = handle['(输入值)']
        if len(input_name) == 0:
            raise RuntimeError('输入值长度0')

        output_name = handle['(输出值)']
        if len(output_name) == 0:
            raise RuntimeError('输出值长度0')

        output_rules = handle['(规则)']
        if len(output_rules) == 0:
            raise RuntimeError('聚合字段长度0')

        # 用于add的数据集
        input_items = self.inputs[input_name]

        output_items = []
        for input_item in input_items:
            output_item = input_item.copy()
            for sum_key, add_keys in output_rules.items():
                sum_value = 0
                for add_key in add_keys:
                    add_value = input_item[add_key]
                    sum_value += add_value
                output_item[sum_key] = sum_value

        self.inputs[output_name] = output_items
