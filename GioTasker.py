#!/usr/local/bin/python3

import os
import yaml
from GioOutputer import GioOutputer
from Emailer import Emailer


class GioTasker:
    task_file_path: str = None
    task = None

    projects: dict = {}  # 项目字典
    dashboards = {}  # 看板字典
    mailbox = {}  # 邮箱
    handles = []  # 处理数组

    def __init__(self, path: str):
        if os.path.exists(path) is False:
            print(path)
            raise RuntimeError('未找到任务文件')

        self.task_file_path = path
        file = open(self.task_file_path, encoding='UTF-8')
        self.task = yaml.load(file)

        if '(项目)' not in self.task.keys():
            raise RuntimeError('未找到(项目)')

        if '(看板)' not in self.task.keys():
            raise RuntimeError('未找到(看板)')

        if '(邮箱)' not in self.task.keys():
            raise RuntimeError('未找到(邮箱)')

        if '(处理)' not in self.task.keys():
            raise RuntimeError('未找到(处理)')

        self.projects = self.task['(项目)']
        self.dashboards = self.task['(看板)']
        self.mailbox = self.task['(邮箱)']
        self.handles = self.task['(处理)']

    def run(self):
        outputs = {}
        for handle in self.handles:
            if '(类型)' not in handle.keys():
                raise RuntimeError('not find (类型)')

            handle_type: str = handle['(类型)']

            if handle_type == '(输出)':
                outputer = GioOutputer(self.projects, self.dashboards, handle, outputs)
                outputer.run()
            elif handle_type == '(邮件)':
                emailer = Emailer(self.mailbox, handle, outputs)
                emailer.run()
