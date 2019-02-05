#!/usr/local/bin/python3

import os
import yaml
from Selecter import Selecter
from Joiner import Joiner
from Unioner import Unioner
from Adder import Adder
from Minuser import Minuser
from Grouper import Grouper
from Outputer import Outputer
from Emailer import Emailer


class Tasker:
    task_file_path = ''
    task = None

    databases = {}  # 数据库字典
    email = {}  # 邮箱
    models = {}  # 模型字典
    handles = []  # 处理数组

    def __init__(self, path):
        if os.path.exists(path) is False:
            print(path)
            raise RuntimeError('未找到任务文件')

        self.task_file_path = path
        file = open(self.task_file_path, encoding='UTF-8')
        self.task = yaml.load(file)

        self.databases = self.task['(数据库)']
        self.email = self.task['(邮箱)']
        self.handles = self.task['(处理)']

    def run(self):
        if len(self.handles) is 0:
            raise RuntimeError('未找到任务处理')

        for handle in self.handles:
            # print(handle)
            if len(handle) is 0:
                raise RuntimeError('未找到操作片段')

            results = {}
            for segment in handle:
                key = list(segment.keys())[0]
                value = list(segment.values())[0]
                if key == '(SELECT)':
                    selecter = Selecter(self.databases, results, value)
                    selecter.run()
                    print(results)
                elif key == '(JOIN)':
                    joiner = Joiner(results, value)
                    joiner.run()
                    print(results)
                elif key == '(UNION)':
                    unioner = Unioner(results, value)
                    unioner.run()
                    print(results)
                elif key == '(ADD)':
                    adder = Adder(results, value)
                    minuser.run()
                    print(results)
                elif key == '(MINUS)':
                    minuser = Minuser(results, value)
                    minuser.run()
                    print(results)
                elif key == '(GROUP)':
                    grouper = Grouper(results, value)
                    grouper.run()
                    print(results)
                elif key == '(输出)':
                    outputer = Outputer(results, value)
                    outputer.run()
                    print(results)
                elif key == '(邮件)':
                    emailer = Emailer(self.email, value, results)
                    emailer.run()
