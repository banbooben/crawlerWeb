#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:36 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : __init__.py.py
# @desc    :

from flask import Blueprint
from .user_resource import UserLoginResource

user = Blueprint("user", __name__, static_folder='../static/scheduler', static_url_path='../static/scheduler')

# 是否启动本模块
enable = True

# 对象
registry = {
    # 路由
    "RESOURCE": (
        (UserLoginResource, "/api/login"),
    ),
    # 蓝本
    "BLUEPRINT": user,
}
