#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-07-01 16:49:04
# @LastEditTime: 2021-08-31 13:29:41
# @FilePath: /app/initialization/base_custom_response.py


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
        self._response_data.update(data)
        self._response_data.update(kwargs)
        return self._response_data
