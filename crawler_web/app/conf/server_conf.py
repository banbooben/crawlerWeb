#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-05-29 14:15:17
# @FilePath: /crawlerWeb/crawler_web/app/conf/server_conf.py

import random
import os

# http conf
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 9527
aria_host = "127.0.0.1"
aria_port = "6800"
aria_token = "test"

# 0mag.net请求地址
zeroMagUrl = 'https://0mag.net/search'

# 电影天堂请求地址
dyttUrl = 'https://www.dy2018.com'

# 西刺代理请求地址
proxyUrl = {
    "高匿": "https://www.xicidaili.com/nn/4052",
    # "普通": "https://www.xicidaili.com/nt/",
    # "qq": "https://www.xicidaili.com/qq"
}
# 西刺代理地址拼接头
proxyUrlFront = "https://www.xicidaili.com/"


def get_databases_url(var_data):
    """
    根据传入的环境获取不同环境的配置参数
    :param var_data: 配置的环境
    :return:
    """
    USER = var_data.get('USER', 'root')
    PASSWORD = var_data.get('PASSWORD', 'shang.666')
    HOST = var_data.get('HOST', '127.0.0.1')
    PORT = var_data.get('PORT', '3306')
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
    PORT = var_data.get('PORT', '3306')
    DATABASE = var_data.get('DATABASE', 'crawler')

    return USER, PASSWORD, HOST, PORT, DATABASE


# 配置基类
class Config(object):
    """
    配置基类
    """
    # 密钥
    SECRET_KEY = '123456'

    # 数据库的配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 配置自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否显示错误信息
    SQLALCHEMY_ECHO = True  # 调试模式显示错误信息

    # 缓存
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 1

    # token有效期
    TOKEN_LIFETIME = 1800

    # 路由白名单
    URL_WHITE_LIST = {
        '/': ['GET'],
        '/api/seed/': ['GET', 'POST'],
        '/auth/': ['POST']
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
        'PORT': '3306',
        'DATABASES': 'crawler'
    }
    SQLALCHEMY_DATABASE_URI = get_databases_url(DATABASES)


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'TESTING'


# 生产环境配置
class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'PRODUCT'


config = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'product': ProductConfig,
    # 默认环境
    'default': DevelopConfig
}

current_environment = "default"
