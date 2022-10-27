#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-05-29 13:52:36
# @LastEditTime: 2020-05-29 13:59:56
# @FilePath: /crawlerWeb/crawler_web/app/extensions/crawler/crawlerSaveSql.py

"""
目前存在的问题：
    1、每次请求可能都起三个循环,和三个queue，不合理，重构

改进方向：
    1、使用redis的列表数据类行来做队列
    2、起一个全局的队列管理服务
        1、这里创建三个队列，一直存在不用管
    3、最后数据序列化后直接放入数据库


"""

import abc
import uuid
import time
from threading import Thread
from functools import wraps
from fake_useragent import UserAgent


# from extensions import cache
from application.tools.redis_tools import redis_tools_
from application.initialization.logger_process import logger
from application.utils.dict2obj import XDict
from application.config.extensions_conf import fake_useragent_file_path
# from application.common.common_func import deserialization, serialize


# from conf import logger


class CrawlerBase(object):
    result = []
    redis_key_timeout = 604800

    # redis_tools_ = Redis()
    crawler_item = XDict()
    crawler_item.url = ""
    ua = UserAgent(path=fake_useragent_file_path)

    headers = {
        "User-Agent": ua.random
    }

    proxy = {}

    def __init__(self, start_url, timeout=60):
        self.start_item = self.create_start_utl(start_url)
        self.timeout = timeout
        self.uuid = uuid.uuid4()
        self.message_a = str(self.uuid) + "_messageA"
        self.message_b = str(self.uuid) + "_messageB"
        self.message_c = str(self.uuid) + "_messageC"
        self.crawler_item.headers = self.headers
        # self.crawler_item.proxy = self.proxy

    # @staticmethod
    def create_start_utl(self, start_url):
        self.crawler_item.url = start_url
        return self.crawler_item

    @abc.abstractmethod
    def merger_result(self, item):
        """
        最后数据的合并处理
        """
        pass

    @abc.abstractmethod
    def download_page(self, item):
        """
        请求获取网页
        """
        pass

    @abc.abstractmethod
    def primary(self, item):
        """
        抽取主方法，抽取连接等所需要等内容
        """
        pass

    def get_message(self, key, func):
        try:
            index = 0
            while True:
                message = redis_tools_.rpop(key)
                if message:
                    logger.info(f"{key}, message{message}")
                    # message = deserialization(self.__cls__().Default, message, url="default")
                    merge_process = Thread(target=func,
                                           args=(
                                               eval(message),
                                           ))
                    merge_process.start()
                    index = 0
                else:
                    if index >= self.timeout:
                        exit()
                    index += 1
                    # logger.info(f"{key}: {index}")
                    time.sleep(1)
        except Exception as e:
            logger.exception(e)

    # @staticmethod
    # def get_item_by_serialize_str(item, serialize_str, *args, **kwargs):
    #     item = deserialization(item, serialize_str, *args, **kwargs)
    #     return item
    #
    @staticmethod
    def push_item_in_redis_list(key, item):
        # serialize_str = serialize(item)
        if not isinstance(item, str):
            item = repr(item)
        redis_tools_.lpush(key, item)

    @classmethod
    def __cls__(cls):
        return cls

    # @classmethod
    # def decorator(cls, func):
    #     @wraps(func)
    #     def _wrap(in_dict, *args, **kwargs):
    #         out_dict = MyDict(in_dict)
    #         rst = func(out_dict, *args, **kwargs)
    #         return rst
    #
    #     return _wrap

    def start(self):
        try:
            self.push_item_in_redis_list(self.message_a, self.start_item)
            thr_downloader = Thread(target=self.get_message, args=(self.message_a, self.download_page))
            thr_primary = Thread(target=self.get_message, args=(self.message_b, self.primary))
            thr_merge_result = Thread(target=self.get_message, args=(self.message_c, self.merger_result))
            thr_downloader.start()
            logger.info("下载线程开启！")
            time.sleep(3)

            thr_primary.start()
            logger.info("抽取线程开启！")

            thr_merge_result.start()
            logger.info("数据合并线程开启")

            thr_merge_result.join()
            return self.result
        except Exception as identifier:
            logger.exception(identifier)


if __name__ == "__main__":
    url = "https://www.dy2018.com/html/gndy/dyzz/index.html"
    craw = CrawlerBase(url, 60)
    res = craw.start()
    print(res)
