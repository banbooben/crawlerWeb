#!/usr/bin/env python

# coding:utf-8
# @Time    : 2020/12/27 0:47
# @Contact : shangyameng@aliyun.com
# @Name    : common_functions.py
# @Desc    :

from uuid import uuid4
# from initialization.application import logger


def format_result_to_logger_str(result):
    logger_result = "\n"
    if isinstance(result, dict):
        for key, value in result.items():
            logger_result += f"\t{key}:\t{repr(value)[:150]}\n"
    elif isinstance(result, list):
        for value in result:
            logger_result += f"\t{repr(value)[:150]}\n"
    elif isinstance(result, tuple):
        for value in result:
            logger_result += f"\t{repr(value)[:150]}\n"
    else:
        logger_result += repr(result)[:200]
    return logger_result


def get_uuid():
    return str(uuid4())


if __name__ == '__main__':
    # url_s = "http://www.baidu.com"
    url_s = "http://127.0.0.1:5000"
    # sss = common_request(url_s)
    a = ""
