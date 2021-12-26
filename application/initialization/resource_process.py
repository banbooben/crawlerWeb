#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 17:45
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    :
# @File    : resource_process.py
# @desc    :

# from flask_restful import Resource
from flask import request
from flask_restful import Api as _Api, Resource
from application.common.decorators import Decorator


class Api(_Api):
    def handle_error(self, e):
        raise e


class CustomResponse(object):
    def __init__(self, message="success", code=200, data=None, *args, **kwargs):
        self._message = message
        self._code = code
        self._data = data or {}
        self._args = args
        self._kwargs = kwargs

        self._response_data = {
            "message": self._message,
            "code": self._code,
            'data': self._data,
        }
        self._response_data.update(kwargs)

    def response(self, message=None, code=200, data=None, *args, **kwargs):
        message = message or self._message
        data = data or self._data
        self._response_data.update({"data": data, "message": message, "code": code})
        self._response_data.update(kwargs)
        self._add_request_id()
        return self._response_data

    def _add_request_id(self):
        from flask import request
        self._response_data.update({
            "request_id": request.request_id
        })


class BaseResource(Resource):
    custom_response_ = CustomResponse()

    def response(self, *args, **kwargs):
        return self.custom_response_.response(*args, **kwargs)


custom_response_ = CustomResponse()
