#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-09-01 00:08:01
# @LastEditTime: 2020-09-01 00:09:22
# @FilePath: /crawlerWeb/crawler_web/blueprint_modules/test/__init__.py

from .testApi import TestApi

test_api = (
    (TestApi, '/api/test/'),
)
