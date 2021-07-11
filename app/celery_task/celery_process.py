# !/usr/bin/env python
# coding:utf-8
# @Time    : 2021/01/17 12:00 上午
# @Name    : celery_process.py
# @Desc    :

import sys

# sys.path.append("..")
from celery import Celery
# import ujson
# from kombu import serialization
from config.server_conf import current_environment

from celery_task.celery_config import dev_conf

# from celery.signals import after_setup_task_logger
# import logging


def make_celery_app(mode):
    conf = dev_conf[mode]
    app = Celery(conf.NAME, broker=conf.CELERY_BROKER_URL, backend=conf.RESULT_BACKEND)

    app.config_from_object(conf)
    # app.conf.update(conf)
    # app.logger = config.logger
    app.autodiscover_tasks()
    return app


# def foo_tasks_setup_logging(**kw):
#     logger = logging.getLogger('foo.tasks')
#     if not logger.handlers:
#         handler = logging.FileHandler('tasks.log')
#         formatter = logging.Formatter(logging.BASIC_FORMAT)  # you may want to customize this.
#         handler.setFormatter(formatter)
#         logger.addHandler(handler)
#         logger.propagate = False


celery_app = make_celery_app(current_environment)
# after_setup_task_logger.connect(logger)

# conf = dev_conf[current_environment]
# celery_app = Celery(__name__, broker=conf.CELERY_BROKER_URL, backend=conf.CELERY_RESULT_BACKEND)
# celery_app = Celery(__name__)
# celery_app.conf.update(conf)
# celery_app.config_from_object(conf)


# from celery.schedules import crontab
# from celery.schedules import timedelta

# from . import current_config

# from .extensions.my_logger.extensions_log import handler
# from config.myLog import logger

# celery_app = Celery(__name__, broker=celery_conf.CELERY_BROKER_URL, backend=celery_conf.CELERY_RESULT_BACKEND)
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
# _set_current_app(celery_app)
# celery_app.autodiscover_tasks("business_layer.extract_business_layer_task")


# def make_celery():
#
#     class CeleryTask(object):
#         # 导入指定的任务模块
#         CELERY_IMPORTS = {
#             'celery_process',
#             'tasks',
#             'a.tasks'
#             "business_layer.extract_business_layer_task"
#         }
#     celery_app.config_from_object(CeleryTask())

# return CeleryTask()
#
#
# @celery_app.task
# def document_parse():
#     # html = common_request("http://www.baidu.com")
#     # logger.info("html")
#     print("html")
#     # return html
