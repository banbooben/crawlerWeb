#!/usr/local/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-12 15:46:25
# @LastEditTime: 2020-04-12 15:48:18
# @FilePath: /crawler_web/app/extensions/extensions_log.py

import pymysql.cursors
from common.decorators import singleton, Decorator
from conf.myLog import logger


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
        # self.cursorclass = pymysql.cursors.DictCursor
        # self.connection, self.cursor = self._connectAndGetCursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
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
            logger.error(e)
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
            print(e)
            return []

    def close(self):
        try:
            if self.connection.ping():
                self.cursor.close()
                self.connection.close()
        except Exception as e:
            print(e)

    # @Decorator.time_func
    # def executeBySelect(self, connection, cursor, sql: str):
    #     try:
    #
    #         res = []
    #         if connection and cursor and sql:
    #             cursor.execute(sql)
    #             res = cursor.fetchall()
    #             logger.info("操作成功")
    #             logger.info("执行结果：{}".format(res))
    #             return res
    #         logger.info("缺少关键参数")
    #         return res
    #     except Exception as e:
    #         logger.error(e)
    #         return []

    # @Decorator.time_func
    # def executemanyByInsertOrUpdate(self, connection, cursor, sql: str,
    #                                 args: list):
    #     """
    #     执行单个sql语句
    #     :param connection: 数据库连接对象
    #     :param cursor: mysql游标
    #     :param sql: 要执行的sql语句
    #     :param args: 需要插入的数据
    #     :return:
    #     """
    #     try:
    #         cursor.executemany(sql, args)
    #         connection.commit()
    #     except Exception as e:
    #         logger.error(e)
    #         connection.roback()
