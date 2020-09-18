#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-09-01 23:30:11
# @FilePath: /crawlerWeb/crawler/extensions/__init__.py

from conf.extensions_conf import aria_host, aria_port, aria_token
from conf.server_conf import (current_config, get_mysql_info, get_redis_config)

from extensions.pyaria2c.aria2 import Aria2
from extensions.sql import Redis, RedisPool

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

USER, PASSWORD, HOST, PORT, DATABASE = get_mysql_info(current_config.DATABASES)

# 自定义模块初始化
host, port, database, decode_responses, redis_password, cache_type = get_redis_config(
    current_config)


# 初始化自定义模块的对象
aria2_downloader = Aria2(aria_host, aria_port, aria_token)

cache_pool = RedisPool(host, port, decode_responses,
                       redis_password).connect_poll
cache = Redis(cache_pool, database).connect()



# 创建数据库管理对象db
db = SQLAlchemy()
migrate = Migrate(db=db)

# cache = Cache(
#     config={
#         "CACHE_TYPE": cache_type,
#         "CACHE_REDIS_HOST": host,
#         "CACHE_REDIS_PORT": port,
#         "CACHE_REDIS_DB": database,
#         "DECODE_RESPONSES": decode_responses,
#         "CACHE_REDIS_PASSWORD": redis_password
#     })
