import time
from .. import app, celery
from ..task.case_actuator import execute_case_interface


@celery.task
def api_execute_case_interface(case_id_list, test_task_id):
    try:
        print("已经正在执行api_execute_case_interface")
        execute_case_interface(case_id_list, test_task_id)
    except Exception as err:
        pass
        app.logger.warning(u"执行测试任务失败" % err)
    else:
        pass


@celery.task
def chk_execute_case_status():
    import os
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>os.getpid()", os.getpid())
