# #!/usr/local/bin python3
# # -*- coding: utf-8 -*-
# # @Project : crawler_web
# # @File    : dytt.py
# # @Author  : shangyameng@datagrand.com
# # @Time    : 2020/4/19 16:38
# # @desc:
#
# from abc import ABC
# from flask import current_app
# import requests
# import lxml.html
# import re
# import os
# import json
# from fake_useragent import UserAgent
#
# # from application.config.extensions_conf import dyttUrl, fake_useragent_file_path
# # from extensions.crawler.crawler import CrawlerBase
# from application.extensions.crawler.crawlerSaveSql import CrawlerBase
# # from application.extensions import cache
# from application.initialization.logger_process import logger
# # from common.common_func import serialize, deserialization
# from application.utils.dict2obj import XDict
# from pathlib import Path
#
#
# # ua = UserAgent(path=os.path.join(os.getcwd(), "fake_useragent_0.1.11.json"))
#
#
# class DyHeavenCrawler(CrawlerBase, ABC):
#     crawler_item = XDict()
#
#     redis_key_timeout = 604800
#
#     crawler_item.url = "url"
#     crawler_item.name = "None"
#     crawler_item.classify = "None"
#     crawler_item.title = "None"
#     crawler_item.date = "None"
#     crawler_item.size = "None"
#     crawler_item.introduction = "None"
#     crawler_item.magnet = "None"
#     crawler_item.content = "None"
#     crawler_item.type = "0"
#     crawler_item.xpath_obj = "None"
#
#     """
#     queueA: 存放需要请求的url对象
#     queueB: 存放下载好的网页数据
#     """
#
#     # def create_start_utl(self, start_url):
#     #     return serialize(HtmlItem())
#
#     def merger_result(self, item):
#         """
#         获取下一页的网页地址等
#         """
#         item = MyDict(item)
#         try:
#             item_res = {
#                 "url": item.url,
#                 "name": item.name,
#                 "title": item.title,
#                 "size": item.size,
#                 "magnet": item.magnet
#             }
#             self.result.append(item_res)
#             # if item.url in cache.keys() and item_res == cache.get(item.url):
#             #     self.result.append(cache.get(item.url))
#             # else:
#             #     cache.set(item.url, json.dumps(item_res, ensure_ascii=False))
#             # self.res
#         except Exception as e:
#             logger.error("merger_result:  {}".format(e))
#             # current_app.logger.error("merger_result:  {}".format(e))
#
#     def download_page(self, item):
#         """
#         获取下一页的网页地址等
#         根据当前状态标记新的状态
#         0：初始页面
#         1：全局列表页面
#         2: 抽取下载连接
#         """
#         item = MyDict(item)
#         try:
#             print(f" download_page info: {item.url}")
#             logger.info("开始下载网页！{}。类型：{}".format(item.url, item.type))
#             # current_app.logger.info("开始下载网页！{}。类型：{}".format(item.url, item.type))
#             old_type = item.type
#             if item.url != "None" and not cache.get(item.url):
#                 # if item.url != "None":
#                 html_obj = requests.get(item.url, headers=self.headers)
#                 html_str = html_obj.content.decode("gbk")
#                 item.content = html_str
#                 print(len(html_str))
#
#                 # 请求结果存入redis数据库
#                 cache.set(item.url, html_str)
#                 cache.expire(item.url, self.redis_key_timeout)
#
#                 # item.xpath_obj = lxml.html.fromstring(html_str)
#             logger.info("下载前类型：{}， 下载后类型：{}".format(old_type, item.type))
#             self.push_item_in_redis_list(self.message_b, item)
#         except Exception as e:
#             logger.error("download_page:  {}".format(e))
#             # current_app.logger.error("download_page:  {}".format(e))
#
#     def primary(self, item):
#         """
#         抽取主方法，抽取连接等所需要等内容
#         """
#         item = MyDict(item)
#         try:
#             logger.info("开始抽取：{}".format(item.url))
#             xpath_obj = lxml.html.fromstring(item.content)
#             # current_app.logger.info("开始抽取：{}".format(item.type))
#             if item.type == "1":
#                 try:
#
#                     tables = xpath_obj.xpath("//div[@class='bd3']//div[@class='co_content8']/ul//table")
#                     print(len(tables))
#                     for table in tables:
#                         # URL抽取
#                         url = table.xpath(".//tr[2]//a/@href")
#                         if url:
#                             new_url = url[0]
#                             if not new_url.startswith("http"):
#                                 new_url = dyttUrl + new_url
#                             tr_item = MyDict()
#                             tr_item.url = new_url
#                             tr_item.type = "2"
#                             title = table.xpath(".//tr[2]//a/text()")
#                             tr_item.title = title[0] if title else "None"
#
#                             name = table.xpath(".//tr[2]//a/text()")[0] if table.xpath(
#                                 ".//tr[2]//a/text()") else "《None》"
#                             tr_item.name = "《{}》".format("".join(re.findall(r"《(.*?)》", name)))
#
#                             date = table.xpath(".//tr[3]//font/text()")
#                             tr_item.date = date[0] if date else "None"
#
#                             introduction = table.xpath(".//tr[4]/td/text()")
#                             tr_item.introduction = introduction[0] if introduction else "None"
#                             self.push_item_in_redis_list(self.message_a, tr_item)
#                             logger.info("{}".format({"url": tr_item.url[:30], "name": tr_item.name[:6],
#                                                      "title": tr_item.title[:6],
#                                                      "introduction": tr_item.introduction[:30],
#                                                      "type": tr_item.type[:6]}))
#                 except Exception as e:
#                     logger.error("列表页抽取:  {}".format(e))
#                     # current_app.logger.error("列表页抽取:  {}".format(e))
#             elif item.type == "2":
#                 try:
#                     logger.info("开始抽取详情页信息：{}".format(item.url))
#                     # current_app.logger.info("开始抽取详情页信息：{}".format(item.url))
#                     down_lists = xpath_obj.xpath("//div[@id='downlist']/table")
#                     if not down_lists:
#                         down_lists = xpath_obj.xpath("//div[@id='Zoom']/table")
#                         # print("再次处理得到的连接：{}".format(len(down_lists)))
#                     # print("共有下载连接：{}".format(len(down_lists)))
#                     # magnet_info = {}
#                     magnet_info = []
#                     for downloader in down_lists:
#                         magnet = downloader.xpath(".//a/@href")[0] if downloader.xpath(".//a/@href") else ""
#                         download_name = downloader.xpath(".//a/text()")[0] if downloader.xpath(".//a/text()") else "]"
#                         magnet_name = re.split(r"[=\]/]", download_name)[-1]
#                         # magnet_info.update({magnet_name: magnet})
#                         magnet_info.append((magnet_name, magnet))
#                     item.magnet = magnet_info
#                     self.push_item_in_redis_list(self.message_c, item)
#                 except Exception as e:
#                     logger.error("信息页抽取:  {}".format(e))
#                     # current_app.logger.error("信息页抽取:  {}".format(e))
#             elif item.type == "0":
#                 try:
#                     area2s = xpath_obj.xpath(
#                         "//div[@class='bd2']/div[@class='index_list']/div[@class='co_area2']")
#                     for area in area2s:
#                         url = area.xpath(".//div[@class='title_all']/p/span/a/@href")
#                         if url:
#                             new_url = url[0]
#                             if not new_url.startswith("http"):
#                                 new_url = dyttUrl + new_url
#                             logger.info("首页抽取抽取到的网址：{}".format(new_url))
#                             # current_app.logger.info("首页抽取抽取到的网址：{}".format(new_url))
#                             # tr_item = DyHeavenCrawler.Default(new_url)
#
#                             tr_item = MyDict()
#                             tr_item.url = new_url
#
#                             tr_item.type = "1"
#                             tr_item.classify = area.xpath(".//div[@class='title_all']/p/span/a/text()")[0]
#                             # print("首页抽取抽取到的分类：{}".format(tr_item.classify))
#                             self.push_item_in_redis_list(self.message_a, tr_item)
#                 except Exception as e:
#                     logger.error("首页抽取:  {}".format(e))
#                     # current_app.logger.error("首页抽取:  {}".format(e))
#         except Exception as e:
#             logger.error("primary:  {}".format(e))
#             # current_app.logger.error("primary:  {}".format(e))
#
#
# if __name__ == "__main__":
#     zero_crawler = DyHeavenCrawler(dyttUrl, 20)
#     res = zero_crawler.start()
#     print(res)
