#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-04-12 15:53:31
# @FilePath: /crawler_web/app/extensions/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cache import Cache
#
from app.conf.server_conf import get_redis_config
from app.conf.server_conf import current_config
host, port, database, decode_responses, redis_password, cache_type = get_redis_config(current_config)

# 创建数据库管理对象db
db = SQLAlchemy()
migrate = Migrate(db=db)
cache = Cache(
    config={"CACHE_TYPE": cache_type,
            "CACHE_REDIS_HOST": host,
            "CACHE_REDIS_PORT": port,
            "CACHE_REDIS_DB": database,
            "DECODE_RESPONSES": decode_responses,
            "CACHE_REDIS_PASSWORD": redis_password})


# 初始化
def config_extensions(app):
    """
    用于初始化：第三方模块及自己写的模块对象
    :param app: flask主对象
    :return: 没有返回值
    """
    db.init_app(app)
    migrate.init_app(app)
    cache.init_app(app)
