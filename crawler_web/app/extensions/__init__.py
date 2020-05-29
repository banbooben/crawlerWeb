#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-04-12 15:53:31
# @FilePath: /crawler_web/app/extensions/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.extensions.pyaria2c.aria2 import Aria2
from ..conf.server_conf import aria_token, aria_port, aria_host
from app.extensions.my_logger.extensions_log import handler
from app.extensions.my_logger import MyLogger
"""
数据库管理配置文件
"""

# 创建数据库管理对象db
db = SQLAlchemy()
migrate = Migrate(db=db)
aria2_downloader = Aria2(aria_host, aria_port, aria_token)
logger = MyLogger()


# 初始化
def config_extensions(app):
    """
    用于初始化：第三方模块及自己写的模块对象
    :param app: flask主对象
    :return: 没有返回值
    """
    db.init_app(app)
    migrate.init_app(app)
