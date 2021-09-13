#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 17:45
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    :
# @File    : base_resource_process.py
# @desc    :

from flask_restful import Resource
from flask import request


class BaseResource(Resource):
    def data(self):
        return request.params

    def files(self):
        return request.files
