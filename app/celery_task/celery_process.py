# !/usr/bin/env python
# coding:utf-8
# @Time    : 2021/01/17 12:00 上午
# @Name    : celery_process.py
# @Desc    :

from celery import Celery
from config.server_conf import current_environment

from celery_task.celery_config import dev_conf
from celery_task.celery_logger import foo_tasks_setup_logging
from celery.signals import after_setup_task_logger


def make_celery_app(mode):
    conf = dev_conf[mode] if mode in dev_conf.keys() else dev_conf["default"]
    app = Celery(conf.NAME, broker=conf.CELERY_BROKER_URL, backend=conf.RESULT_BACKEND)

    app.config_from_object(conf)
    app.autodiscover_tasks()
    return app


celery_app = make_celery_app(current_environment)
after_setup_task_logger.connect(foo_tasks_setup_logging)
