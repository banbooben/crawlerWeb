#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 19:53
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    : 
# @File    : exception_process.py
# @desc    :

from initialization.application import logger
import json


class APIException(Exception):

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code if status_code else 500
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['code'] = self.status_code
        rv['data'] = {}
        logger.error(json.dumps(rv))
        return rv


class ExtractException(Exception):
    status_code = 400

    def __init__(self, message="", code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
        self.code = code
        self.set_default_code()

    def to_dict(self):
        rv = dict(self.payload or ())
        rv.update(self.get_extract_id())
        rv['message'] = self.message
        rv['code'] = self.code if self.code else self.status_code
        rv['status'] = "FAIL"
        rv['data'] = {}
        logger.error(json.dumps(rv))
        return rv

    def set_default_code(self):

        if self.code == "E01":
            if not self.message:
                self.message = "必传参数错误"
        elif self.code == "E02":
            if not self.message:
                self.message = "上传文件类型错误"
        elif self.code == "E03":
            if not self.message:
                self.message = "文件读写、保存失败，检查文件是否可读、可写"
        elif self.code == "E04":
            if not self.message:
                self.message = "系统内部错误"
        elif self.code == "E05":
            if not self.message:
                self.message = "PDF文件解析失败"
        elif self.code == "E06":
            if not self.message:
                self.message = "word文件解析失败"
        elif self.code == "E07":
            if not self.message:
                self.message = "文档解析失败"

    @staticmethod
    def get_extract_id():
        from flask import request

        report_id = request.params.get("report_id", None)
        if report_id:
            return {"id": report_id}
        return {}
