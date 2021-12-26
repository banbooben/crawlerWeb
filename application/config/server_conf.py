#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2021-11-01 20:47:18
# @FilePath: /smfg_api/flask_app/config/server_conf.py

import os
import random
# from flask_app.common.common_conf import get_databases_url
from pathlib import Path
import multiprocessing


class BaseConfig(object):
    # app基础配置
    # 密钥
    PROJECT_NAME = "flask_app"
    SECRET_KEY = ''.join(
        random.sample('zyxwvutsrqponmlkjihgfedcba!@#$%^&*', 32)).encode()

    # 服务运行端口绑定
    # BIND = os.getenv("BIND", "0.0.0.0:5000")
    WORK_NUMS = os.getenv("WORK_NUMS", multiprocessing.cpu_count())

    # app静态资源路径
    TEMPLATE_FOLDER = Path('/flask_app/templates').as_posix()
    STATIC_FOLDER = Path('/flask_app/static').as_posix()
    # STATIC_URL_PATH = '/'

    # 日志配置存储位置
    LOG_DIR = (Path.cwd() / 'logs').as_posix()
    LOG_LEVEL = "INFO"
    LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", 'root.log')

    # 上传文件存储位置
    # UPLOAD_PATH = (Path.cwd() / 'flask_app/static').as_posix()
    # UPLOAD_PATH = Path('/flask_app/static').as_posix()
    # 上传文件允许格式
    ALLOWED_EXTENSIONS = tuple(["pdf", "PDF", "doc", "docx", "txt"])

    JWT_URL_WHITE_LIST = {
        ('/', 'GET'),
    }


# 配置基类
class Config(BaseConfig):
    # 是否使用链接池
    USE_DB_POOL = True
    """ Flask-JWT配置 """
    SSO_LOGIGN = os.getenv('SSO_LOGIGN', True)  # 是否支持单点登录 True:支持，False:不支持
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES',
                                         60 * 60 * 24)
    LOGIN_KEY = os.getenv('LOGIN_KEY', "lk_")
    TOKEN_LIFETIME = 1800  # token有效期

    # 数据库的配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 配置自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否显示错误信息
    SQLALCHEMY_ECHO = False  # 调试模式显示错误信息
    SQLALCHEMY_POOL_SIZE = 20  # 链接池数量
    SQLALCHEMY_POOL_MAX_OVERFLOW = 5  # 超出后，可以创建的链接数
    SQLALCHEMY_POOL_PRE_PING = True  # 每次取出一个连接时，会发送一个select 1来检查连接是否有效
    SQLALCHEMY_POOL_TIMEOUT = 30  # 链接超时时间
    SQLALCHEMY_POOL_RECYCLE = os.getenv("SQLALCHEMY_POOL_RECYCLE", 8 * 60)  # 表示连接在给定时间之后会被回收，不能超过8小时

    MAX_PAGE_SIZE = 1000000

    # 数据库基础配置
    DATABASES_USER = os.getenv('MYSQL_PASSWORD', 'root')
    DATABASES_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    DATABASES_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    DATABASES_PORT = os.getenv('MYSQL_PORT', 212330690)
    DATABASES_DATABASES = os.getenv('MYSQL_DATABASES', "smbc")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASES_USER}:{DATABASES_PASSWORD}@{DATABASES_HOST}:{DATABASES_PORT}/{DATABASES_DATABASES}'

    REDIS_CONF = {
        "CACHE_TYPE": os.getenv('CACHE_TYPE', 'redis'),
        "REDIS_HOST": os.getenv('REDIS_HOST', 'redis'),
        "REDIS_PORT": os.getenv('REDIS_PORT', 6379),
        "REDIS_DB": os.getenv('REDIS_DB', 3),
        "REDIS_PASSWORD": os.getenv('REDIS_PASSWORD', ''),
        "DECODE_RESPONSES": os.getenv('DECODE_RESPONSES', "True"),
    }

    SQLALCHEMY_BINDS = {
        'base': SQLALCHEMY_DATABASE_URI,
    }


# 生产环境配置
class ProductConfig(Config):
    LOG_LEVEL = "INFO"

    # IDPS_HOST = os.getenv('IDPS_HOST', 'http://web_api')
    # IDPS_PORT = os.getenv('IDPS_PORT', '10001')
    #
    # LDAP_URL = os.getenv('LDAP_URL', 'ldap://ad-idc.bdo.com.cn:389')
    # LDAP_AUTHENTICATION = os.getenv('LDAP_AUTHENTICATION', 'simple')
    # LDAP_BASE_DN = os.getenv('LDAP_BASE_DN', 'dc=bdo,dc=com,dc=cn')
    # LDAP_CREDENTIALS = os.getenv('LDAP_CREDENTIALS', 'idSecure.2012')


# 测试环境配置
class TestConfig(Config):
    # 日志等级设置
    LOG_LEVEL = "DEBUG"

    # IDPS_HOST = os.getenv('IDPS_HOST', 'http://idps2-sp.datagrand.cn')
    # IDPS_PORT = os.getenv('IDPS_PORT', '80')

    # LDAP_URL = os.getenv('LDAP_URL', 'ldap://100.100.20.13:389')
    # LDAP_AUTHENTICATION = os.getenv('LDAP_AUTHENTICATION', 'simple')
    # LDAP_BASE_DN = os.getenv('LDAP_BASE_DN', 'dc=sarmn,dc=cn')
    # LDAP_CREDENTIALS = os.getenv('LDAP_CREDENTIALS', 'idSecure.2012')


# 本地环境配置
class LocalConfig(Config):
    DATABASES_USER = os.getenv('MYSQL_PASSWORD', 'root')
    DATABASES_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    DATABASES_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    DATABASES_PORT = os.getenv('MYSQL_PORT', 21290)
    # DATABASES_HOST = os.getenv('MYSQL_HOST', '100.100.21.220')
    # DATABASES_PORT = os.getenv('MYSQL_PORT', 33061)
    DATABASES_DATABASES = os.getenv('MYSQL_DATABASES', "smbc")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASES_USER}:{DATABASES_PASSWORD}@{DATABASES_HOST}:{DATABASES_PORT}/{DATABASES_DATABASES}'

    # 缓存
    REDIS_CONF = {
        "CACHE_TYPE": os.getenv('CACHE_TYPE', 'redis'),
        "REDIS_HOST": os.getenv('REDIS_HOST', '100.100.21.220'),
        "REDIS_PORT": os.getenv('REDIS_PORT', 63791),
        "REDIS_DB": os.getenv('REDIS_DB', 3),
        "REDIS_PASSWORD": os.getenv('REDIS_PASSWORD', '123456'),
        "DECODE_RESPONSES": os.getenv('DECODE_RESPONSES', "True"),
    }

    TEMPLATE_FOLDER = (Path.cwd() / 'static/').as_posix()
    STATIC_FOLDER = (Path.cwd() / 'static/').as_posix()

    # 日志等级设置
    LOG_LEVEL = "DEBUG"


config = {
    'default': LocalConfig,
    'test': TestConfig,
    'product': ProductConfig,
    "base": BaseConfig
}

# global current_config
current_environment = os.getenv("ENV", "default")
current_config = config.get(current_environment)
