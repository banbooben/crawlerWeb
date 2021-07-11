#!/usr/bin/env python

# coding:utf-8
# @Time    : 2020/12/27 0:47
# @Contact : shangyameng@aliyun.com
# @Name    : common_functions.py
# @Desc    :

from uuid import uuid4
# from initialization.application import logger
import os
import json
import requests
from requests import request
from tenacity import (retry, retry_if_exception_type,
                      retry_if_result, stop_after_attempt,
                      wait_random,
                      RetryError)


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
    uuid = str(uuid4()).replace("-", "")
    return uuid


def value_is_none(value):
    return value is None


@retry(retry=(retry_if_result(value_is_none)),
       wait=wait_random(min=0, max=3),
       stop=stop_after_attempt(6),
       reraise=True)
def common_request(url, method="GET", **kwargs):
    """
    request请求，
    如果请求返回的数据为None，重复请求6次，直到获取到数据，否侧报错抛出
    Args:
        url:
        method:
        **kwargs:

    Returns:

    """
    send_review_request = request(method=method, url=url, **kwargs)
    if send_review_request.status_code == 401:
        return "{}"
        # return common_request(url=url, method=method, *args, **kwargs)
    else:
        result = send_review_request.content.decode("utf-8") if send_review_request is not None else None
        return result
        # return None


@retry(retry=retry_if_exception_type(json.JSONDecodeError),
       stop=stop_after_attempt(3),
       reraise=True)
def common_request_to_json(url, method="GET", **kwargs):
    """
    请求到的数据，转换为json格式
    Args:
        url:
        method:
        **kwargs:

    Returns:

    """
    try:
        response_str = common_request(url, method, **kwargs)
    except Exception as e:
        if isinstance(e, RetryError):
            response_str = None
        response_str = "{}"
    res = json.loads(response_str)
    return res


if __name__ == '__main__':
    # url_s = "http://www.baidu.com"
    url_s = "http://127.0.0.1:5000"
    # sss = common_request(url_s)
    sss = common_request_to_json(url_s)
    a = ""
