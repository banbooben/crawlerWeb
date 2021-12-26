# !/usr/bin/env python
# coding:utf-8
# @Time    : 2021/10/13 15:51
# @Contact : shangyameng@datagrand.com
# @Name    : bdo_base_server.py
# @Desc    :
import os
import random
import re
from datetime import datetime
from pathlib import Path

from application.common.common_functions import base64encode, base64decode
from application.config.server_conf import current_config
from application.extensions.idps_tools.idps_api import IdpsTools
from application.initialization.logger_process import logger

from application.initialization.error_process import ModelException, APIException, FileException, IdpsException
from application.tools.pdf_tools import PdfTools
from application.tools.requests_tools import request_tools_


class BaseServer(object):

    def __init__(self):
        self.idps_tools_ = IdpsTools(host=current_config.IDPS_HOST,
                                     port=current_config.IDPS_PORT)
        self.pdf_tools_ = PdfTools()
        self.request_tools_ = request_tools_
