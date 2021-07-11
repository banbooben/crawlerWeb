# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : error_process.py.py
# @Desc    :

import json
from flask import jsonify, request
from utils.exception_process import APIException, ExtractException

from werkzeug.exceptions import HTTPException


def init_error(app):
    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ExtractException)
    def extract_error_handle(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

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
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @blueprint.app_errorhandler(ExtractException)
    def extract_error_handle(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @blueprint.app_errorhandler(405)
    def extract_error_handle(error):
        return {"code": 405, "message": "Method Not Allowed", "status": "FAIL", "id": request.request_id}

    @blueprint.app_errorhandler(404)
    def extract_error_handle(error):
        return {"code": 404, "message": "The requested URL was not found on the server", "status": "FAIL",
                "id": request.request_id}
