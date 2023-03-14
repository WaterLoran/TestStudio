# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request
from flask_restx import Api, Resource
from case.batch_update_case import batch_update_case_interface


upload_case = Blueprint('upload_case', __name__)
upload_case_api = Api(upload_case)


@upload_case_api.route('/upload_case')
class UploadCase(Resource):

    # 接收post请求
    @staticmethod
    def post():
        data = request.files
        file = data['file']
        print("file.filename", file.filename)
        print("request.headers", request.headers)
        # 文件写入磁盘

        basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
        # upload_path = os.path.join(basePath, 'upload')
        # upload_path = os.path.abspath(upload_path)
        upload_path = os.path.join(basePath, file.filename)
        print("upload_file_path", upload_path)
        file.save(upload_path)
        # 这里调用批量更新数据进去数据库的接口函数写入数据库, 注意函数待interface
        batch_update_case_interface(upload_path)

        return "文件已经被接收并且,更新进数据库\n"

