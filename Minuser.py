#!/usr/local/bin/python3


class Minuser:
    inputs = {}  # 数据
    minuses = {}  # 减法

    # inputs格式 {变量名: [{}]}
    def __init__(self, inputs, handles):
        if inputs is None or len(inputs) is 0:
            raise RuntimeError('未找到上下文数据')

        if handles is None or len(handles) is 0:
            raise RuntimeError('未找到加法配置')

        self.inputs = inputs
        self.minuses = handles

    def run(self):
        for minus in self.minuses:
            self.operate(minus)

    def operate(self, handle):
        # (MINUS):
        #   - (输入值): 目标充值提现数据
        #     (输出值): 目标充值提现数据
        #     (规则):
        #       净值:
        #         (减数): 充值量
        #         (被减数): 提现量

        input_name = handle['(输入值)']
        if len(input_name) == 0:
            raise RuntimeError('输入值长度0')

        output_name = handle['(输出值)']
        if len(output_name) == 0:
            raise RuntimeError('输出值长度0')

        output_rules = handle['(规则)']
        if len(output_rules) == 0:
            raise RuntimeError('聚合字段长度0')

        # 用于minus的数据集
        input_items = self.inputs[input_name]

        output_items = []
        for input_item in input_items:
            output_item = input_item.copy()
            for key, config in output_rules.items():
                minus_key = config['(减数)']
                if len(minus_key) == 0:
                    raise RuntimeError('减数长度0')

                minused_key = config['(被减数)']
                if len(minus_key) == 0:
                    raise RuntimeError('被减数长度0')

                output_item[key] = input_item[minus_key] - input_item[minused_key]

        self.inputs[output_name] = output_items
