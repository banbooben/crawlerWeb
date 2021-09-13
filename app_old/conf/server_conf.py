#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-09-01 22:41:33
# @FilePath: /crawlerWeb/crawler_web/conf/server_conf.py

import random
import os
from .common_conf import get_databases_url, get_mysql_info, get_redis_config


# 配置基类
class Config(object):
    """
    配置基类
    """
    # 密钥
    SECRET_KEY = 'aliksuydgi/ekjh$gawel;isvnurio'

    # 数据库的配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 配置自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否显示错误信息
    SQLALCHEMY_ECHO = True  # 调试模式显示错误信息

    # token有效期
    TOKEN_LIFETIME = 1800

    # 路由白名单
    URL_WHITE_LIST = {
        '/': ['GET'],
    }

    # 通知邮箱配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'armn_s@163.com'
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'Sym0618Zyf')


# 环境配置
class DevelopConfig(Config):
    DATABASES = {
        'USER': 'root',
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'shang.666'),
        'HOST': '127.0.0.1',
        'PORT': '33061',
        'DATABASES': 'crawler'
    }

    # 缓存
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '100.100.21.123'
    CACHE_REDIS_PORT = 63791
    CACHE_REDIS_DB = 0
    DECODE_RESPONSES = True
    CACHE_REDIS_PASSWORD = 123456
    # decode_responses = True
    SQLALCHEMY_DATABASE_URI = get_databases_url(DATABASES)

    # 路由白名单
    URL_WHITE_LIST = {
        '/': ['GET'],
        '/123': ['GET'],
        '/api/seed/': ['GET', 'POST'],
        '/auth/': ['POST'],
        '/api/aria/': ['GET'],
        '/aria/': ['GET'],
        '/api/test/': ['GET', "POST"]
    }


current_environment = "default"
config = {'default': DevelopConfig}

current_config = config[current_environment]
