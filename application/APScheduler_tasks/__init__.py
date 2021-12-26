#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:56 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : __init__.py.py
# @desc    :
from functools import reduce

from .test_jobs import jobs as test_jobs
from .async_tasks_status import jobs as async_jobs

all_jobs = [
    test_jobs,
    # async_jobs,
]

__all__ = ["all_jobs"]
