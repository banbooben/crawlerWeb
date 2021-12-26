#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 12:20 上午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : async_tasks_status.py
# @desc    :
import json

from application.tools.requests_tools import request_tools_
from application.initialization.logger_process import logger


class AsyncTaskStatus(object):

    def __init__(self):
        self.host = "http://127.0.0.1:8000"

    def async_idps_tasks(self):
        url = f"{self.host}/async/tasks"
        res = request_tools_.common_request_to_json(url)
        logger.info(json.dumps(res))

    def async_oad_task_status(self):
        url = f"{self.host}/async/oad/diff/tasks"
        res = request_tools_.common_request_to_json(url)
        logger.info(json.dumps(res))

    def async_user_info(self):
        url = f"{self.host}/async/users"
        res = request_tools_.common_request_to_json(url)
        logger.info(json.dumps(res))


async_task_status_ = AsyncTaskStatus()

jobs = {
    async_task_status_.async_idps_tasks: {
        "trigger": 'cron',
        "second": '*/10',
        "coalesce": True,
    },
    async_task_status_.async_oad_task_status: {
        "trigger": 'cron',
        "second": '*/10',
        "coalesce": True,
    },
}
