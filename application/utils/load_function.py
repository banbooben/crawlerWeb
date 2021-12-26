#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 7:45 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : load_function.py
# @desc    :

import importlib
from application.initialization.application import logger


def load_function(file_path, func):
    module = importlib.import_module(file_path.replace("/", ".").rsplit(".", 1)[0])
    importlib.reload(module)
    try:
        func = getattr(module, func)
        return func
    except Exception as e:
        logger.exception(e)
        return None





if __name__ == '__main__':
    abs_file_path = "APScheduler/jobs"
    func = load_function(abs_file_path, "test_job_")
    a = ""
