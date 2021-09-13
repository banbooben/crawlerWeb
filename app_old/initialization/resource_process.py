#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 17:45
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    : 
# @File    : resource_process.py
# @desc    :

from flask_restful import Resource
from flask import request


class BaseResource(Resource):

    def response(self, message=None, code=200, result=None, *args, **kwargs):
        message = message or ""
        data = result or {}

        resp = {
            "message": message,
            "code": code,
            'result': data,
            "history_id": request.request_id
        }

        resp.update(kwargs)
        return resp

