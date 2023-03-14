# 启动celery命令
 启动定时任务
 celery -A main.celery beat
 启动worker
 celery -A main.celery worker -l info -P eventlet
 
