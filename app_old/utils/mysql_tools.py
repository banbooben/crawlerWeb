#!/usr/bin/env python

# coding:utf-8
# @Time    : 2020/12/27 0:47
# @Contact : shangyameng@aliyun.com
# @Name    : mysql_tools.py
# @Desc    :


import pymysql.cursors
from common.decorators import singleton, Decorator
from initialization.logger_process import logger


@singleton
class PyMysql(object):
    def __init__(self, host, port, user, password, db, charset="utf8mb4"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self._connect_and_get_cursor()
        self.connection, self.cursor = None, None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    @Decorator.time_func
    def _connect_and_get_cursor(self):
        """
        创建连接并初始化游标
        :return:
        """
        try:
            connection = pymysql.connect(host=self.host,
                                         port=self.port,
                                         user=self.user,
                                         password=self.password,
                                         db=self.db,
                                         charset=self.charset)
            cursor = connection.cursor()
            self.connection, self.cursor = connection, cursor
        except Exception as e:
            logger.exception(e)
            return "None", "None"

    @Decorator.time_func
    def _execute_by_select(self,
                           sql: str):
        """
        执行单个sql语句
        :param sql: 要执行的sql语句
        :return:
        """
        try:

            res = []
            if self.cursor and sql:
                self.cursor.execute(sql)
                res = self.cursor.fetchall()
            self.connection.commit()
            return res
        except Exception as e:
            logger.exception(e)
            return []

    def close(self):
        try:
            # if self.connection.ping():
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            logger.exception(e)
