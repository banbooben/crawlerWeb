#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2020年02月07日

@author: jianzhihua
'''

import os
from typing import Any

from flask import request
from flask_jwt_extended import JWTManager as _JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException


from utils.custom_response import CustomResponse


class JWTProcess(object):
    def __init__(self, app):
        from config.server_conf import current_config
        app.config['JWT_SECRET_KEY'] = current_config.SECRET_KEY

        app.config['SSO_LOGIGN'] = os.getenv('SSO_LOGIGN', True)
        app.config['LOGIN_KEY'] = os.getenv('LOGIN_KEY', "lk_")
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 60 * 60 * 24)

        self.app = app
        self.jwt = JWTManager(app)

        self.url_white_url = current_config.JWT_URL_WHITE_LIST

    def init_jwt_decorator(self):
        # @self.jwt.user_loader_callback_loader
        # def user_loader_callback(identity: dict):
        #     from blueprints.users.user_models import UserModel

        #     user_id = identity.get("user_id")
        #     if not user_id:
        #         raise JWTExtendedException("Invalid Token!")

        #     return UserModel.active_query.filter_by(id=user_id).first() or AnonymousUser()

        @self.app.before_request
        def jwt_auth():
            """
            在登录前验证接口中的jwt token是否有效
            """
            if request.args.get("is_debug") == "is_debug":
                return

            # 跳过一些验证..
            if (request.path, request.method) in frozenset(self.url_white_url):
                return

            verify_jwt_in_request()

        @self.app.errorhandler(JWTExtendedException)
        def no_auth_handler(error: JWTExtendedException):
            """
            @attention: 提示
            """
            # return ucr.op_fail(str(error), status=401), 401
            return CustomResponse.response(str(error), code=401), 401


class JWTManager(_JWTManager):
    def _set_error_handler_callbacks(self, app):
        """
        暂停注册错误, 由exception_process统一处理
        """
        ...


class AnonymousUser:
    """
    有别于登录的用户
    """

    is_superuser = False
    is_anonymous = True

    def __getattribute__(self, name: str) -> Any:
        if name in ('is_superuser', "is_anonymous"):
            return super().__getattribute__(name)
        return None
