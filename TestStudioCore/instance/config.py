# -*- coding: utf-8 -*-
from celery.schedules import crontab
from datetime import timedelta


CELERY_BROKER_URL = 'redis://localhost:6379/1',
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
# 被导入后的使用效果
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'

CELERYBEAT_SCHEDULE = {
    'every-3S-update_celery_task_schedule': {
        'task': 'express.update_celery_task_schedule',
        'schedule': timedelta(seconds=10)
        # TODO 暂时调整该时长,用于调试,上线后需要修改为3秒
    },
    # 'every-15-min-at-8-to-22': {
    #     'task': 'express.update',
    #     'schedule': crontab(minute='*/15', hour='8-22')
    # },
    # 'every-1-hour': {
    #     'task': 'access_token.update',
    #     'schedule': crontab(minute=0, hour='*/1')
    # },
    # 'every-9-am': {
    #     'task': 'library.return_books',
    #     'schedule': crontab(minute=0, hour='9')
    # }
}


celery_task_bind_test = []

