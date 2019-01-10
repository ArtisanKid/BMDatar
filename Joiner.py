#!/usr/local/bin/python3


class Joiner:
    inputs = {}  # 数据
    joins = []  # 连接

    # inputs格式 {变量名: [{}]}
    def __init__(self, inputs, handles):
        if inputs is None or len(inputs) == 0:
            raise RuntimeError('未找到上下文数据')

        if handles is None or len(handles) == 0:
            raise RuntimeError('未找到加法配置')

        self.inputs = inputs
        self.joins = handles

    def run(self):
        for join in self.joins:
            self.operate(join)

    def operate(self, join):
        input_names = join['(输入值)']
        if len(input_names) == 0:
            raise RuntimeError('输入值长度0')

        join_on = join['(ON)']
        if len(join_on) == 0:
            raise RuntimeError('On长度0')

        # (LEFT)/(RIGHT)/(FULL)/(INNER)
        join_type = join['(类型)']
        if len(join_type) == 0:
            raise RuntimeError('类型长度0')

        output_name = join['(输出值)']
        if len(output_name) == 0:
            raise RuntimeError('输出值长度0')

        output_rules = join['(规则)']
        if len(output_rules) == 0:
            raise RuntimeError('规则长度0')

        is_first_input = True  # 支持左连接、右连接、全连接、内连接

        # output_items结构{join_on : {}}
        output_items = {}
        for input_name in input_names:
            # 用于join的数据集
            input_items = self.inputs[input_name]

            # 校验是否空数据集
            if len(input_items) == 0:
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
                            output_item = {}
                            self.fill_output_item(input_name, output_rules, input_item, output_item)
                        else:
                            output_item = output_items[join_on_value]
                            self.fill_output_item(input_name, output_rules, input_item, output_item)
                        bridge_output_items[join_on_value] = output_item
                    elif join_type == '(FULL)':  # 全连接
                        if join_on_value not in output_items.keys():  # 左侧无数据
                            output_item = {}
                            self.fill_output_item(input_name, output_rules, input_item, output_item)
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

    def left_join(self):
        pass

    def right_join(self):
        pass

    def full_join(self):
        pass

    def inner_join(self):
        pass

    # input_name: 输入数据集名称
    # output_rules: 输出规则
    # input_item: 输入项
    # output_item: 输出项
    #
    # 此方法用于将input_item的字段按照output_rules设置到output_item中
    def fill_output_item(self, input_name, output_rules, input_item, output_item):
        # output_rules
        # (规则):
        #   输出字段名:
        #     (字段): 输入数据集.字段
        #     (默认值): Asset

        if input_name is None or len(input_name) == 0:
            raise RuntimeError('未找到数据集')

        if input_name is None or len(input_name) == 0:
            raise RuntimeError('未找到数据集')

        if output_rules is None or len(output_rules) == 0:
            raise RuntimeError('未找到规则')

        if input_item is None:
            raise RuntimeError('未找到输入项')

        if output_item is None:
            raise RuntimeError('未找到输出项')

        # 如果没有输出规则，说明需要所有字段
        for output_item_key, config in output_rules.items():
            rule_input_name = None
            rule_item_key = None

            path = config['(字段)']
            if path.count('.') != 0:
                components = path.split('.')
                rule_input_name = components[0]
                rule_item_key = components[1]
            else:
                rule_item_key = path

            # 如果rule_input_name是None，表示所有数据集的字段都可以填充
            # rule_input_name是当前数据集，表示可以填充
            if rule_input_name is None or rule_input_name == input_name:
                output_item[output_item_key] = input_item[rule_item_key]
            else:
                if output_item_key not in output_item.keys():
                    output_item[output_item_key] = config['(默认值)']
