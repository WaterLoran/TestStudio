from .. import celery, app
from ..task.task_manage import update_test_task_interface
from ..plugins.celery_test_task_serialization import CeleryTestTask
import time
import os


@celery.task(name='express.update_celery_task_schedule')
def update_test_task_schedule():
    """测试定时任务,将用于自动更新所有celery异步任务,即刷新用例执行任务的进度"""
    print("测试定时任务,将用于自动更新所有celery异步任务,即刷新用例执行任务的进度")



    print("更新完celery_test_task的执行进度之后,做了删除和修改,最新的数据如下")
    pass

