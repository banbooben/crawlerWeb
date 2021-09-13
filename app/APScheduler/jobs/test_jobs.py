#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:56 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : test_jobs.py
# @desc    :

import time

from APScheduler.scheduler_logger import logger

from servers import extract_business_


class TestJob(object):

    def print_info(self):
        logger.info(f"test {time.time()}")

    def test_002(self):
        extract_business_.get_business()
