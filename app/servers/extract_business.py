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
from lxml import etree

from initialization.error_process import ExtractException
from common.common_functions import (format_result_to_logger_str,
                                     common_request_to_json as common_request)


class ExtractApiBusiness(object):
    ...
