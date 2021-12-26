#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-08-30 14:25:06
# @LastEditTime: 2021-08-31 13:58:02
# @FilePath: /app/APScheduler/jobs/clear_expired_files_jobs.py
import os
import time

from application.tools.file_tools import FileTools
from application.initialization.application import logger


class ClearExpiredFileJobs(object):
    def __init__(self, *args, **kwargs):
        self.file_tools_ = FileTools()
        self._dirs_68 = [
            "/data/share_data/transform",
            "/data/share_data/table_parser",
            "/data/share_data/pdf2txt",
            "/data/share_data/node",
            "/data/table_parser/online_data/upload",
            "/data/pdf2txt/online_data/upload",
            "/data/pdf2txt/online_data/output",
        ]

    @property
    def dirs_68(self):
        return self._dirs_68

    def delete_files_by_dirs(self, dirs, start_day=None, end_day=None):
        if dirs and isinstance(dirs, list):
            [self.delete_old_files(dir_, start_day=start_day, end_day=end_day) for dir_ in dirs]

    def delete_old_files(self, del_files_path, start_day=None, end_day=None):
        need_del_files = self.file_tools_.find_all_file_by_times(del_files_path, start_day, end_day)
        self.file_tools_.del_files_by_list(need_del_files)
        self.file_tools_.del_none_file_dir(del_files_path)
        return need_del_files


clear_expired_file_jobs_ = ClearExpiredFileJobs()


def delete_old_files(start_day=None, end_day=5):
    clear_expired_file_jobs_.delete_files_by_dirs(clear_expired_file_jobs_.dirs_68, start_day=start_day,
                                                  end_day=end_day)
