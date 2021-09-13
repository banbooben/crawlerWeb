#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:36 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : __init__.py.py
# @desc    :

from flask import Blueprint
from .ap_scheduler import (
    APSchedulerJobsBaseResource,
    APSchedulerJobsResource,
    APSchedulerJobResource,
)

scheduler = Blueprint("scheduler",
                      __name__,
                      static_folder='../static/scheduler',
                      static_url_path='../static/scheduler')

# 是否启动本模块
enable = True

# 对象
registry = {
    # 路由
    "RESOURCE": (
        (APSchedulerJobsBaseResource, "/api/scheduler/jobs"),
        (APSchedulerJobsResource, "/api/scheduler/jobs/<string:job_id>"),
        (APSchedulerJobResource, "/api/scheduler/jobs/<string:job_id>/<string:active>"),
    ),
    # 蓝本
    "BLUEPRINT": scheduler,
}
