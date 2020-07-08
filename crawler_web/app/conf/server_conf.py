#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-05-29 14:15:17
# @FilePath: /crawlerWeb/crawler_web/app/conf/server_conf.py

import random
import os

current_environment = "testing"


def get_databases_url(var_data):
    """
    根据传入的环境获取不同环境的配置参数
    :param var_data: 配置的环境
    :return:
    """
    USER = var_data.get('USER', 'root')
    PASSWORD = var_data.get('PASSWORD', 'shang.666')
    HOST = var_data.get('HOST', '127.0.0.1')
    PORT = var_data.get('PORT', '33061')
    DATABASE = var_data.get('DATABASE', 'crawler')

    return 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USER, PASSWORD, HOST, PORT,
                                                   DATABASE)


def get_mysql_info(var_data):
    """
    根据传入的环境配置获取不同环境的配置参数
    :param var_data: 配置的环境
    :return:
    """
    USER = var_data.get('USER', 'root')
    PASSWORD = var_data.get('PASSWORD', 'shang.666')
    HOST = var_data.get('HOST', '127.0.0.1')
    PORT = var_data.get('PORT', '33061')
    DATABASE = var_data.get('DATABASE', 'crawler')

    return USER, PASSWORD, HOST, PORT, DATABASE


def get_redis_config(var_data):
    host = var_data.CACHE_REDIS_HOST
    port = var_data.CACHE_REDIS_PORT
    database = var_data.CACHE_REDIS_DB
    decode_responses = var_data.DECODE_RESPONSES
    redis_password = var_data.CACHE_REDIS_PASSWORD
    cache_type = var_data.CACHE_TYPE
    return host, port, database, decode_responses, redis_password, cache_type


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

    # 缓存
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 1
    CACHE_REDIS_PASSWORD = 123456
    CACHE_DEFAULT_TIMEOUT = 1800

    # token有效期
    TOKEN_LIFETIME = 1800

    # 路由白名单
    URL_WHITE_LIST = {
        '/': ['GET'],
        '/api/seed/': ['GET', 'POST'],
        '/auth/': ['POST'],
        '/api/aria/': ['GET'],
        '/api/test/': ['GET', "POST"]
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
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 63791
    CACHE_REDIS_DB = 1
    DECODE_RESPONSES = True
    CACHE_REDIS_PASSWORD = 123456
    SQLALCHEMY_DATABASE_URI = get_databases_url(DATABASES)


# 测试环境配置
class TestingConfig(Config):
    DATABASES = {
        'USER': 'root',
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'shang.666'),
        'HOST': '127.0.0.1',
        'PORT': '33061',
        'DATABASES': 'crawler'
    }

    # 缓存
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 63791
    CACHE_REDIS_DB = 1
    DECODE_RESPONSES = True
    CACHE_REDIS_PASSWORD = 123456
    # decode_responses = True
    SQLALCHEMY_DATABASE_URI = get_databases_url(DATABASES)


config = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    # 默认环境
    'default': DevelopConfig
}

current_config = config[current_environment]

# if __name__ == "__main__":
#     current_environment = "default"
#     res = get_mysql_info(config[current_environment].DATABASES)
#     print(res)
