#!/usr/bin python3
# !/usr/bin/env python

# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : extensions.py.py
# @Desc    :

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config.server_conf import current_config
from common.common_conf import get_redis_config

from utils.redis_tools import Redis

# # 创建数据库管理对象db
db = SQLAlchemy()
migrate = Migrate(db=db)
# cache = Redis(get_redis_config(current_config.REDIS_CONF))


# 初始化
def config_extensions(app):
    """
    用于初始化：第三方模块及自己写的模块对象
    :param app: flask主对象
    :return: 没有返回值
    """
    # from initialization.sqlalchemy_process import init_db
    # init_db(app)

    # from initialization.jwtextend_process import JWTProcess
    # JWTProcess(app).init_jwt_decorator()

    # db.init_app(app)
    migrate.init_app(app)
