#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:38 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : test.py
# @desc    :

# from flask import request

from . import auth

from marshmallow import Schema, fields

from application.common.decorators import Decorator

from application.initialization.logger_process import logger

from application.initialization.resource_process import BaseResource


# from ...initialization.error_process import APIException


class AuthTest(BaseResource):
    @Decorator.deserialization
    @auth.doc(operationId="ceshi")
    @auth.arguments(Schema.from_dict({
        "test": fields.Str(missing="123"),
        "test2": fields.Str(missing="123")
    }), location="json")
    @Decorator.deserialization
    def get(self, params):
        logger.info(f"{params=}")
        logger.info(f"{params.text=}")
        data = {}
        return self.response(data=data)

    @auth.doc(operationId="ceshias")
    @auth.arguments(Schema.from_dict({
        "test": fields.Str(missing="123"),
        "test2": fields.Str(missing="123")
    }), location="query")
    @Decorator.time_func
    @Decorator.deserialization
    def post(self, params):
        logger.info(f"{params=}")
        params.update({"aaa": 666})
        logger.info(f"{params=}")
        logger.info(f"{params.test=}")
        logger.info(f"{params.aaa=}")
        data = {}
        return self.response(data=data)
