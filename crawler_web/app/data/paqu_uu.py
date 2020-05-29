# -*- coding:utf-8 -*-
import os
import re
import time
from queue import Queue
from threading import Thread
from urllib.parse import quote

import requests
from fake_useragent import UserAgent


class HtmlItem(object):

    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.thunder = ""


class PaChong(object):
    ug = UserAgent(verify_ssl=False)
    thunder_list = []
    item_q = Queue()
    page_q = Queue()
    res_q = Queue()

    def __init__(self, url_list, must_str_list):
        self.must_str_list = must_str_list if must_str_list else []
        self.url_list = url_list
        self.header = {
            "User-Agent": self.ug.random,
            "referer": "https://www.96dcw.com/shipin/index.html",
        }

    def _get_next_url_in_first_page(self, item: HtmlItem):
        try:
            result_html = requests.get(item.url,
                                       headers=self.header).content.decode('utf-8')
            url_str_list = [x for x in re.split(r'/', item.url) if x != '']
            front_url = url_str_list[0] + '//' + url_str_list[1]
            sec_href_list = [
                x for x in re.findall(r'<a href="(.*?)" title="(.*?)" target', result_html)
                if len(x) > 1]
            must_str = "|".join(self.must_str_list)
            thr_href_list = []
            print("B", must_str)
            for ind in sec_href_list:
                res = re.findall(r"{}".format(must_str), ind[1])
                if res:
                    thr_href_list.append((ind[1], front_url + ind[0]))
                    self.item_q.put(HtmlItem(front_url + ind[0], "XJJ-" + ind[1]))
                    print("C", "XJJ-" + ind[1], front_url + ind[0])
            print("A", thr_href_list)
            next_page = re.findall(r'[\d]+</a> <a href="(.*?)" title="下一页">', result_html)
            if next_page:
                if not re.findall(r"(javascript:;)", next_page[0]):
                    next_page_url = front_url + quote(next_page[0])
                    print(next_page_url, "下一页")
                    self.page_q.put(HtmlItem(next_page_url, "下一页"))
        except Exception as e:
            print(e, "二级页面信息抽取失败...", end="\n")

    def _get_thunder_in_item_q(self, item: HtmlItem):
        try:
            res_html = requests.get(item.url,
                                    headers=self.header).content.decode('utf-8')
            thunder_str = 'h' + re.findall('value="h(.*?)">', res_html)[0]
            item.thunder = thunder_str
            print('{}：抽取完毕'.format(item.url))
            print('\t抽取到：{}'.format(thunder_str))
            self.res_q.put(item)
        except Exception as e:
            print(e, "获取磁力链接失败...")

    def _write_thunder_to_txt(self):
        if self.page_q.empty() and self.item_q.empty():
            try:
                thunder_num = self.res_q.qsize()
                if not os.path.exists('/Users/shangyameng/Nextcloud/code/paqu_uu/data/'):
                    os.mkdir('/Users/shangyameng/Nextcloud/code/paqu_uu/data/')
                with open('/Users/shangyameng/Nextcloud/code/paqu_uu/data/thunder.txt', 'a') as f:
                    while not self.res_q.empty():
                        thunder_item = self.res_q.get()
                        write_str = thunder_item.title + '：\n'
                        f.write(thunder_item.thunder + '\n')
                print('已写入数据：{}条'.format(thunder_num))
            except Exception as e:
                print(e, "数据保存失败", end="\n")

    def deal_item_url_in_queue(self):
        while True:  # 如果队列不为空
            try:
                item_url = self.item_q.get(block=True, timeout=60)
                print('开始抽取：', item_url.url)
                thr = Thread(target=self._get_thunder_in_item_q, args=(item_url,))
                thr.start()
            except Exception as e:
                print(e, '待抽取处理完毕', end="\n")
                break

    def deal_page_url_in_queue(self):
        while True:  # 如果队列不为空
            try:
                url = self.page_q.get(block=True, timeout=60)
                print('开始处理：', url)
                thr = Thread(target=self._get_next_url_in_first_page, args=(url,))
                thr.start()
            except Exception as e:
                print('待抽取处理完毕')
                break

    def add_url_in_list(self, url_list):
        if url_list:
            for item_html in url_list:
                self.page_q.put(HtmlItem(item_html[0], item_html[1]))

    def start(self):
        try:
            print('{}\n爬虫任务启动中......'.format('*' * 30))
            time.sleep(3)
            print('爬虫任务启动成功，开始执行\n{}'.format('*' * 30))
            self.add_url_in_list(self.url_list)
            print("爬取地址添加完毕")
            page_thr = Thread(target=self.deal_page_url_in_queue)
            item_thr = Thread(target=self.deal_item_url_in_queue)
            print('页面处理线程启动成功')
            page_thr.start()
            print('抽取线程启动成功')
            item_thr.start()
            print("开始写入抽取到的数据。。。")
            self._write_thunder_to_txt()
        except Exception as e:
            print(e)


