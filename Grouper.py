#!/usr/local/bin/python3


class Grouper:
    inputs = {}  # 数据
    groups = {}  #

    # inputs格式 {变量名: [{}]}
    def __init__(self, inputs, handles):
        if inputs is None or len(inputs) == 0:
            raise RuntimeError('未找到上下文数据')

        if handles is None or len(handles) == 0:
            raise RuntimeError('未找到求和配置')

        self.inputs = inputs
        self.groups = handles

    def run(self):
        for group in self.groups:
            self.operate(group)

    def operate(self, handle):
        # (GROUP):
        #   - (输入值): 交易数据
        #     (输出值): 交易数据
        #     (规则):
        #       - symbol

        input_name = handle['(输入值)']
        if len(input_name) == 0:
            raise RuntimeError('输入值长度0')

        output_name = handle['(输出值)']
        if len(output_name) == 0:
            raise RuntimeError('输出值长度0')

        output_group_keys = handle['(规则)']
        if len(output_group_keys) == 0:
            raise RuntimeError('聚合字段长度0')

        # 用于group的数据集
        input_items = self.inputs[input_name]

        # bridge_output_items用于支持各种类型的sum处理
        # {join(group_values[]): output_item}
        bridge_output_items = {}

        for input_item in input_items:
            group_values = []

            for group_key in output_group_keys:
                group_value = input_item[group_key]
                group_values.append(group_value)

            group_values_join = '-'.join(group_values)

            if group_values_join in bridge_output_items.keys():
                output_item = bridge_output_items[group_values_join]
                for sum_key, sum_value in output_item.items():
                    # 聚合条件不做sum
                    if sum_key in output_group_keys:
                        continue

                    input_item_value = input_item[sum_key]
                    output_item[sum_key] = sum_value + input_item_value
            else:
                bridge_output_items[group_values_join] = input_item.copy()

        self.inputs[output_name] = list(bridge_output_items.values())
