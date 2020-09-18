#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-11 20:32:31
# @LastEditTime: 2020-04-17 10:07:44
# @FilePath: /crawler_web/app/crawler/crawler.py

import abc
import time
from queue import Queue
from threading import Thread
from flask import current_app


class CrawlerBase(object):
    queueA = Queue()  # 网页连接
    queueB = Queue()  # 下载的网页数据
    queueC = Queue()  # 抽取得到的结果

    def __init__(self, start_url, timeout=5):
        self.start_url = self.creat_start_utl(start_url)
        self.timeout = timeout

    def creat_start_utl(self, start_url):
        return start_url

    @abc.abstractmethod
    def merger_result(self, item, result):
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

    def get_messageA(self):
        try:
            while True:
                messageA = self.queueA.get(timeout=self.timeout)
                down_process = Thread(target=self.download_page,
                                      args=(messageA, ))
                down_process.start()
        except Exception as e:
            # current_app.logger.error(e)
            print(e)

    def get_messageB(self):
        try:
            while True:
                queueB = self.queueB.get(timeout=self.timeout)
                primary_process = Thread(target=self.primary,
                                         args=(queueB, ))
                primary_process.start()
        except Exception as e:
            # current_app.logger.error("请求处理完毕！")
            print("请求处理完毕！")

    def get_messageC(self):
        result = []
        try:
            while True:
                if not self.queueC.empty():
                    messageC = self.queueC.get()
                    merge_process = Thread(target=self.merger_result,
                                           args=(
                                               messageC,
                                               result,
                                           ))
                    merge_process.start()
                else:
                    print("请求处理完毕！")
                    break
            return result
        except Exception as e:
            print(e)
            # current_app.logger.error(e)

    def put_start_item_in_queue(self):
        self.queueA.put(self.start_url)

    def start(self):
        try:
            self.put_start_item_in_queue()
            thr_downloader = Thread(target=self.get_messageA)
            thr_primary = Thread(target=self.get_messageB)
            thr_downloader.start()
            print("下载线程开启！")
            # current_app.logger.info("下载线程开启！")
            time.sleep(self.timeout-2)
            thr_primary.start()
            print("抽取线程开启！")
            # current_app.logger.info("抽取线程开启！")
            # thr_downloader.join()
            thr_primary.join()
            res = self.get_messageC()
            print("处理最终结果：{}".format(res))
            # current_app.logger.info("处理最终结果：{}".format(res))
            return len(res), res
        except Exception as identifier:
            print(identifier)
            # current_app.logger.error(identifier)


if __name__ == "__main__":
    url = "https://www.dy2018.com/html/gndy/dyzz/index.html"
    craw = CrawlerBase(url)
    craw_res = craw.start()
