#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 5:45 下午
# @Author  : shangyameng@aliyum.com

# 注册蓝本：在看得见app的地方
from app.route.aria_route import aria

# 注册时也可以指定相关的蓝本参数，优先级高于创建时的参数
ALL_BLUEPRINT = (
    aria,
)


def route_extensions(app):
    for item in ALL_BLUEPRINT:
        app.register_blueprint(item, url_prefix="/{}".format(item.name))
