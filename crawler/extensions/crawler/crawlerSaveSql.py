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
from extensions import cache
from conf.myLog import logger
from common.common_func import deserialization, serialize


# from conf import logger


class CrawlerBase(object):
    result = []
    Default = {
        "url": None
    }

    @abc.abstractmethod
    class Default(object):
        def __init__(self, url):
            self.url = url

    def __init__(self, start_url, timeout=60):
        self.start_item = self.create_start_utl(start_url)
        self.timeout = timeout
        self.uuid = uuid.uuid4()
        self.message_a = str(self.uuid) + "_messageA"
        self.message_b = str(self.uuid) + "_messageB"
        self.message_c = str(self.uuid) + "_messageC"

    @staticmethod
    def create_start_utl(start_url):

        return CrawlerBase.Default(start_url)

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
                message = cache.rpop(key)
                if message:
                    logger.info(f"{key}, message{message}")
                    message = deserialization(self.__cls__().Default, message, url="default")
                    merge_process = Thread(target=func,
                                           args=(
                                               message,
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

    @staticmethod
    def push_item_in_redis_list(key, item):
        serialize_str = serialize(item)
        cache.lpush(key, serialize_str)

    @classmethod
    def __cls__(cls):
        return cls

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

    # def get_message_a(self):
    #     try:
    #         while True:
    #             message_a = cache.brpop(self.message_a, self.timeout)
    #             message_a = deserialization(self.__cls__(), message_a[-1])
    #             if message_a:
    #                 down_process = Thread(target=self.download_page,
    #                                       args=(message_a,))
    #                 down_process.start()
    #     except Exception as e:
    #         logger.exception(e)
    #
    # def get_message_b(self):
    #     try:
    #         while True:
    #             message_b = cache.brpop(self.message_b, self.timeout)
    #             message_b = deserialization(self.__cls__(), message_b[-1])
    #             if message_b:
    #                 primary_process = Thread(target=self.primary,
    #                                          args=(message_b,))
    #                 primary_process.start()
    #     except Exception as e:
    #         logger.exception(e)
    #         print("请求处理完毕！")
    #
    # def get_message_c(self):
    #     try:
    #         while True:
    #             message_c = cache.brpop(self.message_c, self.timeout)
    #             message_c = deserialization(self.__cls__(), message_c[-1])
    #             if message_c:
    #                 merge_process = Thread(target=self.merger_result,
    #                                        args=(
    #                                            message_c,
    #                                        ))
    #                 merge_process.start()
    #     except Exception as e:
    #         logger.exception(e)


if __name__ == "__main__":
    url = "https://www.dy2018.com/html/gndy/dyzz/index.html"
    craw = CrawlerBase(url, 60)
    craw.start()
