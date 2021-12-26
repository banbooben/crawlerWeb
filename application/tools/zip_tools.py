#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/1 3:47 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : zip_tools.py
# @desc    :

import zipfile
from pathlib import Path
from application.initialization.logger_process import logger


class ZipFileTools(object):

    def __init__(self):
        self._zip_item = None

    def create(self, filename, flag="w"):
        self._zip_item = zipfile.ZipFile(f'{filename}', flag, zipfile.ZIP_DEFLATED)

    def add_file_or_file_path(self, file_path: str):
        if file_path and Path(file_path).exists():
            self._zip_item.write(file_path)

    def add_files(self, files_list):
        for file_path in files_list:
            self.add_file_or_file_path(file_path)
        a = ""

    def write(self):
        self._zip_item.close()
        self._zip_item = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.write()


zip_tools_ = ZipFileTools()
# def zip_file(file_name, path):
#     zip_ = zipfile.ZipFile(f'{file_name}.zip', 'w', zipfile.ZIP_DEFLATED)
#     # 把zfile整个目录下所有内容，压缩为new.zip文件
#     zip_.write(path)
#     # 把c.txt文件压缩成一个压缩文件
#     # zip_file.write('c.txt',compress_type=zipfile.ZIP_DEFLATED)
#     zip_.close()


if __name__ == '__main__':
    path = "/Users/sarmn/work_speace/smfg/smfg_api/flask_app/app.py"
    path2 = "/Users/sarmn/work_speace/smfg/smfg_api/flask_app/tools/mysql_tools.py"
    file_name_name = "./tests"
    zp = ZipFileTools()
    zp.create(file_name_name)
    zp.add_files([path, path2])
    zp.write()
