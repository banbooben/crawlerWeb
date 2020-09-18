#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/8 18:29
# @Author  : shangyameng@aliyun.com
# @Site    : 
# @File    : my_log.py

import os
import sys
import time
import logging
import warnings
import pathlib

# LOGGING_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


class Logger(object):
    def __init__(self, set_level="INFO",
                 name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
                 log_name=time.strftime("%Y-%m-%d.log", time.localtime()),
                 log_path=(pathlib.Path().cwd()/"logs").absolute(),
                 use_console=True,
                 save_file=True):
        """
        Args:
            set_level: 日志级别["NOTSET"|"DEBUG"|"INFO"|"WARNING"|"ERROR"|"CRITICAL"]，默认为INFO
            name: 日志中打印的name，默认为运行程序的name
            log_name: 日志文件的名字，默认为当前时间（年-月-日.log）
            log_path: 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
            use_console: 是否在控制台打印，默认为True
            save_file: 日志是否保存到本地文件，默认为True
        """
        if not set_level:
            set_level = self._exec_type()  # 设置set_level为None，自动获取当前运行模式
        self.__logger = logging.getLogger(name)
        self.setLevel(
            getattr(logging, set_level.upper()) if hasattr(logging, set_level.upper()) else logging.INFO)  # 设置日志级别
        if not os.path.exists(log_path):  # 创建日志目录
            os.makedirs(log_path)
        formatter = logging.Formatter('%(asctime)s\t_%(levelname)s_\t%(filename)s\t_%(lineno)s_ >>>\t%(message)s')
        handler_list = list()
        if save_file:
            handler_list.append(logging.FileHandler(os.path.join(log_path, log_name), encoding="utf-8"))
        if use_console:
            handler_list.append(logging.StreamHandler())
        for handler in handler_list:
            handler.setFormatter(formatter)
            self.addHandler(handler)

    def __getattr__(self, item):
        return getattr(self.logger, item)

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, func):
        self.__logger = func

    @staticmethod
    def _exec_type():
        return "DEBUG" if os.environ.get("IPYTHONENABLE") else "INFO"

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(INFO):
            self._log(INFO, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(WARNING):
            self._log(WARNING, msg, args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        warnings.warn("The 'warn' method is deprecated, ""use 'warning' instead", DeprecationWarning, 2)
        self.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.error(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(CRITICAL):
            self._log(CRITICAL, msg, args, **kwargs)


# logger = Logger()
if __name__ == '__main__':
    # from pathlib import Path
    #
    # local_path = Path().cwd()
    # my_log_root = local_path.parent.parent / "logs"

    # res = my_log_root.absolute()
    # res = (pathlib.Path().cwd()/"logs").absolute()
    # res = os.system("pwd")
    # res = Logger(log_path=pathlib.Path().cwd().parent.parent / "logs")
    res = ""
    print(res)
