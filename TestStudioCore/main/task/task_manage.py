# -*- coding: utf-8 -*-
from utils.mysql import Mysql
import datetime
import time


class TaskManage:
    def __init__(self):
        self.mysql = Mysql()
        pass

    def create_task(self, case_id_list, test_task_id=""):
        # create table test_task(
        # 	id INT NOT NULL AUTO_INCREMENT,
        # 	task_id INT NOT NULL,
        # 	create_time DATETIME,
        # 	name VARCHAR(100) NOT NULL,
        # 	case_id_list VARCHAR(5000) NOT NULL,
        # 	schedule INT NOT NULL,
        # 	PRIMARY KEY (id, task_id))
        # 	ENGINE=InnoDB DEFAULT CHARSET=utf8;
        # INSERT INTO table_name ( field1, field2,...fieldN )  VALUES  ( value1, value2,...valueN );

        print("datetime.datetime.now()", datetime.datetime.now())
        print("time.time", )
        cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if test_task_id == "":
            test_task_id = int(time.time())
        task_name = str(test_task_id)
        case_id_str = "==>".join(case_id_list)
        cur_schedule = 1  # 因为刚刚创建任务,所以先暂定将进度确定为1

        sql_cmd = "INSERT INTO test_task " \
                  "(task_id, create_time, name, case_id_list, schedule) " \
                  "VALUES ('%d','%s','%s','%s','%d')" % (test_task_id, cur_time, task_name, case_id_str, cur_schedule)
        # print("sql_cmd:", sql_cmd)
        self.mysql.exec_sql_in_database(sql=sql_cmd)
        return test_task_id

    def delete_task(self):
        pass

    def update_task(self, task_id, latest_schedule):
        sql_cmd = "UPDATE test_task SET schedule='%d' WHERE task_id='%d'" % (latest_schedule, task_id)
        self.mysql.exec_sql_in_database(sql=sql_cmd)
        pass

    def get_tasks(self):
        sql_cmd = "SELECT * FROM test_task"
        sql_res = self.mysql.exec_sql_in_database(sql=sql_cmd)
        print("sql_res", sql_res)
        pass



def create_test_task_interface(case_is_list, test_task_id):
    task = TaskManage()
    task_id = task.create_task(case_is_list, test_task_id)
    return task_id

def get_test_tasks_interface():
    task = TaskManage()
    task.get_tasks()

def update_test_task_interface(test_task_id, latest_schedule):
    task = TaskManage()
    task.update_task(test_task_id, latest_schedule)

if __name__ == '__main__':
    # case_is_list = ["case_01", "case_02", "case_03", "case_04", "case_05"]
    # task = TaskManage()
    # task.create_task(case_is_list)

    task = TaskManage()
    task.get_tasks()

