#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/5 23:55
# @Author  : shangyameng@aliyun.com
# @Site    : 
# @File    : application.py

from flask import current_app

from app.extensions import db
from app.extensions.pyaria2c.aria2 import Aria2
from app.extensions.sql import cache_redis
from app.extensions import cache
from app.conf import logger

from app.conf.extensions_conf import aria_token, aria_port, aria_host

"""
数据库管理配置文件
"""

aria2_downloader = Aria2(aria_host, aria_port, aria_token)
