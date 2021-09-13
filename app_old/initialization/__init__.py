# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : __init__.py.py
# @Desc    :

from flask import Flask
from flask_cors import CORS
from flask_log_request_id import RequestID

from apis import register_resource_and_blueprint
from config.server_conf import current_config
# from extensions.celery_task.celery_config import celery_conf
# from route import route_extensions∂

from initialization.extensions import config_extensions
from initialization.application import logger
from initialization.error_process import init_error
from initialization.request_process import init_hook_function, Request


# from initialization.celery_process import make_celery

# def init_app(config_name='default'):
def init_app():
    # if config_name == "default" or config_name not in config:
    #     current_conf = current_config
    # else:
    #     current_conf = config[config_name]

    # 初始化app
    flask_app = Flask(__name__,
                      template_folder=current_config.TEMPLATE_FOLDER,
                      static_folder=current_config.STATIC_FOLDER,
                      static_url_path=current_config.STATIC_URL_PATH)

    # 配置基类
    flask_app.config.from_object(current_config)

    # 注册生成celery
    # celery_app.conf.update(flask_app.config)
    # celery_app.config_from_object(celery_conf)
    # make_celery()
    # celery_app.config_from_object(make_celery())
    # make_celery()

    # 设置跨域
    flask_app.config["JSON_AS_ASCII"] = False
    CORS(flask_app, supports_credentials=True)

    # 重写request，并添加相关方法
    flask_app.request_class = Request

    # 注册全局错误
    init_error(flask_app)

    # 注册钩子函数
    init_hook_function(flask_app)

    # 配置蓝本路由、api接口
    register_resource_and_blueprint(flask_app)

    # # 配置日志
    # flask_app.logger.addHandler(logger)

    # 配置扩展
    config_extensions(flask_app)

    # 注册获取请求ID，供日志使用
    RequestID(flask_app)

    # # 配置蓝本路由
    # route_extensions(flask_app)
    #
    # # 配置api接口
    # config_resource(flask_app)

    return flask_app

# app_conf = {"http_host": HTTP_HOST, "http_port": HTTP_PORT}
