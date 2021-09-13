#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/18 18:04
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    : 
# @File    : a.py
# @desc    :

from initialization.application import logger
from celery_task.celery_process import celery_app

from servers.extract_business import ExtractApiBusiness


@celery_app.task
def document_parse():
    # html = common_request("http://www.baidu.com")
    logger.info("start test")
    ExtractApiBusiness().get_business()
    # return html
