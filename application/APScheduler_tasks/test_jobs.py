#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:56 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : test_jobs.py
# @desc    :

import time

from application.initialization.logger_process import logger


class TestJob(object):

    def print_info(self):
        logger.info(f"test {time.time()}")

    def test_002(self):
        logger.info("test")
        # extract_business_.get_business()


test_jobs_ = TestJob()

jobs = {
    test_jobs_.print_info: {
        "trigger": 'cron',
        "second": '*/5',
        "coalesce": True,
    },
    test_jobs_.test_002: {
        "trigger": 'cron',
        "second": '*/3',
        "coalesce": True,
    },
}
