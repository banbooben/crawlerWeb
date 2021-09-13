#!/usr/bin/env python

# coding:utf-8
# @Time    : 2020/12/27 0:47
# @Contact : shangyameng@aliyun.com
# @Name    : decorators.py
# @Desc    :

import threading
import time
from functools import wraps
from initialization.logger_process import logger


# from .common_func import serialize, deserialization


# def Singleton(cls):
#     """
#     单例模式
#     """
#     instance = None
#
#     @synchronized
#     def __new__(cls, *args, **kwargs):
#         if cls.instance is None:
#             cls.instance = object.__new__(cls, *args, **kwargs)
#         return cls.instance


def singleton(cls):
    """
    类装饰器，实现基于线程安全的单例模式
    :param cls:
    :return:
    """

    def synchronized(func):
        """
        函数装饰器，实现给予线程安全
        配合实现
        """
        func.__lock__ = threading.Lock()

        def lock_func(*args, **kwargs):
            with func.__lock__:
                return func(*args, **kwargs)

        return lock_func

    _instance = {}

    @synchronized
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


class Decorator(object):
    @classmethod
    def time_func(cls, func):
        @wraps(func)
        def _wrap(*args, **kwargs):
            st = time.time()
            rst = func(*args, **kwargs)
            et = time.time()
            output_str = "func: '{}' time: {}s".format(func.__name__, et - st)
            logger.info(output_str)
            return rst

        return _wrap

    # @classmethod
    # def save_file(cls, func):
    #     @wraps(func)
    #     def _wrap(*args, **kwargs):
    #         from flask import request
    #         from config.server_conf import current_config
    #
    #         for item in request.files:
    #             item = request.files[item]
    #             fine_name = item.filename
    #
    #         res = func(*args, **kwargs)
    #         return res
    #
    #     return _wrap

    # @classmethod
    # def serializes(cls, func):
    #     def serialize(item):
    #         result = {}
    #         keys = [key for key in dir(item) if not key.startswith("__")]
    #         for key in keys:
    #             result[key] = eval(f"""item.{repr(key).strip("'")}""")
    #         return repr(result)
    #
    #     @wraps(func)
    #     def _wrap(*args, **kwargs):
    #         new_args = []
    #         item = serialize(*args, **kwargs)
    #         new_args.extend(args)
    #         new_args.append(item)
    #         args = tuple(new_args)
    #         rst = func(*args, **kwargs)
    #         return rst
    #
    #     return _wrap
    #
    # @classmethod
    # def deserializes(cls, func):
    #     def deserialization(item, result, *args, **kwargs):
    #         obj = item(*args, **kwargs)
    #         keys = [key for key in dir(item(*args, **kwargs)) if not key.startswith("__")]
    #         key_value = eval(result)
    #         for key in keys:
    #             value = key_value.get(key, None)
    #             if value:
    #                 setattr(obj, key, value)
    #         return obj
    #
    #     @wraps(func)
    #     def _wrap(*args, **kwargs):
    #         new_args = []
    #         var_item = deserialization(*args, **kwargs)
    #         new_args.extend(args)
    #         new_args.append(var_item)
    #         args = tuple(new_args)
    #         rst = func(*args, **kwargs)
    #         return rst
    #
    #     return _wrap
#
#
# @Decorator.serializes
# def get_item_info(item, *args, **kwargs):
#     print(item)
#     return item
#
#
# @Decorator.deserializes
# def get_obj_by_str(item, *args, **kwargs):
#     print(item)
#     print(args)
#     return item
#
#
# class HtmlItem(object):
#
#     def __init__(self, a):
#         self.url = "url"
#         self.type = "0"
#         self.a = a
#
#
# if __name__ == '__main__':
#     test = HtmlItem("123")
#     res = get_item_info(test)
#     res = get_obj_by_str(HtmlItem, "{'type': '0', 'url': 'test', 'a':123123}", a="aaa")
#     print(res)
#     # serialize(test)
#     # deserialization(HtmlItem, "{'type': '0', 'url': 'test', 'a':123123}", a="aaa")
