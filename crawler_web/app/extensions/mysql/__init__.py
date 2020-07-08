#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Project : crawler_web
# @File    : __init__.py.py
# @Author  : shangyameng@datagrand.com
# @Time    : 2020/5/4 09:08
# @desc: 


# from app.extensions.mysql.mysql_protogenesis import PyMysql
# from app.extensions.mysql.redis_protogenesis import Redis
from redis import Redis
from app.conf.server_conf import config, current_environment, get_mysql_info, get_redis_config

USER, PASSWORD, HOST, PORT, DATABASE = get_mysql_info(config[current_environment].DATABASES)
host, port, database, decode_responses, redis_password, cache_type = get_redis_config(config[current_environment])


# mysql = PyMysql()

# 创建
cache_redis = Redis(host=host, port=port, db=database, decode_responses=decode_responses, password=redis_password)
