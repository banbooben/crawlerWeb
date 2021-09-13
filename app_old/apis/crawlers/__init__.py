#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-08-31 17:02:12
# @LastEditTime: 2020-09-01 22:32:49
# @FilePath: /crawlerWeb/crawler_web/blueprint_modules/crawlers/__init__.py

from .crawlers import CrawlerAPI

crawler_api = ((CrawlerAPI, '/api/crawler/'), )