url_list = [
    ("https://www.59etr.com/shipin/list-%E6%AC%A7%E7%BE%8E%E7%B2%BE%E5%93%81.html", "欧美")
]
key_list = []

page = PaChong(url_list, key_list)
# page.start(url_list)
# page._get_next_url_in_first_page(test_url)
page.start()


def download_meizitu(pic_dir_name, page_num=1):
    header = {
        "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "Referer": "https://www.mzitu.com/tag/youhuo/"
    }
    # 循环遍历要处理的页面
    for i in range(page_num):
        if i == 0:
            url = 'https://www.mzitu.com/tag/youhuo/'
        else:
            url = 'https://www.mzitu.com/tag/youhuo/page/{}/'.format(i + 1)

        # 请求网页
        result_list = requests.get(url, headers=header)

        # 拼接并创建文件夹
        dir_name = os.getcwd() + '/download/' + pic_dir_name
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print('创建新文件夹')
        all_info = result_list.text

        # 二级地址的提取,需要创建的文件夹
        re_re = re.compile(
            r"<li><a href=\"(.*?)\" target=\"_blank\"><img class=\'lazy\' src=\'https://i.meizitu.net/pfiles/img/lazy.png\' data-original=\'(.*?)\' alt=\'(.*?)\' width"
        )
        pic_urls_info = re_re.findall(all_info)

        # 循环处理提取到的地址并访问二级URL
        for pic_url in pic_urls_info:
            sec_pic_url = pic_url[0]
            result_pic = requests.get(sec_pic_url, headers=header)
            sec_info = result_pic.text

            # 创建单独的高清文件文件夹
            sec_dir_name = os.getcwd(
            ) + '/download/' + pic_dir_name + '/' + pic_url[-1]
            # print(os.path.exists(sec_dir_name), pic_url[-1])
            if not os.path.exists(sec_dir_name):
                os.makedirs(sec_dir_name)
                print('创建二级文件夹{}'.format(sec_dir_name))

            # 提取该人有多少张照片（即要请求的次数）
            sec_re = re.compile(
                r">\…</span><a href=\'(.*?)\'><span>(.*?)</span></a><a href\=")
            pic_nums = sec_re.findall(sec_info)[-1][-1]

            pic_num = 0
            while pic_num < int(pic_nums):
                # for pic_num in range(int(pic_nums)):
                if pic_num == 1:
                    headers = header

                # 拼接二级请求用到的header
                headers = {
                    "User-Agent":
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                    "Referer": sec_pic_url + "/{}".format(pic_num + 1)
                }

                sec_pic_urls = sec_pic_url + "/{}".format(pic_num + 1)
                # 请求二级页面数据
                result_pic = requests.get(sec_pic_urls, headers=headers)
                sec_info = result_pic.text

                # 提取高清图片地址
                big_pic = re.compile(r'><img src=\"(.*?)\" alt')
                big_pic_url = big_pic.findall(sec_info)
                print(big_pic_url)
                if len(big_pic_url) == 0:
                    pic_num -= 1
                    continue
                # 请求高清图片
                pic = sec_dir_name + '/' + big_pic_url[-1].split('/')[-1]
                pic_name = big_pic_url[-1].split('/')[-1]
                is_download = os.path.exists(pic)
                if not is_download:
                    result_big_pic = requests.get(big_pic_url[-1],
                                                  headers=headers)
                    with open(sec_dir_name + '/' + pic_name, 'wb+') as f:
                        f.write(result_big_pic.content)
                    print('正在下载：{}...'.format(pic_name))
                    pic_num += 1
                else:
                    print('{}已下载过，自动跳过......'.format(pic))
                    pic_num += 1
                    continue

# download_meizitu("meizitu", 127)
