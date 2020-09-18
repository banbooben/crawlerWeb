#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-09-01 21:52:48
# @LastEditTime: 2020-09-01 23:13:49
# @FilePath: /crawlerWeb/crawler_web/initialization/extensions.py

from extensions import db, migrate


# 初始化
def config_extensions(app):
    """
    用于初始化：第三方模块及自己写的模块对象
    :param app: flask主对象
    :return: 没有返回值
    """
    db.init_app(app)
    migrate.init_app(app)
    # cache.init_app(app)
