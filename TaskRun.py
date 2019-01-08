#!/usr/local/bin/python3

import os
from Tasker import Tasker

# 获取任务文件目录
task_files_dir = os.path.join(os.path.dirname(__file__), "tasks")
# task_files_dir = "~/Desktop/tasks/"

# 获取任务文件列表
task_file_names = os.listdir(task_files_dir)

# 输出所有文件和文件夹
for task_file_name in task_file_names:
    if task_file_name.index('.') == 0:
        continue
    task_file_path = os.path.join(task_files_dir, task_file_name).replace("\\", "/")
    tasker = Tasker(task_file_path)
    tasker.run()


