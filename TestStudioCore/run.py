#!/usr/bin/env python
# -*- coding: utf-8 -*-
from main import app
import os
from threading import Thread
import time
from main import db
from main.task.task_manage import update_test_task_interface

def chk_case_task_schedule_thread():
    global db
    while True:
        time.sleep(2)
        finished_celery_task_list = []
        for item in db.celery_test_task_list:
            test_task_id = item["test_task_id"]
            celery_task_id = item["celery_task_id"]
            status = celery_task_id.status
            if status == "SUCCESS":
                finished_celery_task_list.append(item)
                update_test_task_interface(test_task_id, 100)
        #已经执行完成的任务,则在将对应的测试任务删除之后,需要将这个临时信息给删除
        if finished_celery_task_list != []:
            for item in finished_celery_task_list:
                db.celery_test_task_list.remove(item)


if __name__ == "__main__":
    t = Thread(target=chk_case_task_schedule_thread)
    t.start()
    app.debug = app.config['DEBUG']
    app.run(host='0.0.0.0', port=5000)


# 注意在Linux端启动的时候,对应的配置文件,需要放在下面的这个位置
# /usr/var/main-instance/config.py

# 启动celery的worker的命令如下
# celery -A main.celery worker -l info -P eventlet

# 启动celery定时任务的命令如下
# celery -A main.celery beat

# 拷贝Core代码到Linux后台
# cd C:\Program Files\PuTTY&&pscp -pw feng1996 -r E:\development_space\TestStudioCore root@192.168.0.106:/usr/local

# 拷贝Front代码到Linux后台
# cd C:\Program Files\PuTTY&&pscp -pw feng1996 -r E:\development_space\TestStudioFront root@192.168.0.106:/usr/local

# 拷贝AutoTEST代码到Linux后台
# cd C:\Program Files\PuTTY&&pscp -pw feng1996 -r E:\development_space\AutoTEST root@192.168.0.106:/usr/local

