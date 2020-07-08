#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-04-23 20:50:01
# @FilePath: /crawler_web/app/apis/aria.py

from flask import request, current_app, render_template
from flask_restful import Resource
from ..application import aria2_downloader, logger
from app.extensions.crawler.zeroMag import ZeroCrawler
from app.models.dytt_model import DyHeaven
from app.models.proxy_model import Proxy

# from ..extensions import db
# from flask import current_app


class AriaAPI(Resource):
    def post(self):
        """
        # @description: post请求，根据请求参数不同执行不同的方法
        # @param {type} 
        # @return: 
        """
        if request.method != "POST":
            return "error, method not allowed !"
        key = request.form.get("request_type", None)
        if key == "add_downloader":
            download_url = request.form.get("download_url", None)
            if download_url:
                response = aria2_downloader.addUrl(download_url)
                return response
        res = {"code": 200, "msg": "不做处理", "data": "result"}
        return res

    def get(self):
        """
        
        # @description: 
        # @param {type} 
        # @return: 
        
        """
        try:
            key = request.args.get("key", None)
            if key == "search":
                values = request.args.get("search", None)
                if values:
                    search_res = ZeroCrawler(values).start()
                    print(search_res)
                    res = {"code": 200, "msg": "OK", "data": search_res}
                    logger.info("请求成功：{}".format(res))
                    return res
                res = {"code": 1002, "msg": "error", "data": []}
                logger.info("请求失败：{}".format(res))
                return res
            res = {"code": 1000, "msg": "不做处理", "data": []}
            logger.info("请求成功：{}".format(res))
            return res
        except Exception as e:
            logger.error(e)
