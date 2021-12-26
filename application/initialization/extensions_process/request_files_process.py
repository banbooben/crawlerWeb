#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/17 9:48 上午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : request_files_process.py
# @desc    :
import os
import time
# from functools import wraps
from pathlib import Path
import shutil

from flask import request

from application.common.decorators import Decorator
from application.config.server_conf import current_config

from application.initialization.application import logger

from application.initialization.error_process import FileException


class FlaskRequestFilesFunc(object):

    @classmethod
    @Decorator.time_func
    def save_file(cls) -> dict:
        all_files_path = {}
        files = request.files
        if not files:
            raise all_files_path
        logger.info(f"start check and save file")
        start_time = time.time()
        request_id = request.request_id
        save_file_dir = current_config.STATIC_FOLDER + f"/{request.blueprint}/{request_id}"
        Path(save_file_dir).mkdir(exist_ok=True)

        _ = [[
            cls()._save_single_file(all_files_path, file, file_key, ind, request_id, save_file_dir)
            for ind, file in enumerate(files.getlist(file_key))]
            for file_key in files]

        del _

        logger.info(f"end save file use {round(time.time() - start_time, 2)}s")
        return all_files_path

    def _save_single_file(self, all_files_path, file, file_key, ind, request_id, save_file_dir):
        """
        保存单个文件
        :param all_files_path:
        :param file:
        :param file_key:
        :param ind:
        :param request_id:
        :param save_file_dir:
        :return:
        """
        logger.info(f" {file_key}")
        current_file_save_path = save_file_dir + f"/{file_key}"
        Path(current_file_save_path).mkdir(exist_ok=True)
        # file = files[file_key]
        suffix = self._check_files(file, save_file_dir)
        new_file_name = request_id + f"_{file_key}_{ind}.{suffix}"
        logger.info(f"file info::: new_file: {new_file_name}")
        file_path = os.path.join(current_file_save_path, new_file_name)
        try:
            file.save(file_path)
            if file_key not in all_files_path:
                all_files_path.update({file_key: [{"file_path": file_path, "file_name": file.filename}]})
            else:
                all_files_path[file_key].append({"file_path": file_path, "file_name": file.filename})
        except Exception as e:
            logger.exception(e)
            shutil.rmtree(save_file_dir)
            raise FileException("The file cannot be saved", code="F004")

    # @classmethod
    def _check_files(self, file, save_file_dir):
        """
        检查上传的文件
        Args:
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
            raise FileException(code="F003")

        return suffix

    # def before_request_save_files(self, func):
    #     @wraps(func)
    #     def _wrap(*args, **kwargs):
    #         files_dict = self.save_file()
    #         request.files = files_dict
    #         rst = func(*args, **kwargs)
    #         return rst
    #
    #     return _wrap
