# -*- coding: utf-8 -*-
import logging
import pymysql #导入模块


class Mysql(object):
    def __init__(self):
        self.db = None
        pass

    def get_server_ip_port(self):
        mysql_ip = "192.168.0.106"
        mysql_port = 3306
        return mysql_ip, mysql_port

    def get_mysql_password(self):
        # mysql_password = os.environ.get('MYSQL_PASSWORD')
        mysql_password = "Admin@123"
        return mysql_password

    def mysqladmin_flush_hosts(self):
        pass

    def connect_to_mysql(self):
        mysql_ip, mysql_port = self.get_server_ip_port()
        mysql_password = self.get_mysql_password()
        print(mysql_ip, mysql_port)
        print(mysql_password)
        db = pymysql.connect(
            host=mysql_ip,
            port=mysql_port,
            user='root',
            passwd=mysql_password,
            db='test_studio',
            charset='utf8'
        )
        self.db = db

    def exec_sql(self, sql=""):
        if sql == "":
            assert False

        if self.db is None:
            self.connect_to_mysql()
        db = self.db

        cursor = db.cursor()
        result = None
        try:
            cursor.execute(sql)  # 执行sql语句
            result = cursor.fetchall()  # 返回数据库查询的所有信息，用元组显示
            db.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
        except Exception as err:
            db.rollback()  # 发生错误时回滚
            logging.error("exec_sql_cmd:exec cmd failed, err:{}".format(err))
        cursor.close()  # 关闭游标
        return result

    def change_database(self, target_databases="test_studio"):
        sql = "use {};".format(target_databases)
        logging.info("change_databases::sql ==> {}".format(sql))
        self.exec_sql(sql=sql)

    def exec_sql_in_database(self, database="test_studio", sql=""):
        self.change_database(target_databases=database)
        res = self.exec_sql(sql=sql)
        return res