# -*- coding: utf-8 -*-
from flask import Blueprint, request
from flask_restx import Api, Resource
from case.get_all_case import GetAllCase

test_case = Blueprint('test_case', __name__)
test_case_api = Api(test_case)

@test_case_api.route('/test_case')
class TestTask(Resource):

    # 接收get请求
    @staticmethod
    def get():
        print("接收到获取所有用例的请求,正在处理")
        get_case = GetAllCase()
        get_case.get_sql_data_to_item()
        item = get_case.case_tree.get_res_of_tree_interface(get_case.id_to_case_id_list)
        return item


    # 接收post请求
    @staticmethod
    def post():
        json_data = request.json
        print(json_data)
        return json_data + "POST"

    # 接收put请求
    @staticmethod
    def put():
        print('case_api put')
        return 'case_api 接口已经被请求 put'