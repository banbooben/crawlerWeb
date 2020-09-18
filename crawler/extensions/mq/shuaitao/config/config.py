#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/9 10:58
# @Author  : WangLei
# @FileName: config.py
# @Software: PyCharm

import os
from datetime import timedelta
from flask_rabbitmq import RabbitMQ,Queue
import pymysql
from werkzeug.contrib.cache import SimpleCache
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from DBUtils.PooledDB import PooledDB
from src.until.mq_queue import queue
import pika
# 缓存配置
cache = SimpleCache()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 批量上传人脸保存路径
USER_PIC_DIR = "/static/user_user/"
PIC_DIR = BASE_DIR + USER_PIC_DIR


class Config:
    # 项目的bug模式
    DEBUG = True
    # session配置
    SECRET_KEY = os.urandom(24)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    # db

    HOST = '192.168.10.19'
    PORT = 3306
    USER = "root"
    PASSWORD = 'Cm~!@#2020$%^789'
    DBNAME = 'egc_sf'
    CHARSET = 'utf8mb4'

    # 日志等级
    LOG_INFO = DEBUG

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DBNAME}"
    # 调度器开关
    SCHEDULER_API_ENABLED = True
    # 持久化配置
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    # 配置rabbitmq连接配置
    RABBITMQ_HOST = '192.168.10.112'
    RABBITMQ_USERNAME = 'admin'
    RABBITMQ_PASSWORD = 'admin123'
    RABBITMQ_VHOST = '/sf_egc_dev'

    POOL = PooledDB(
        creator=pymysql,
        maxconnections=10,
        mincached=2,
        maxcached=5,
        maxshared=3,
        blocking=True,
        maxusage=None,
        setsession=[],
        ping=0,
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DBNAME,
        charset=CHARSET
    )



class Devlopment(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False


configs = {
    'dev': Devlopment(),
    'pro': Production()
}
