#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 7:01 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : scheduler_logger.py
# @desc    :

from APScheduler.ap_scheduler import scheduler_config

from loguru import logger


def my_filter(log_record):
    from flask import request
    try:
        log_record["request_id"] = request.request_id
    except:
        log_record["request_id"] = "null"

    return log_record


log_conf = {
    "handlers": [
        {"sink": scheduler_config.LOG_FILE_PATH,
         "level": scheduler_config.LOG_LEVEL,
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
