#!/usr/bin/env python

# coding:utf-8
# @Time    : 2020/12/27 0:47
# @Contact : shangyameng@aliyun.com
# @Name    : common_functions.py
# @Desc    :

import base64
import hashlib
import json

from uuid import uuid4

from application.initialization.error_process import TypeException


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


def base64encode(_str: str):
    try:
        return base64.b64encode(_str.encode()).decode()
    except Exception as e:
        raise TypeException(e, code="T002")


def base64decode(_str: str):
    try:
        return base64.b64decode(_str.encode()).decode()
    except Exception as e:
        raise TypeException(e, code="T003")


def get_hash_digest(need_hash_info):
    return hashlib.sha256(json.dumps(need_hash_info, sort_keys=True).encode("utf-8")).hexdigest()


def format_dict_none_value(dict_info: dict):
    for key, value in dict_info.items():
        if value is None:
            dict_info.update({key: ''})
        elif key == "working":
            if isinstance(value, str) and ("在职" in value or "聘用" in value or "待入职" in value):
                dict_info.update({key: True})
            elif value in ["True", "true", "1", 1, True]:
                dict_info.update({key: True})
            elif isinstance(value, str) and "离职" in value:
                dict_info.update({key: False})
            elif value in ["False", "false", "0", 0, False]:
                dict_info.update({key: False})
            else:
                dict_info.update({key: False})
        #     dict_info.update({key: False})
        # if value in ["True", "true", "1", 1, True]:
        #     return True
        # elif value in ["False", "false", "0", 0, False]:
        #     return False
        # elif isinstance(value, str) and ("在职" in value or "聘用" in value):
        #     return True
        # elif isinstance(value, str) and "离职" in value:
        #     return False
    return dict_info


def dict_reset(dict_info: list, key: str, reverse=False):
    if dict_info and key:
        dict_info = sorted(dict_info, key=lambda x: x[key], reverse=reverse)
    return dict_info


def obj_add_request_id(obj_item, class_name=Exception):
    from flask import request

    if isinstance(obj_item, class_name):
        obj_item.__setattr__("request_id", request.request_id)
    return obj_item


if __name__ == '__main__':
    # url_s = "http://www.baidu.com"
    url_s = "http://127.0.0.1:5000"
    # sss = common_request(url_s)
    a = ""
