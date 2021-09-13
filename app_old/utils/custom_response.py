#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-07-01 16:49:04
# @LastEditTime: 2021-07-01 16:53:56
# @FilePath: /app/utils/custom_response.py


class CustomResponse(object):

    @classmethod
    def response(cls, message=None, code=200, result=None, *args, **kwargs):
        message = message or ""
        data = result or {}

        resp = {"message": message, "code": code, 'result': data}

        resp.update(kwargs)
        return resp
