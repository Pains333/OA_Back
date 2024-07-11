# 名字：Pains
# 时间：2024/7/8 15:06
import os
from celery import Celery
from celery.signals import after_setup_logger
import logging

# 设置django的setting模块，celery会读取这个模块中的配置信息
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oaback.settings')

app = Celery('oaback')

# 日志管理
@after_setup_logger.connect
def setup_logging(logger, *args, **kwargs):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')

    # add filehandler
    fh = logging.FileHandler('celery.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

# 配置从settings.py中读取celery配置信息，所有elery配置信息都要以CELERY_开头
# broker_url: CELERY_BROKER_URL
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务，任务可以写在app/task.py中
app.autodiscover_tasks()

# 测试任务
# 1. bind=True，在任务函数中，第一个参数就是任务对象（Task），如果没有设置这个参数，或者是bind=False，那么任务函数中就不会有任务对象参数
# 2. ignore_result=True，就不会保存任务执行的结果
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')