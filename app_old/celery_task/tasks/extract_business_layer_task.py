#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/16 16:52
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    :
# @File    : extract_business_layer.py
# @desc    :

from celery_task.celery_process import celery_app
from business_layer import extract_business


@celery_app.task()
def document_parse(params, nessry_info):
    nessry_info = extract_business.document_parse(params, nessry_info)
    return nessry_info


@celery_app.task()
def document_local_parse(params, nessry_info):
    nessry_info = extract_business.document_local_parse(params, nessry_info)
    return nessry_info
