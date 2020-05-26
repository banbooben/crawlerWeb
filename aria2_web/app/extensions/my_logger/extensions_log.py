#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-12 15:46:25
# @LastEditTime: 2020-04-12 15:48:18
# @FilePath: /aria2_web/app/extensions/extensions_log.py
import os
import time
import logging


# log配置，实现日志自动按日期生成日志文件
def make_dir(make_dir_path):
    """
    文件生成
    :param make_dir_path:
    :return:
    """
    path = make_dir_path.strip()
    if not os.path.exists(path):
        os.makedirs(path)
    return path


log_dir_name = "logs"  # 创建文件夹名字
log_file_name = 'logger-' + time.strftime(
    '%Y-%m-%d', time.localtime(time.time())) + '.log'  # 创建日志文件
log_file_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir,
                 os.pardir)) + os.sep + log_dir_name  # 日志保存目录
make_dir(log_file_folder)
log_file_str = log_file_folder + os.sep + log_file_name

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file_str, encoding='UTF-8')  # 创建日志对象
handler.setLevel(logging.DEBUG)  # 设置日志等级（ERROR、WARN、INFO、DEBUG）
logging_format = logging.Formatter(
    '%(asctime)s -%(levelname)s- %(filename)s -%(lineno)s- %(message)s'
)  # 日志显示格式
handler.setFormatter(logging_format)
