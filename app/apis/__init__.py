#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-09-01 22:33:59
# @FilePath: /crawlerWeb/crawler_web/blueprint_modules/__init__.py

from flask_restful import Api

from .crawlers import crawler_api
from .test import test_api
from .aria import aria_api
# 注册蓝本：在看得见app的地方
from route.aria_route import aria
from route.auth import auth

# 配置路由地址
"""
原理：
api.add_resource(resource, url)
1、将创建的接口类注册到app中
"""

DEFAULT_RESOURCE = (aria_api, crawler_api, test_api)
# default_resource = (aria_api, crawler_api, test_api)

# 注册时也可以指定相关的蓝本参数，优先级高于创建时的参数
ALL_BLUEPRINT = (
    aria,
    auth,
)


def config_resource(app):
    api = Api(app)
    for blueprint_api in DEFAULT_RESOURCE:
        for resource, url in blueprint_api:
            api.add_resource(resource, url)


def route_extensions(app):
    for item in ALL_BLUEPRINT:
        app.register_blueprint(item, url_prefix="/{}".format(item.name))
