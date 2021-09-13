# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:38 下午
# @Name    : base_logger_process.py
# @Desc    :

from loguru import logger

from pathlib import Path
from sys import stdout

from config.server_conf import current_config, current_environment

root_file = current_config.LOG_DIR + "/" + current_config.LOG_FILE_NAME
Path(current_config.LOG_DIR).mkdir(exist_ok=True)


def my_filter(log_record):
    from flask import request
    try:
        log_record["request_id"] = request.request_id
    except:
        log_record["request_id"] = "null"

    return log_record


local_config = {
    "file_handler": {"sink": root_file,
                     "level": current_config.LOG_LEVEL,
                     # "serialize": True,
                     "format": '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>'
                               ' - <green>{request_id}</green>'
                               ' - <level>{level: <8}</level>'
                               ' - <cyan>{name}</cyan>:<cyan>{line}</cyan>'
                               ' - [<cyan>{function}</cyan>]:  <level>{message}</level>',
                     "filter": my_filter,
                     "enqueue": True},
    "stream": {"sink": stdout,
               "level": current_config.LOG_LEVEL,
               "format": '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>'
                         ' - <green>{request_id}</green>'
                         ' - <level>{level: <8}</level>'
                         ' - <cyan>{name}</cyan>:<cyan>{line}</cyan>'
                         ' - [<cyan>{function}</cyan>]:  <level>{message}</level>',
               "filter": my_filter,
               },
}


handlers = []

if current_environment not in ["default", "base"]:
    handlers.append(local_config["file_handler"])
else:
    handlers.append(local_config["stream"])


logger.configure(**{"handlers": handlers})
