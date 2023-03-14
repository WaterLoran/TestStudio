# -*- coding: utf-8 -*-
from utils.mysql import Mysql


class GetAllCase:
    def __init__(self):
        self.mysql = Mysql()
        self.sql_data = None


    def get_sql_data_to_item(self):
        sql_cmd = "select * from test_task order by task_id desc;"
        sql_data = self.mysql.exec_sql_in_database(sql=sql_cmd)
        # print("sql_data", sql_data)
        self.sql_data = sql_data

    def get_task_data(self):
        sql_data = self.sql_data
        test_task = []
        for item in sql_data:
            t_dict = {}
            t_dict["name"] = item[3]
            t_dict["taskid"] = item[1]
            t_dict["createtime"] = str(item[2])
            t_dict["caseidlist"] = item[4].replace("==>", ",")
            t_dict["schedule"] = item[5]
            # print("t_dict", t_dict)
            test_task.append(t_dict)
        # print("test_task", test_task)
        return test_task

def get_all_tasks_interface():
    get_case = GetAllCase()
    get_case.get_sql_data_to_item()
    return get_case.get_task_data()
    pass

if __name__ == "__main__":
    get_case = GetAllCase()
    get_case.get_sql_data_to_item()
    get_case.get_task_data()

    #
    # print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    # print(item)


