#!/usr/local/bin/python3

import time
import pymysql


class Selecter:
    databases = {}  # 数据库字典
    handles = {}  # 筛选

    # inputs格式 {变量名: [{}]}
    def __init__(self, databases={}, handles={}):
        if len(databases) == 0:
            raise RuntimeError('未找到数据库')

        if len(handles) == 0:
            raise RuntimeError('未找到筛选')

        self.databases = databases
        self.handles = handles

    def run(self):
        outputs = {}
        for database_name, handles in self.handles.items():
            if database_name not in self.databases.keys():
                raise RuntimeError('未找到筛选')

            database_config = self.databases[database_name]
            database_server = database_config['(服务器)']
            if database_server is None or len(database_server) is 0:
                raise RuntimeError('未找到服务器')

            database_port = database_config['(端口号)']
            if isinstance(database_port, str):
                if database_port is None or len(database_port) is 0:
                    raise RuntimeError('未找到端口号')
                database_port = int(database_port)

            database_user = database_config['(用户名)']
            if database_user is None or len(database_user) is 0:
                raise RuntimeError('未找到用户名')

            database_password = database_config['(密码)']
            if isinstance(database_password, str):
                if database_password is None or len(database_password) is 0:
                    raise RuntimeError('未找到密码')
            else:
                if database_password <= 0:
                    raise RuntimeError('未找到密码')
                database_password = '%d' % database_password

            connection = pymysql.connect(host=database_server,
                                         user=database_user,
                                         password=database_password,
                                         database=database_name,
                                         port=database_port)

            for handle in handles:
                sql = handle['(输入值)']

                if sql.count('(TODAY)'):
                    sql = sql.replace('(TODAY)', time.strftime('%Y-%m-%d', time.localtime()))

                print(sql + '\n\n')

                output_name = handle['(输出值)']
                output_fields = handle['(字段)']

                cursor = connection.cursor()
                cursor.execute(sql)
                results = cursor.fetchall()

                dics = []
                for result in results:
                    dic = {}
                    for index in range(len(output_fields)):
                        dic[output_fields[index]] = result[index]
                    dics.append(dic)

                outputs[output_name] = dics

                cursor.close()

        return outputs
