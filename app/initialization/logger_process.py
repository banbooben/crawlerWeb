# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:38 下午
# @Name    : logger_process.py
# @Desc    :

import logging

from logging import config
from pathlib import Path

from flask_log_request_id import RequestIDLogFilter
from config.server_conf import current_config

ROOT_LOG = current_config.LOG_DIR + '/root.log'
ERROR_LOG = current_config.LOG_DIR + '/error.log'
Path(current_config.LOG_DIR).mkdir(exist_ok=True)

LOG_CONF = {
    'version': 1,
    'incremental': False,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': ('%(asctime)s - %(request_id)s - %(levelname)s - %(filename)s:%(lineno)s'
                       ' - [%(funcName)s]:  %(message)s'),
        }
    },
    'filters': {
        'req_id_filter': {
            '()': RequestIDLogFilter        # 获取请求中的 request_id
        }
    },
    'handlers': {
        'default': {

            # # 日期格式的日志
            # "class": "logging.handlers.TimedRotatingFileHandler",
            # "backupCount": 10,
            # "when": "d",
            # "filename": ROOT_LOG,

            # 文件格式的日志
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': ROOT_LOG,  # 日志输出文件位置
            'backupCount': 5,  # 备份份数
            'maxBytes': 1024 * 1024 * 20,  # 文件大小

            'level': logging.DEBUG,
            'formatter': 'standard',
            'encoding': 'utf-8',
            'filters': ['req_id_filter'],  # 使用哪种formatters日志格式
        },
        'error': {

            # # 日期格式的日志
            # "class": "logging.handlers.TimedRotatingFileHandler",
            # "backupCount": 10,
            # "when": "d",
            # "filename": ROOT_LOG,

            # 文件格式的日志
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': ROOT_LOG,  # 日志输出文件位置
            'backupCount': 5,  # 备份份数
            'maxBytes': 1024 * 1024 * 20,  # 文件大小

            'level': logging.ERROR,
            'formatter': 'standard',
            'encoding': 'utf-8',
            'filters': ['req_id_filter'],  # 使用哪种formatters日志格式
        },
        'info': {

            # # 日期格式的日志
            # "class": "logging.handlers.TimedRotatingFileHandler",
            # "backupCount": 10,
            # "when": "d",
            # "filename": ROOT_LOG,

            # 文件格式的日志
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': ROOT_LOG,  # 日志输出文件位置
            'backupCount': 5,  # 备份份数
            'maxBytes': 1024 * 1024 * 20,  # 文件大小


            'level': logging.INFO,
            'formatter': 'standard',
            'encoding': 'utf-8',
            'filters': ['req_id_filter'],  # 使用哪种formatters日志格式
        },
        'debug': {

            # # 日期格式的日志
            # "class": "logging.handlers.TimedRotatingFileHandler",
            # "backupCount": 10,
            # "when": "d",
            # "filename": ROOT_LOG,

            # 文件格式的日志
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': ROOT_LOG,  # 日志输出文件位置
            'backupCount': 5,  # 备份份数
            'maxBytes': 1024 * 1024 * 20,  # 文件大小

            'level': logging.DEBUG,
            'formatter': 'standard',
            'encoding': 'utf-8',
            'filters': ['req_id_filter'],  # 使用哪种formatters日志格式
        },
        'stream_info': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'standard',
            'filters': ['req_id_filter']
        }
    },
    'loggers': {
        'default': {
            'level': "DEBUG",
            'propagate': 0,
            'handlers': ['debug', "stream_info"]
        },
        "product": {
            "level": "INFO",
            "handlers": ["info"],
            "propagate": 0,
            "qualname": "product"
        },
        "test": {
            "level": "DEBUG",
            "handlers": ["debug"],
            "propagate": 0,
            "qualname": "test"
        }
    },
    'root': {
        'level': logging.INFO,
        "propagate": 0,
        'handlers': ['info']
    },
}

# class RequestIdLogRecord(logging.LogRecord):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         from flask import request
#         try:
#             self.request_id = request.request_id
#         except:
#             self.request_id = "null"
#
#
# logging.setLogRecordFactory(RequestIdLogRecord)

config.dictConfig(LOG_CONF)
logger = logging.getLogger(current_config.LOG_LEVEL)

__all__ = ['logger']
