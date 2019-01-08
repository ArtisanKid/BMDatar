#!/usr/local/bin/python3


class Joiner:
    inputs = {}  # 数据
    handles = []  # 连接

    # inputs格式 {变量名: [{}]}

    def __init__(self, inputs={}, handles=[]):
        if len(inputs) == 0:
            raise RuntimeError('未找到数据')

        if len(handles) == 0:
            raise RuntimeError('未找到连接')

        self.inputs = inputs
        self.handles = handles

    def run(self):
        for handle in self.handles:
            input_names = handle['(输入值)']

            join_on = handle['(ON)']
            join_type = handle['(类型)']  # (LEFT)/(RIGHT)/(FULL)/(INNER)

            output_name = handle['(输出值)']
            output_rules = handle['(规则)']

            is_first_input = True  # 支持左连接、右连接、全连接、内连接

            # output_items结构{join_on : {}}
            output_items = {}
            for input_name in input_names:
                if input_name not in self.inputs.keys():
                    raise RuntimeError('未找到数据集' + input_name)

                # 用于join的数据集
                input_items = self.inputs[input_name]

                # 校验是否空数据集
                if input_items is None or len(input_items) == 0:
                    print('空数据集' + input_name)

                    if join_type == '(INNER)':  # 如果是内连接
                        self.inputs[output_name] = []
                        return

                    if is_first_input:  # 如果是首组数据
                        if join_type == '(LEFT)':  # 如果是左连接
                            self.inputs[output_name] = []
                            return
                        elif join_type == '(RIGHT)':  # 如果是右连接
                            continue
                        else:  # 如果是全连接
                            continue
                    else:  # 如果不是首组数据
                        if join_type == '(RIGHT)':  # 如果是右连接
                            self.inputs[output_name] = []
                            return
                        elif join_type == '(LEFT)':  # 如果是左连接
                            continue
                        else:  # 如果是全连接
                            continue

                # 校验数据集合法性，是否包含join_on，是否排重，是否满足映射
                tmp_input_item_join_on_values = []
                for input_item in input_items:
                    if join_on not in input_item.keys():
                        raise RuntimeError('未找到on' + join_on)

                    on_value = input_item[join_on]
                    if on_value in tmp_input_item_join_on_values:
                        raise RuntimeError('表数据未排重' + on_value)

                    tmp_input_item_join_on_values.append(on_value)

                    # 这里需要检验input_item字段映射

                # bridge_output_items用于支持各种类型的join处理
                bridge_output_items = {}
                if join_type == '(LEFT)':  # 左连接
                    bridge_output_items = output_items
                elif join_type == '(FULL)':  # 全连接
                    bridge_output_items = output_items

                for input_item in input_items:
                    join_on_value = input_item[join_on]

                    if is_first_input:  # 如果是首组数据
                        output_item = {}
                        self.fill_output_item(input_name, output_rules, input_item, output_item)
                        bridge_output_items[join_on_value] = output_item
                    else:
                        if join_type == '(LEFT)':  # 左连接
                            if join_on_value not in output_items.keys():  # 右侧数据无效
                                continue

                            output_item = output_items[join_on_value]
                            self.fill_output_item(input_name, output_rules, input_item, output_item)
                            bridge_output_items[join_on_value] = output_item
                        elif join_type == '(RIGHT)':  # 右连接
                            if join_on_value not in output_items.keys():  # 左侧无数据
                                output_item = self.fill_output_item(input_name, output_rules, input_item)
                            else:
                                output_item = output_items[join_on_value]
                                self.fill_output_item(input_name, output_rules, input_item, output_item)
                            bridge_output_items[join_on_value] = output_item
                        elif join_type == '(FULL)':  # 全连接
                            if join_on_value not in output_items.keys():  # 左侧无数据
                                output_item = self.fill_output_item(input_name, output_rules, input_item)
                            else:
                                output_item = output_items[join_on_value]
                                self.fill_output_item(input_name, output_rules, input_item, output_item)
                            bridge_output_items[join_on_value] = output_item
                        else:  # 内连接
                            if join_on_value not in output_items.keys():  # 右侧数据无效
                                continue

                            output_item = output_items[join_on_value]
                            self.fill_output_item(input_name, output_rules, input_item, output_item)
                            bridge_output_items[join_on_value] = output_item

                is_first_input = False
                output_items = bridge_output_items

            values = list(output_items.values())
            self.inputs[output_name] = values

    def fill_output_item(self, input_name, output_rules, input_item, output_item):
        if output_rules is None or len(output_rules) == 0:
            for key, value in input_item.items():
                if key in output_item.keys():
                    raise RuntimeError('重复字段' + key)

                output_item[key] = value  # 直接将input_item作为output_item
            return output_item

        for output_item_key, config in output_rules.items():
            input_name_item_key = config['(字段)']
            tmps = input_name_item_key.split('.')
            rule_input_name = tmps[0]
            rule_item_key = tmps[1]

            if rule_input_name == input_name:  # 非此数据集映射规则
                output_item[output_item_key] = input_item[rule_item_key]
            else:
                if output_item_key not in output_item.keys():
                    output_item[output_item_key] = config['(默认值)']
