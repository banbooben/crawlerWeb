#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 23:00:27
# @LastEditTime: 2020-04-23 20:44:46
# @FilePath: /crawler_web/app/__init__.py

from flask import Flask
from flask_cors import CORS
from .extensions import config_extensions
# from .extensions.my_logger.extensions_log import handler
from app.common.application import logger
from .apis import config_resource
from .conf.server_conf import config
from .route import route_extensions


def init_app(config_name='default'):
    flask_app = Flask(__name__, static_url_path='')

    # 配置基类
    if config_name not in config:
        config_name = 'default'
    flask_app.config.from_object(config[config_name])

    # 设置跨域
    flask_app.config["JSON_AS_ASCII"] = False
    CORS(flask_app, supports_credentials=True)

    # 配置蓝本路由
    route_extensions(flask_app)

    # 配置日志
    flask_app.logger.addHandler(logger)

    # 配置api接口
    config_resource(flask_app)

    # 配置扩展
    config_extensions(flask_app)
    return flask_app


# app_conf = {"http_host": HTTP_HOST, "http_port": HTTP_PORT}
