#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-04-08 23:12:56
# @FilePath: /aria2_web/app/apis/__init__.py

from flask_restful import Api
from .aria import AriaAPI
from .crawlers import CrawlerAPI

# 配置路由地址
"""
原理：
api.add_resource(resource, url)
1、将创建的接口类注册到app中
"""

DEFAULT_RESOURCE = (
    (AriaAPI, '/api/aria2/'),
    (CrawlerAPI, '/api/crawler/'),
)


def config_resource(app):
    api = Api(app)
    for resource, url in DEFAULT_RESOURCE:
        api.add_resource(resource, url)
