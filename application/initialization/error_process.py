# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : error_process.py.py
# @Desc    :

import json
from flask import jsonify, request

from werkzeug.exceptions import HTTPException
from application.initialization.application import logger


class ExceptionBase(Exception):
    def __init__(self, message="", code=400, data=None, error_data=None):
        super().__init__()
        self.message = ""
        self.code = code
        self.payload = data or {}
        self.error_data = error_data or {}
        self.set_default_code()
        self.message += f"\n{message}"

    def to_dict(self):
        rv = dict(self.payload or ())
        rv.update(self.get_request_id())
        rv['message'] = self.message.strip()
        rv['code'] = self.code
        if not rv.get("data"):
            rv['data'] = self.error_data
        logger.error(json.dumps(rv, ensure_ascii=False))
        # logger.exception(Exception)
        return rv

    @staticmethod
    def get_request_id():
        from flask import request
        request_id = None

        try:
            request_id = request.request_id
        finally:
            return {"request_id": request_id}

    def set_default_code(self):
        ...


class APIException(ExceptionBase):

    def set_default_code(self):
        if self.code == "E001":
            self.message = "缺少username"
        elif self.code == "E002":
            self.message = "缺少password"
        elif self.code == "E003":
            self.message = "缺少token"
        elif self.code == "E004":
            self.message = "参数校验失败，缺少参数！"
        elif self.code == "E005":
            self.message = "当前流程未处理完毕，暂不支持操作！"
        elif self.code == "E006":
            self.message = "当前流程不支持合同的批量操作！"
        elif self.code == "E007":
            self.message = "无权限操作此合同"
        elif self.code == "E008":
            self.message = "待删除资源不存在，请确认"
        elif self.code == "E009":
            self.message = "该文档类型暂不支持，请联系管理人员"
        elif self.code == "E010":
            self.message = "必要参数校验失败！"
        elif self.code == "E011":
            self.message = "操作数据出错, 请联系开发人员"
        elif self.code == "E012":
            self.message = "当前状态不支持此操作，请核对！"
        elif self.code == "E013":
            self.message = "参数校验失败，参数不合法！"
        elif self.code == "E014":
            self.message = "缺少更新数据！"


class TypeException(ExceptionBase):

    def set_default_code(self):
        if self.code == "T001":
            self.message = "变量类型错误"
        elif self.code == "T002":
            self.message = "无法加密"
        elif self.code == "T003":
            self.message = "无法解密"
        elif self.code == "E004":
            self.message = "参数校验失败"
        elif self.code == "E005":
            self.message = "LADP接口请求失败"
        elif self.code == "E006":
            self.message = "缺少username"
        elif self.code == "E007":
            self.message = "缺少username"


class FileException(ExceptionBase):

    def set_default_code(self):
        if self.code == "F001":
            self.message = "缺少文件！"
        elif self.code == "F002":
            self.message = "文件不存在！"
        elif self.code == "F003":
            self.message = "上传文件中含有错误类型！"
        elif self.code == "F004":
            self.message = "文件保存失败！"
        elif self.code == "F005":
            self.message = "模版文件不存在！"
        elif self.code == "F006":
            self.message = "文件信息获取失败！"
        elif self.code == "F007":
            self.message = "转换PDF文档失败！"
        elif self.code == "F008":
            self.message = "待下载的文件不存在！"


class ModelException(ExceptionBase):

    def set_default_code(self):
        if self.code == "M001":
            self.message = "参数校验错误！"
        elif self.code == "M002":
            self.message = "数据添加失败！"
        elif self.code == "M003":
            self.message = "查询数据不存在！"
        elif self.code == "M004":
            self.message = "文件保存失败！"
        elif self.code == "M005":
            self.message = "模版文件不存在！"


class IdpsException(ExceptionBase):

    def set_default_code(self):
        if self.code == "I001":
            self.message = "比对任务创建失败！"
        elif self.code == "I002":
            self.message = "抽取任务创建失败！"
        elif self.code == "I003":
            self.message = "审核任务创建失败！"
        elif self.code == "I004":
            self.message = "比对任务创建失败！"
        elif self.code == "I005":
            self.message = "比对任务创建失败！"


class ExtractException(ExceptionBase):
    status_code = 400

    def to_dict(self):
        rv = dict(self.payload or ())
        rv.update(self.get_request_id())
        rv['message'] = self.message
        rv['code'] = self.code if self.code else self.status_code
        rv['status'] = "FAIL"
        rv['data'] = {}
        logger.error(json.dumps(rv))
        return rv

    def set_default_code(self):

        if self.code == "E01":
            if not self.message:
                self.message = "缺少文件！"


def init_error(app):
    @app.errorhandler(APIException)
    @app.errorhandler(FileException)
    @app.errorhandler(ExtractException)
    @app.errorhandler(TypeException)
    @app.errorhandler(ModelException)
    @app.errorhandler(IdpsException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.code if str(error.code).isdigit() else 400
        return response

    # @app.errorhandler(ExtractException)
    # def extract_error_handle(error):
    #     response = jsonify(error.to_dict())
    #     response.status_code = error.status_code
    #     return response
    #
    # @app.errorhandler(FileException)
    # def file_error_handle(error):
    #     response = jsonify(error.to_dict())
    #     response.status_code = error.status_code
    #     return response

    @app.errorhandler(405)
    def extract_error_handle(error):
        return {"code": 405, "message": "Method Not Allowed", "status": "FAIL", "id": request.request_id}

    @app.errorhandler(404)
    def extract_error_handle(error):
        return {"code": 404, "message": "The requested URL was not found on the server", "status": "FAIL",
                "id": request.request_id}

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": "E04",
            "id": request.request_id,
            "message": e.description,
            "status": "FAIL",
            "name": e.name,
        })
        response.content_type = "application/json"
        return response

    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     """Return JSON instead of HTML for HTTP errors."""
    #     # start with the correct headers and status code from the error
    #     response = e.get_response()
    #     # replace the body with JSON
    #     response.data = json.dumps({
    #         "code": "E04",
    #         "id": request.request_id,
    #         "message": e.description,
    #         "status": "FAIL",
    #         "name": e.name,
    #     })
    #     response.content_type = "application/json"
    #     return response


def register_blueprint_error(blueprint):
    @blueprint.app_errorhandler(APIException)
    @blueprint.app_errorhandler(TypeException)
    @blueprint.app_errorhandler(FileException)
    @blueprint.app_errorhandler(ExtractException)
    @blueprint.app_errorhandler(ModelException)
    @blueprint.app_errorhandler(IdpsException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.code if error.code.isdigit() else 400
        return response

    # @blueprint.app_errorhandler(ExtractException)
    # def extract_error_handle(error):
    #     response = jsonify(error.to_dict())
    #     response.status_code = error.status_code
    #     return response

    @blueprint.app_errorhandler(405)
    def extract_error_handle(error):
        return {"code": 405, "message": "Method Not Allowed", "status": "FAIL", "id": request.request_id}

    @blueprint.app_errorhandler(404)
    def extract_error_handle(error):
        return {"code": 404, "message": "The requested URL was not found on the server", "status": "FAIL",
                "id": request.request_id}
