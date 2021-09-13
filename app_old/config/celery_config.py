#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/18 18:07
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    : 
# @File    : celery_config.py
# @desc    :
import sys

sys.path.append("..")
from config.server_conf import current_config
from common.common_conf import get_redis_config


class CeleryConfigBase(object):
    NAME = "celery_test"
    redis_config = get_redis_config(current_config.REDIS_CONF)

    # celery获取任务地址
    # CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_BROKER_URL = f'redis://{redis_config["host"]}:{redis_config["port"]}/{redis_config["db"]}'
    # celery任务结果返回地址
    RESULT_BACKEND = f'redis://{redis_config["host"]}:{redis_config["port"]}/1'

    # 导入指定的任务模块
    # CELERY_IMPORTS = {
    #     'celery_task.tasks',
    # }
    # IMPORTS = [
    #     'celery_task.tasks.test_task',
    # ]
    # imports = ["celery_task.tasks", ]
    imports = (
        # 'celery_task.tasks',
        'business_layer.extract_business_layer',
    )


# class CeleryTestEnv(CeleryConfigBase):
#
#     imports = ["extensions.celery_task.tasks", ]
#
#
# class CeleryDevEnv(CeleryConfigBase):
#
#     imports = ["extensions.celery_task.tasks", ]


dev_conf = {
    'default': CeleryConfigBase,
    'test': CeleryConfigBase,
    'product': CeleryConfigBase,
}
