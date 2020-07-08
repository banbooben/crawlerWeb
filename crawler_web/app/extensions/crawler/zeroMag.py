#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-11 20:32:31
# @LastEditTime: 2020-04-17 23:28:23
# @FilePath: /crawler_web/app/crawler/zeroMag.py
from abc import ABC

from app.conf.extensions_conf import zeroMagUrl
from app.extensions.crawler.crawler import CrawlerBase
import requests
import lxml.html
import re


# from flask import current_app


class HtmlItem(object):
    def __init__(self, url: str, headers=None, proxy=None):
        self.url = url
        self.headers = headers
        self.proxy = proxy
        self.name = None
        self.title = None
        self.size = None
        self.magnet = None
        self.content = None
        self.type = None


class ZeroCrawler(CrawlerBase, ABC):
    """
    queueA: 存放需要请求的url对象
    queueB: 存放下载好的网页数据
    """

    def creat_start_utl(self, start_url):
        url = zeroMagUrl + "?q={}".format(start_url)
        return HtmlItem(url)

    def merger_result(self, item: HtmlItem, result: list):
        """
        获取下一页的网页地址等
        """
        try:
            item_res = {
                "name": item.name,
                "title": item.title,
                "size": item.size,
                "magnet": item.magnet
            }
            result.append(item_res)
        except Exception as e:
            print("merger_result:  {}".format(e))
            # current_app.logger.error(e)

    def download_page(self, item: HtmlItem):
        """
        获取下一页的网页地址等
        """
        try:
            print("开始下载网页！")
            if item.url:
                html_obj = requests.get(item.url, params=item.headers)
                html_str = html_obj.content.decode("utf-8")
                item.content = html_str
                if not item.type:
                    item.type = "1"
            self.queueB.put(item)
        except Exception as e:
            print("download_page:  {}".format(e))
            # current_app.logger.error(e)

    def primary(self, item: HtmlItem):
        """
        抽取主方法，抽取连接等所需要等内容
        """
        try:
            if item.type == "1":
                html_str = item.content
                parse_result = lxml.html.fromstring(html_str)
                tables = parse_result.xpath("//tbody/tr")
                for tr in tables:
                    url = tr.xpath(".//a/@href")[0].strip()
                    tr_item = HtmlItem(url)
                    tr_item.name = tr.xpath(".//a/text()")[0].strip()
                    tr_item.title = tr.xpath(".//p/text()")[0].strip()
                    tr_item.size = tr.xpath(
                        './/td[@class="td-size"]/text()')[0].strip()
                    tr_item.type = "2"
                    self.queueA.put(tr_item)
                    print("{}".format({"url": tr_item.url[:6], "name": tr_item.name[:6], "title": tr_item.title[:6],
                                       "size": tr_item.size[:6], "type": tr_item.type[:6]}), self.queueB.qsize(),
                          end=", ")
            elif item.type == "2":
                magnet = re.findall(r" value=\"(.*?)\" spellcheck",
                                    item.content)
                if magnet:
                    item.magnet = [magnet[0], ]
                self.queueC.put(item)
        except Exception as e:
            print("primary:  {}".format(e))
            # current_app.logger.error(e)


if __name__ == "__main__":
    zero_crawler = ZeroCrawler("anjelica")
    res = zero_crawler.start()
    print(res)
