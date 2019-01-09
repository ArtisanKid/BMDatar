#!/usr/local/bin/python3

import time
import pymysql
import utils


class Selecter:
    databases = {}  # 数据库字典
    inputs = {}  # 数据
    selects = {}  # 筛选

    # inputs格式 {变量名: [{}]}
    def __init__(self, databases, inputs, handles):
        if inputs is None or len(databases) == 0:
            raise RuntimeError('未找到数据库配置')

        if inputs is None:
            raise RuntimeError('未找到上下文数据')

        if handles is None or len(handles) is 0:
            raise RuntimeError('未找到加法配置')

        self.databases = databases
        self.inputs = inputs
        self.selects = handles

    def run(self):
        for database_name, selects in self.selects.items():
            database_config = self.databases[database_name]

            database_server = database_config['(服务器)']
            if len(database_server) == 0:
                raise RuntimeError('未找到服务器')

            database_port = database_config['(端口号)']
            if isinstance(database_port, str):
                if len(database_port) == 0:
                    raise RuntimeError('未找到端口号')
                database_port = int(database_port)
            else:
                if database_port <= 0:
                    raise RuntimeError('未找到端口号')

            database_user = database_config['(用户名)']
            if len(database_user) == 0:
                raise RuntimeError('未找到用户名')

            database_password = database_config['(密码)']
            if isinstance(database_password, str):
                if len(database_password) == 0:
                    raise RuntimeError('未找到密码')
            else:
                if database_password <= 0:
                    raise RuntimeError('未找到密码')
                database_password = str(database_password)

            connection = pymysql.connect(host=database_server,
                                         user=database_user,
                                         password=database_password,
                                         database=database_name,
                                         port=database_port)

            for select in selects:
                self.operate(connection, select)

    def operate(self, connection, select):
        sql = select['(输入值)']
        if len(sql) == 0:
            raise RuntimeError('输入值长度0')

        if sql.count('(TODAY)'):
            sql = sql.replace('(TODAY)', time.strftime('%Y-%m-%d', time.localtime()))

        if sql.count('(YESTERDAY)'):
            sql = sql.replace('(YESTERDAY)', time.strftime('%Y-%m-%d', utils.yesterday()))

        print(sql + '\n\n')

        output_name = select['(输出值)']
        if len(output_name) == 0:
            raise RuntimeError('输出值长度0')

        output_fields = select['(字段)']
        if len(output_fields) == 0:
            raise RuntimeError('输出字段长度0')

        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        dics = []
        for result in results:
            dic = {}
            for index in range(len(output_fields)):
                dic[output_fields[index]] = result[index]
            dics.append(dic)
        self.inputs[output_name] = dics

        cursor.close()
