#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-08-31 13:00:22
# @LastEditTime: 2021-08-31 13:29:07
# @FilePath: /app/apis/user/user_resource.py

from flask import request
from flask_restful import Resource
# from initialization.base_resource_process import BaseResource

from initialization.application import custom_response_
from initialization.base_error_process import APIException

from common.decorators import Decorator


class UserLoginResource(Resource):
    # @Decorator.add_request_id
    def post(self):
        return custom_response_.response()
