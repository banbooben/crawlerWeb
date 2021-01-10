#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-09-01 22:17:33
# @LastEditTime: 2020-09-01 22:17:59
# @FilePath: /crawlerWeb/crawler_web/conf/common_conf.py


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
    return {"host": host, "port": port, "db": database, "decode_responses": decode_responses,
            "password": redis_password, }
