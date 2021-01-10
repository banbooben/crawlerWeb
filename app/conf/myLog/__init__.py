#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/24 17:30
# @Author  : shangyameng@datagrand.com
# @Site    : 
# @File    : __init__.py.py

import os
from .my_log import Logger
from pathlib import Path


# def set_logs_path(num):
#     log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
#     while num > 0:
#         log_path = os.path.dirname(log_path)
#         num -= 1
#     log_path = os.path.join(log_path, "logs")
#     return log_path


logger = Logger(log_path=Path().cwd().parent.parent / "logs")
