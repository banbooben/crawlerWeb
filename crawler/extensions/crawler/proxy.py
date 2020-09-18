#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Project : crawler_web
# @File    : proxy.py
# @Author  : shangyameng@datagrand.com
# @Time    : 2020/4/23 12:14
# @desc: 


from abc import ABC
from flask import current_app
from conf.extensions_conf import proxyUrl, proxyUrlFront
from extensions.crawler.crawler import CrawlerBase
import requests
import lxml.html
import re
import time
from fake_useragent import UserAgent


# from flask import current_app


class HtmlItem(object):
    ua = UserAgent(verify_ssl=False)

    def __init__(self, url: str, headers=None, proxy={}):
        self.url = url
        self.headers = {"User-Agent": self.ua.random}
        self.proxy = proxy
        self.ip = None
        self.port = None
        self.address = None
        self.anonymity = None
        self.net_type = None
        self.speed = None
        self.connect_time = None
        self.alive_time = None
        self.content = None
        self.type = "0"
        self.xpath_obj = None
        self.page_num = 1
        self.auth_time = None


class ProxyCrawler(CrawlerBase, ABC):
    """
    queueA: 存放需要请求的url对象
    queueB: 存放下载好的网页数据
    """
    QueueProxy = []

    def creat_start_utl(self, start_url):

        return proxyUrl

    def put_start_item_in_queue(self):
        for key in self.start_url.keys():
            url = self.start_url[key]
            item = HtmlItem(url)
            self.queueA.put(item)

    def merger_result(self, item: HtmlItem, result: list):
        """
        获取下一页的网页地址等
        """
        try:
            item_res = {"url": item.url,
                        "ip": item.ip,
                        "port": item.port,
                        "net_type": item.net_type,
                        "address": item.address,
                        "anonymity": item.anonymity,
                        "speed": item.speed,
                        "connect_time": item.connect_time
                        }
            result.append(item_res)
        except Exception as e:
            print("merger_result:  {}".format(e))
            # current_app.logger.error("merger_result:  {}".format(e))

    def download_page(self, item: HtmlItem):
        """
        获取下一页的网页地址等
        根据当前状态标记新的状态
        0：初始页面
        1：全局列表页面
        2: 抽取下载连接
        """
        try:
            print("开始下载网页！{}。类型：{}".format(item.url, item.type))
            old_type = item.type
            if item.url:
                html_obj = requests.get(item.url, headers=item.headers)
                html_str = html_obj.content.decode("utf-8")
                item.content = html_str
                item.xpath_obj = lxml.html.fromstring(html_str)
            # print("当前类型：{}".format(old_type))
            self.queueB.put(item)
        except Exception as e:
            print("download_page:  {}".format(e))
            # current_app.logger.error("download_page:  {}".format(e))

    def primary(self, item: HtmlItem):
        """
        抽取主方法，抽取连接等所需要等内容
        """
        try:
            print("开始抽取：{}".format(item.url))
            # current_app.logger.info("开始抽取：{}".format(item.url))
            if item.type == "0":
                try:
                    print("开始抽取第<{}>页：".format(item.page_num))
                    # current_app.logger.info("开始抽取第<{}>页：".format(item.page_num))
                    trs = item.xpath_obj.xpath("//table[@id='ip_list']//tr")
                    for tr in trs:
                        new_item = HtmlItem(item.url)
                        ip = tr.xpath(".//td[2]/text()")
                        new_item.ip = ip[0] if ip else ""
                        port = tr.xpath("//td[3]/text()")
                        new_item.port = port[0] if port else ""
                        address = tr.xpath("//td[4]/a/text()")
                        new_item.address = address[0] if address else ""
                        anonymity = tr.xpath("//td[5]/text()")
                        new_item.anonymity = anonymity[0] if anonymity else ""
                        net_type = tr.xpath("//td[6]/text()")
                        new_item.net_type = net_type[0] if net_type else ""
                        speed = tr.xpath("//td[7]/div[@class='bar']/@title")
                        new_item.speed = speed[0] if speed else ""
                        connect_time = tr.xpath("//td[8]/div[@class='bar']/@title")
                        new_item.connect_time = connect_time[0] if connect_time else ""
                        alive_time = tr.xpath("//td[9]/text()")
                        new_item.alive_time = alive_time[0] if alive_time else ""
                        auth_time = tr.xpath("//td[10]/text()")
                        new_item.auth_time = auth_time[0] if auth_time else ""
                        self.queueC.put(new_item)
                        print("{}".format({"url": new_item.url, "ip": new_item.ip,
                                           "port": new_item.port, "net_type": new_item.net_type,
                                           "address": new_item.address,
                                           "anonymity": new_item.anonymity, "speed": new_item.speed,
                                           "connect_time": new_item.connect_time}), end=", ",
                              sep="\n")

                    page_nations = item.xpath_obj.xpath('//div[@class="pagination"]')
                    page_nation = page_nations[0] if page_nations else None
                    next_page = page_nation.xpath(".//a[@class='next_page']/@href") if page_nation else None
                    page_num_item = page_nation.xpath(".//em[@class='current']/text()") if page_nation else None
                    next_url = proxyUrlFront + next_page[0] if next_page else None
                    page_num = page_num_item[0] if page_num_item else None
                    if next_url and page_num:
                        html_item = HtmlItem(url=next_url)
                        html_item.page_num = page_num
                        self.queueA.put(html_item)
                    else:
                        print("抽取完毕")
                        # current_app.logger.info("抽取完毕")
                except Exception as e:
                    print("列表页抽取:  {}".format(e))
                    # current_app.logger.error("列表页抽取:  {}".format(e))
        except Exception as e:
            print("primary:  {}".format(e))
            # current_app.logger.error(e)


if __name__ == "__main__":
    zero_crawler = ProxyCrawler("test")
    res = zero_crawler.start()
    print(res)
