#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Project : crawlerWeb
# @File    : testApi.py
# @Author  : shangyameng@datagrand.com
# @Time    : 2020/5/26 14:47
# @desc:

import json
import re
import pickle
from flask import request
from flask_restful import Resource

from extensions import cache
from conf.myLog import logger
from common.common_func import serialize

# USER, PASSWORD, HOST, PORT, DATABASE = get_mysql_info(current_environment)

USER, PASSWORD, HOST, PORT, DATABASE = "root", "root", "127.0.0.1", 16153, "contract"


class HtmlItem(object):

    def __init__(self, url: str, headers=None, proxy=None):
        self.url = url
        self.type = "0"


class TestApi(Resource):
    def post(self):
        pass

    def get(self):
        if request.method != "GET":
            return "error, method not allowed !"
        # mysql_db = PyMysql(HOST, PORT, USER, PASSWORD, DATABASE)
        # print(type(mysql_db))
        #
        # connection, cursor = mysql_db.connectAndGetCursor()
        # current_app.logger.info(type(connection))
        # current_app.logger.info(type(cursor))
        #
        # # 查询表数据
        # sql = """select CONCAT("alter table ",a.table_name," convert to character set utf8mb4 collate utf8mb4_bin;") from (select table_name from information_schema.`TABLES` where TABLE_SCHEMA = "contract") a;"""
        #
        # res = mysql_db.executeBySelect(connection, cursor, sql)
        # for sql_str in res:
        #     print(sql_str[0])
        # # current_app.logger.info(res)
        # res = re.search(r"\d+", "read12343123asd")
        res = {"a": 123}
        # cache.set("test", serialize(HtmlItem("test")))
        # cache.lpush("aaa", serialize(HtmlItem("zxcvbnm")))
        # res = cache.get('test')
        # # a = cache.rpop("aaa")
        # logger.info(f"{res, type(res)}")
        # logger.info(f"{a, type(a)}")
        logger.info("test")
        return {"code": 200, "mes": "OK", "data": [res, "a"]}
