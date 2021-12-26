#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/20 15:54
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    :
# @File    : celery_logger.py
# @desc    :

from loguru import logger
from application.extensions.celery_task.celery_config import dev_conf
from application.config.server_conf import current_environment

current_environment = current_environment if current_environment in dev_conf.keys() else "default"
celery_config = dev_conf[current_environment]


def my_filter(log_record):
    from flask import request
    try:
        log_record["request_id"] = request.request_id
    except:
        log_record["request_id"] = "null"

    return log_record


def foo_tasks_setup_logging(**kw):
    log_conf = {
        "handlers": [
            {"sink": celery_config.CELERY_LOG_FILE,
             "level": celery_config.LOG_LEVEL,
             # "serialize": True,
             "format": '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>'
                       ' - <green>{request_id}</green>'
                       ' - <level>{level: <8}</level>'
                       ' - <cyan>{name}</cyan>:<cyan>{line}</cyan>'
                       ' - [<cyan>{function}</cyan>]:  <level>{message}</level>',
             "filter": my_filter,
             "enqueue": True},
        ]
    }
    logger.configure(**log_conf)
