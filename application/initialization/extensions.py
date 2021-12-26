#!/usr/bin python3
# !/usr/bin/env python

# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : extensions.py
# @Desc    :

from .extensions_process.request_files_process import FlaskRequestFilesFunc

request_file_tools_ = FlaskRequestFilesFunc()


# 初始化
def config_extensions(app):
    """
    用于初始化：第三方模块及自己写的模块对象
    :param app: flask主对象
    :return: 没有返回值
    """
    from .extensions_process.flask_sqlalchemy_process import init_db
    init_db(app)

    from application.initialization.extensions_process.jwtextend_process import JWTProcess
    # JWTProcess(app).init_jwt_decorator()

    # from flask_app.extensions.APScheduler import schedule_init
    # schedule_init()
    ...
