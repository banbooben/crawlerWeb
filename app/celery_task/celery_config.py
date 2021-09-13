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

    CELERY_LOG_FILE = current_config.LOG_DIR + "/celery.log"
    LOG_LEVEL = current_config.LOG_LEVEL
    # CELERY_ENABLE_UTC = True  # 启用UTC时区
    # CELERY_TIMEZONE = 'Asia/Shanghai'  # 上海时区
    # CELERYD_HIJACK_ROOT_LOGGER = False  # 拦截根日志配置
    # CELERYD_MAX_TASKS_PER_CHILD = 1  # 每个进程最多执行1个任务后释放进程（再有任务，新建进程执行，解决内存泄漏）
    # celery获取任务地址
    # CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    # if redis_config["redis_password"]:
    if redis_config["password"]:
        CELERY_BROKER_URL = f'redis://:{redis_config["password"]}@{redis_config["host"]}:{redis_config["port"]}/{redis_config["db"]}'
        # celery任务结果返回地址
        RESULT_BACKEND = f'redis://:{redis_config["password"]}@{redis_config["host"]}:{redis_config["port"]}/1'
    else:
        CELERY_BROKER_URL = f'redis://{redis_config["host"]}:{redis_config["port"]}/{redis_config["db"]}'
        # celery任务结果返回地址
        RESULT_BACKEND = f'redis://{redis_config["host"]}:{redis_config["port"]}/1'


class CeleryTestEnv(CeleryConfigBase):
    # 导入指定的任务模块
    imports = (
        'celery_task.tasks',
        # 'business_layer.extract_business_layer',
    )


class CeleryProductEnv(CeleryConfigBase):
    # 导入指定的任务模块
    imports = (
        'celery_task.tasks',
        # 'business_layer.extract_business_layer',
    )


dev_conf = {
    'default': CeleryTestEnv,
    'test': CeleryTestEnv,
    'product': CeleryProductEnv,
}
