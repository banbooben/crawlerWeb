#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/17 9:48 上午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : flask_request_files_process.py
# @desc    :
import os
import time
from functools import wraps
from pathlib import Path
import shutil

from flask import request

from common.decorators import Decorator
from config.server_conf import current_config

from initialization.application import logger

from initialization.base_error_process import FileException


class FlaskRequestFilesFunc(object):

    @Decorator.time_func
    def save_file(self) -> dict:
        all_files_path = {}
        files = request.files
        if not files:
            raise FileException(code="F001")
        logger.info(f"start check and save file")
        start_time = time.time()
        request_id = request.request_id
        save_file_dir = current_config.UPLOAD_PATH + f"/{request_id}"
        Path(save_file_dir).mkdir(exist_ok=True)

        for file_key in files:
            logger.info(f" {file_key}")
            current_file_save_path = save_file_dir + f"/{file_key}"
            Path(current_file_save_path).mkdir(exist_ok=True)

            file = files[file_key]
            suffix = self._check_files(file, save_file_dir)
            new_file_name = request_id + f"_{file_key}.{suffix}"
            logger.info(f"file info::: new_file: {new_file_name}")
            file_path = os.path.join(current_file_save_path, new_file_name)
            try:
                file.save(file_path)
                all_files_path.update({
                    file: {"new_file": file_path}
                })
            except Exception as e:
                logger.exception(e)
                shutil.rmtree(save_file_dir)
                raise FileException("The file cannot be saved", code="F004")

        logger.info(f"end save file use {round(time.time() - start_time, 2)}s")
        return all_files_path

    # @classmethod
    def _check_files(self, file, save_file_dir):
        """
        检查上传的文件
        Args:
            file_key:
            file:
            save_file_dir:

        Returns:

        """
        if not file:
            shutil.rmtree(save_file_dir)
            raise FileException("没有获取到文件", code="F002")
        suffix = file.filename.rsplit(".", 1)[-1]

        if suffix.lower() not in current_config.ALLOWED_EXTENSIONS:
            shutil.rmtree(save_file_dir)
            raise FileException("上传文件中含有错误类型", code="F003")

        return suffix

    # @classmethod
    def decorator_save_files(self, func):
        @wraps(func)
        def _wrap(*args, **kwargs):
            files_dict = self.save_file()
            request.files = files_dict
            rst = func(*args, **kwargs)
            return rst

        return _wrap
