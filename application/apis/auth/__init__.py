#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:36 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : __init__.py.py
# @desc    :

# from .blueprint import scheduler

# from flask import Blueprint
from flask_smorest import Blueprint
from application.config.server_conf import current_config

auth = Blueprint("auth",
                 __name__,
                 static_folder=f'{current_config.STATIC_FOLDER}/auth',
                 static_url_path='/')


class BPInit(object):
    # 是否启动本模块
    enable = True
    blueprint = auth

    from .test import (
        AuthTest,
    )

    resource = (
        (AuthTest, ""),
    )
