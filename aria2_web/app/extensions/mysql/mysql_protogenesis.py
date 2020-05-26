#!/usr/local/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-12 15:46:25
# @LastEditTime: 2020-04-12 15:48:18
# @FilePath: /aria2_web/app/extensions/extensions_log.py

import pymysql.cursors
from app.common.decorators import Singleton, time_func
from app.extensions import logger
from app.conf.server_conf import HTTP_PORT, HTTP_HOST, current_environment, config


@Singleton
class PyMysql(object):
    def __init__(self, host, port, user, password, db, charset="utf8mb4"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = self.charset
        self.cursorclass = pymysql.cursors.DictCursor

    @time_func
    def connectAndGetCursor(self):
        """
        创建连接并初始化游标
        :return: 
        """
        try:
            with pymysql.connect(host=self.host,
                                 port=self.port,
                                 user=self.user,
                                 password=self.password,
                                 db=self.db,
                                 charset=self.charset) as connection:
                with connection.cursor() as cursor:
                    return connection, cursor
        except Exception as e:
            logger.error(e)
            return None

    @time_func
    def executeByInsOrUpdOrDel(self, connection, cursor, sql: str, values):
        """
        执行单个sql语句
        :param connection: 数据库连接对象
        :param cursor: mysql游标
        :param sql: 要执行的sql语句
        :param values: 需要插入的数据
        :return: 
        """
        try:
            if isinstance(values, tuple):
                cursor.execute(sql, values)
            elif isinstance(values, list):
                cursor.executemany(sql, values)
            connection.commit()
            res = cursor.fetchone()
            logger.info("操作成功")
            logger.info("执行结果：{}".format(res))
        except Exception as e:
            logger.error("操作失败：{}".format(e))
            connection.roback()

    @time_func
    def executeByInsOrUpdOrDel(self, connection, cursor, sql: str, values):
        pass

    # @time_func
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
