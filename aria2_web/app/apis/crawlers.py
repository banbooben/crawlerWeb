#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Project : aria2_web
# @File    : crawlers.py
# @Author  : shangyameng@datagrand.com
# @Time    : 2020/5/1 04:00
# @desc: 

from flask import request, current_app
from flask_restful import Resource

from app.extensions.crawler import *
from app.extensions import db
from app.models import *


class CrawlerAPI(Resource):

    @staticmethod
    def processes(crawlerProcess, start_url):
        current_app.logger.info("start to get info with dytt")
        number, result = crawlerProcess(start_url).start()
        current_app.logger.info("start write info to mysql")
        # self.write_to_mysql(result, dyHeaven_fields, DyHeaven)
        print("数据库字段：{}".format(dyHeaven_fields))
        current_app.logger.info("抽取到的结果：{}".format(result))

        return number, result

    @staticmethod
    def write_to_mysql(result, fields, table):
        write_obj_list = []
        if not result or not fields or not table:
            return "no result or no fields"
        for info in result:
            sql_text = ''
            for field in fields:
                if info.get(field, None):
                    if sql_text:
                        sql_text += ', {}={}'.format(field, info[field])
                    else:
                        sql_text += '{}={}'.format(field, info[field])
            print(sql_text)
            # write_obj_list.append(table(eval(sql_text)))
        try:
            # db.session.add_list(write_obj_list)
            print(write_obj_list)
            pass
        except Exception as e:
            # db.session.rollback()
            current_app.logger.error("数据写入失败，已回滚！\nERROR: {}".format(e))

    def post(self):
        pass

    def get(self):
        """
        提供get方法API，调用爬虫爬取相关数据
        :return:
        """
        if request.method != "GET":
            current_app.logger.error("error, method not allowed!")
            return "error, method not allowed!"
        key = request.args.get("request_type", None)
        if key == "download_dytt":
            number, result = self.processes(DyHeavenCrawler, key)
            return {"code": 200, "msg": "succeed", "data": result}
        if key == "download_proxy":
            number, result = self.processes(ProxyCrawler, key)
            return {"code": 200, "msg": "succeed", "data": result}
        return {"code": 2001, "msg": "not worker", "data": []}
