# -*- coding: utf-8 -*-
import json
import time
from flask import Blueprint, request
from flask_restx import Api, Resource
from main.task.get_all_task import get_all_tasks_interface
from ..plugins.test_task_interface import api_execute_case_interface
from .. import db
from .. import app


test_task = Blueprint('test_task', __name__)
test_task_api = Api(test_task)


@test_task_api.route('/test_task')
class TestTask(Resource):

    # 接收get请求
    @staticmethod
    def get():
        app.logger.info(u"接收到获取测试任务的get请求")
        test_task_data = get_all_tasks_interface()
        return test_task_data

    # 接收post请求
    @staticmethod
    def post():
        app.logger.info(u"接收到test_task的post请求-执行测试任务-正在进行")
        print(u"接收到test_task的post请求-执行测试任务-正在进行")
        data = request.get_data()
        json_data = json.loads(data)
        case_id_list = json_data['case_id_list']

        test_task_id = int(time.time())
        celery_task_id = api_execute_case_interface.delay(case_id_list, test_task_id)

        celery_bind_test_dict = {}
        celery_bind_test_dict["test_task_id"] = test_task_id
        celery_bind_test_dict["celery_task_id"] = celery_task_id

        global db
        db.celery_test_task_list.append(celery_bind_test_dict)
        return "已经接收要执行的测试用例,并且执行完成,请稍后查看测试任务"

    # 接收put请求
    @staticmethod
    def put():
        print('test_task_api put')
        return 'test_task_api put'


