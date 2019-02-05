#!/usr/local/bin/python3

import os
import sys
from Tasker import Tasker
from GioTasker import GioTasker


def database_task_run():
    # 获取任务文件目录
    task_files_dir = os.path.join(os.path.dirname(__file__), "tasks")

    # 获取任务文件列表
    task_file_names = os.listdir(task_files_dir)

    # 输出所有文件和文件夹
    for task_file_name in task_file_names:
        if task_file_name.index('.') == 0:
            continue
        task_file_path = os.path.join(task_files_dir, task_file_name).replace("\\", "/")
        tasker = Tasker(task_file_path)
        tasker.run()


def gio_task_run():
    # 获取任务文件目录
    task_files_dir = os.path.join(os.path.dirname(__file__), "gios")

    # 获取任务文件列表
    task_file_names = os.listdir(task_files_dir)

    # 输出所有文件和文件夹
    for task_file_name in task_file_names:
        if task_file_name.index('.') == 0:
            continue

        task_file_path = os.path.join(task_files_dir, task_file_name).replace("\\", "/")
        tasker = GioTasker(task_file_path)
        tasker.run()


if len(sys.argv) < 2:
    print('缺少参数！请使用：python TaskRun.py database\n或者使用：python TaskRun.py gio')
    exit(1)

arg_type = sys.argv[1]

if arg_type == 'database':
    database_task_run()
elif arg_type == 'gio':
    gio_task_run()

# gio_task_run()
