# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import *
from .plugins.celery_mgt import make_celery
from logging.handlers import RotatingFileHandler
from .local.database import Database
import logging


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
celery = make_celery(app)
CORS(app, resources=r"/*")  # 允许跨域

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)

db = Database()

# 为了规避循环导入问题,在最后再去导入路由
from main.api.test_case import test_case
from main.api.test_task import test_task
from main.api.upload_case import upload_case
app.register_blueprint(test_task)
app.register_blueprint(test_case)
app.register_blueprint(upload_case)

# 必须添加行代码,这行代码表示将定时任务导入,否则将出现"celery Did you remember to import the module containing this task?"的错误
# 不然不能被celery识别到
from .plugins.cron import *





