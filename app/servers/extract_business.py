#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/16 16:52
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    : 
# @File    : extract_process.py
# @desc    :


from pathlib import Path
import os
import shutil
import json
import re
import time
# from lxml import etree

from initialization.base_error_process import ExtractException
from initialization.application import logger
from tools.requests_tools import request_tools_


class ExtractApiBusiness(object):

    def get_business(self):
        i = 0
        while i < 20:
            logger.info("celery test info")
            i += 1

    ...
