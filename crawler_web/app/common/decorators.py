#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Project : crawler_web
# @File    : decorators.py
# @Author  : shangyameng@datagrand.com
# @Time    : 2020/5/23 22:50
# @desc:

import threading
import time
from functools import wraps
from flask import current_app
from app.application import logger

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


def Singleton(cls):
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
