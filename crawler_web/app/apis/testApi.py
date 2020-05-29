#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Project : crawlerWeb
# @File    : testApi.py
# @Author  : shangyameng@datagrand.com
# @Time    : 2020/5/26 14:47
# @desc:

from flask import request, current_app
from flask_restful import Resource

from app.extensions.crawler import *
from app.extensions.mysql.mysql_protogenesis import PyMysql
from app.extensions import db, logger
from app.models import *
from app.conf.server_conf import get_mysql_info, current_environment

# USER, PASSWORD, HOST, PORT, DATABASE = get_mysql_info(current_environment)

USER, PASSWORD, HOST, PORT, DATABASE = "root", "root", "127.0.0.1", 16153, "contract"


class TestApi(Resource):
    def post(self):
        pass

    def get(self):
        if request.method != "GET":
            return "error, method not allowed !"
        mysql_db = PyMysql(HOST, PORT, USER, PASSWORD, DATABASE)
        print(type(mysql_db))

        connection, cursor = mysql_db.connectAndGetCursor()
        current_app.logger.info(type(connection))
        current_app.logger.info(type(cursor))

        # 查询表数据
        sql = """select CONCAT("alter table",a.table_name,"convert to character set utf8mb4 collate utf8mb4_bin;") from (select table_name from information_schema.`TABLES` where TABLE_SCHEMA = "contract") a;"""

        res = mysql_db.executeBySelect(connection, cursor, sql)
        for sql_str in res:
            print(sql_str[0])
        # current_app.logger.info(res)
        return {"code": 200, "mes": "OK", "data": str(res)}
