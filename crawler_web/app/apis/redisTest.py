#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/22 11:24
# @Author  : shangyameng@datagrand.com
# @Site    : 
# @File    : redisTest.py

from flask import request, current_app, render_template
from flask_restful import Resource
from ..application import aria2_downloader, logger, cache_redis


class RedisTest(Resource):

    def get(self):
        pass

    def post(self):
        pass



