#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Project : crawler_web
# @File    : dytt.py
# @Author  : shangyameng@datagrand.com
# @Time    : 2020/4/19 16:38
# @desc: 

from abc import ABC
from flask import current_app

from app.conf.extensions_conf import dyttUrl
from app.extensions.crawler.crawler import CrawlerBase
import requests
import lxml.html
import re
from fake_useragent import UserAgent


class HtmlItem(object):
    ua = UserAgent(verify_ssl=False)

    def __init__(self, url: str, headers=None, proxy=None):
        self.url = url
        self.headers = {"User-Agent": self.ua.random}
        self.proxy = proxy
        self.name = None
        self.classify = None
        self.title = None
        self.date = None
        self.size = None
        self.introduction = None
        self.magnet = None
        self.content = None
        self.type = "0"
        self.xpath_obj = None


class DyHeavenCrawler(CrawlerBase, ABC):
    """
    queueA: 存放需要请求的url对象
    queueB: 存放下载好的网页数据
    """

    def creat_start_utl(self, start_url):
        return HtmlItem(dyttUrl)

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
            # current_app.logger.info("开始下载网页！{}。类型：{}".format(item.url, item.type))
            old_type = item.type
            if item.url:
                html_obj = requests.get(item.url, params=item.headers)
                html_str = html_obj.content.decode("gbk")
                item.content = html_str
                item.xpath_obj = lxml.html.fromstring(html_str)
            print("下载前类型：{}， 下载后类型：{}".format(old_type, item.type))
            # current_app.logger.info("下载前类型：{}， 下载后类型：{}".format(old_type, item.type))
            self.queueB.put(item)
        except Exception as e:
            print("download_page:  {}".format(e))
            # current_app.logger.error("download_page:  {}".format(e))

    def primary(self, item: HtmlItem):
        """
        抽取主方法，抽取连接等所需要等内容
        """
        try:
            print("开始抽取：{}".format(item.type))
            # current_app.logger.info("开始抽取：{}".format(item.type))
            if item.type == "1":
                try:
                    tables = item.xpath_obj.xpath("//div[@class='bd3']//div[@class='co_content8']/ul//table")
                    # print(len(tables))
                    # re_str = r'"(.*?)" class="ulink" title="(.*?)">.*?>日期：([\d\.\-/]{10}).*?">"◎(.*?)"'
                    # print(re.findall(re_str, item.content))
                    for table in tables:
                        # URL抽取
                        url = table.xpath(".//tr[2]//a/@href")
                        if url:
                            new_url = url[0]
                            if not new_url.startswith("http"):
                                new_url = dyttUrl + new_url
                            # print("列表页抽取到的网址：{}".format(new_url))
                            tr_item = HtmlItem(new_url)
                            tr_item.type = "2"

                            title = table.xpath(".//tr[2]//a/text()")
                            tr_item.title = title[0] if title else "None"

                            name = table.xpath(".//tr[2]//a/text()")[0] if table.xpath(
                                ".//tr[2]//a/text()") else "《None》"
                            tr_item.name = "《{}》".format("".join(re.findall(r"《(.*?)》", name)))

                            date = table.xpath(".//tr[3]//font/text()")
                            tr_item.date = date[0] if date else "None"

                            introduction = table.xpath(".//tr[4]/td/text()")
                            tr_item.introduction = introduction[0] if introduction else "None"
                            self.queueA.put(tr_item)
                            print("{}".format({"url": tr_item.url[:30], "name": tr_item.name[:6],
                                               "title": tr_item.title[:6],
                                               "introduction": tr_item.introduction[:30],
                                               "type": tr_item.type[:6]}), end=", ")
                except Exception as e:
                    print("列表页抽取:  {}".format(e))
                    # current_app.logger.error("列表页抽取:  {}".format(e))
            elif item.type == "2":
                try:
                    print("开始抽取详情页信息：{}".format(item.url))
                    # current_app.logger.info("开始抽取详情页信息：{}".format(item.url))
                    down_lists = item.xpath_obj.xpath("//div[@id='downlist']/table")
                    if not down_lists:
                        down_lists = item.xpath_obj.xpath("//div[@id='Zoom']/table")
                        # print("再次处理得到的连接：{}".format(len(down_lists)))
                    # print("共有下载连接：{}".format(len(down_lists)))
                    magnet_list = []
                    for downloader in down_lists:
                        magnet = downloader.xpath(".//a/@href")[0] if downloader.xpath(".//a/@href") else ""
                        download_name = downloader.xpath(".//a/text()")[0] if downloader.xpath(".//a/text()") else "]"
                        magnet_name = re.split(r"[=\]/]", download_name)[-1]
                        # print("magnet_name: {}".format(magnet_name))
                        magnet_list.append((magnet_name, magnet))
                    item.magnet = magnet_list
                    self.queueC.put(item)
                except Exception as e:
                    print("信息页抽取:  {}".format(e))
                    # current_app.logger.error("信息页抽取:  {}".format(e))
            elif item.type == "0":
                try:
                    area2s = item.xpath_obj.xpath(
                        "//div[@class='bd2']/div[@class='index_list']/div[@class='co_area2']")
                    for area in area2s:
                        url = area.xpath(".//div[@class='title_all']/p/span/a/@href")
                        if url:
                            new_url = url[0]
                            if not new_url.startswith("http"):
                                new_url = dyttUrl + new_url
                            print("首页抽取抽取到的网址：{}".format(new_url))
                            # current_app.logger.info("首页抽取抽取到的网址：{}".format(new_url))
                            tr_item = HtmlItem(new_url)
                            tr_item.type = "1"
                            tr_item.classify = area.xpath(".//div[@class='title_all']/p/span/a/text()")[0]
                            # print("首页抽取抽取到的分类：{}".format(tr_item.classify))
                            self.queueA.put(tr_item)
                except Exception as e:
                    print("首页抽取:  {}".format(e))
                    # current_app.logger.error("首页抽取:  {}".format(e))
        except Exception as e:
            print("primary:  {}".format(e))
            # current_app.logger.error("primary:  {}".format(e))


if __name__ == "__main__":
    zero_crawler = DyHeavenCrawler("test")
    res = zero_crawler.start()
    print(res)
