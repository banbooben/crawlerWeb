#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-08-18 18:12:30
# @LastEditTime: 2021-08-19 16:33:59
# @FilePath: /app/APScheduler/ap_scheduler.py

import sys
from pytz import utc
from initialization.application import logger

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.gevent import GeventScheduler
# from apscheduler.schedulers.tornado import TornadoScheduler
# from apscheduler.schedulers.twisted import TwistedScheduler
# from apscheduler.schedulers.qt import QtScheduler

from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# from apscheduler.jobstores.rethinkdb import RethinkDBJobStore
# from apscheduler.jobstores.zookeeper import ZooKeeperJobStore

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from apscheduler.triggers import (date, interval, cron)

from config.server_conf import current_config, current_environment


class APSchedulerConfig(object):
    LOG_FILE_PATH = current_config.LOG_DIR + "/scheduler.log"
    LOG_LEVEL = "INFO"


class ProductConfig(APSchedulerConfig):
    scheduler_config = {
        "jobstores": {
            'default': SQLAlchemyJobStore(url=current_config.SQLALCHEMY_DATABASE_URI)
        },
        "executors": {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(4)
        },
        "job_defaults": {
            'coalesce': False,
            'max_instances': 3
        },
        "timezone": utc
    }
    LOG_LEVEL = "DEBUG"


class LocalConfig(APSchedulerConfig):
    scheduler_config = {
        "jobstores": {
            'default': SQLAlchemyJobStore(url='sqlite:////Users/sarmn/my_project/APScheduler/jobs.sqlite')
        },
        "executors": {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(4)
        },
        "job_defaults": {
            'coalesce': False,
            'max_instances': 3
        },
        "timezone": utc
    }

    LOG_LEVEL = "INFO"


scheduler_config = {
    "default": LocalConfig,
    "product": ProductConfig,
}.get(current_environment, "default")

scheduler = BackgroundScheduler(**scheduler_config.scheduler_config)
scheduler.start()
