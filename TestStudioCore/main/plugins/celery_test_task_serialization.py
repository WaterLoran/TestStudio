import pickle
from utils.mysql import Mysql
from .. import app, celery

from utils.mysql import Mysql
import time


class CeleryTestTaskMysql:
    def __init__(self):
        self.mysql = Mysql()

    def create_task(self, celery_test_task_id):
        # create table celery_test_task(
        # 	id INT NOT NULL AUTO_INCREMENT,
        # 	celery_test_task_bytes VARCHAR(1000) NOT NULL,
        # 	PRIMARY KEY (id))
        # 	ENGINE=InnoDB DEFAULT CHARSET=utf8;

        # INSERT INTO celery_test_task ( id, celery_test_task_bytes )  VALUES  ( value1, value2 );
        celery_test_id = int(time.time())
        print("celery_test_id", celery_test_id)
        print("celery_test_task_id", celery_test_task_id)

        # sql_cmd = f'INSERT INTO celery_test_task (id, celery_test_task_bytes) VALUES ({celery_test_id}, "{celery_test_task_id}");'
        celery_test_task_hex = celery_test_task_id.hex()
        print("type(celery_test_task_hex)", type(celery_test_task_hex))
        print("celery_test_task_hex", celery_test_task_hex)
        sql_cmd = "INSERT INTO celery_test_task (id, celery_test_task_bytes) VALUES ({}, x'{}');".format(celery_test_id, celery_test_task_hex)
        print("sql_cmd:", sql_cmd)
        self.mysql.exec_sql_in_database(sql=sql_cmd)
        return celery_test_id

    def delete_task(self, celery_test_id):
        sql_cmd = "DELETE FROM celery_test_task WHERE id = %s" % (celery_test_id)
        print("sql_cmd:", sql_cmd)
        self.mysql.exec_sql_in_database(sql=sql_cmd)
        return celery_test_id

    def get_task(self):
        sql_cmd = "SELECT * FROM celery_test_task"
        print("sql_cmd:", sql_cmd)
        result = self.mysql.exec_sql_in_database(sql=sql_cmd)
        return result

class CeleryTestTask:
    def __init__(self):
        self.celery_mysql = CeleryTestTaskMysql()
        pass

    def serialization_to_mysql(self, celery_test_task):
        app.logger.info("序列化前的数据celery_test_task", celery_test_task)
        app.logger.info("celery_test_task.status", celery_test_task["celery_task_id"].status)
        celery_bytes = pickle.dumps(celery_test_task)

        temp_celery_dict = pickle.loads(celery_bytes)
        app.logger.info("反序列化后的temp_celery_dict", temp_celery_dict)
        app.logger.info("temp_celery_dict.status", temp_celery_dict["celery_task_id"].status)

        celery_test_task_id = self.celery_mysql.create_task(celery_bytes)
        print("celery_test_task_id:", celery_test_task_id)

    def deserialization_from_mysql(self):
        result = self.celery_mysql.get_task()
        celery_test_task_list = []
        for item in result:
            print("item", item)
            celery_test_task_id = item[0]
            celery_test_task_bytes = item[1]
            print("==>READ  celery_test_task_bytes", celery_test_task_bytes)
            celery_test_task_dict = pickle.loads(celery_test_task_bytes)
            t_dict = {"celery_test_task_id": celery_test_task_id,
                      "celery_test_task_dict": celery_test_task_dict}
            celery_test_task_list.append(t_dict)
        print("celery_test_task_list", celery_test_task_list)
        return celery_test_task_list

    def celery_test_task_delete(self, celery_test_id):
        celery_test_id = self.celery_mysql.delete_task(celery_test_id)
        print("celery_test_id", celery_test_id)




