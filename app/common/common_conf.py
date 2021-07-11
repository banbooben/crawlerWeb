#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-09-01 22:17:33
# @LastEditTime: 2020-09-01 22:17:59
# @Name    : common_conf.py
# @Desc    :


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
    host = var_data.get("REDIS_HOST", "127.0.0.1")
    port = var_data.get("REDIS_PORT", 6379)
    redis_password = var_data.get("REDIS_PASSWORD", "")
    database = var_data.get("REDIS_DB", 0)
    decode_responses = var_data.get("DECODE_RESPONSES", True)
    return {"host": host, "port": port, "db": database, "decode_responses": decode_responses,
            "password": redis_password, }
