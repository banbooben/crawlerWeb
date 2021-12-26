#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/26 10:59 上午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : application_conf.py.py
# @desc    :
import os


class ApplicationConfig(object):
    ...


class TestConfig(ApplicationConfig):
    ...


class ProductConfig(ApplicationConfig):
    ...


config = {
    'default': ApplicationConfig,
    'test': TestConfig,
    'product': ProductConfig,
}

# global current_config
current_environment = os.getenv("ENV", "default")
current_application_config = config.get(current_environment)
