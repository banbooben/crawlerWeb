#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-09-01 22:34:13
# @FilePath: /crawlerWeb/crawler_web/blueprint_modules/aria/__init__.py

from .aria import AriaAPI

from flask import redirect, Blueprint, current_app

aria = Blueprint("aria", __name__, static_folder='../static/aria', static_url_path='../static/aria')


# 配置路由地址
"""
原理：
api.add_resource(resource, url)
1、将创建的接口类注册到app中
"""

aria_api = (
    (AriaAPI, '/api/aria2/'),
)


