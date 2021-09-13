#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/2 18:57
# @Author  : shangyameng@aliyun.com
# @Site    :
# @File    : extensions_conf.py

import os
from pathlib import Path

# http config
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 5000

# header config
fake_useragent_file_path = "/Users/sarmn/import_files/fake_useragent_0.1.11.json"

# aria config
aria_host = "127.0.0.1"
aria_port = "6800"
aria_token = "test"


class OcrConfig(object):
    """OCR配置"""

    ocr_url = os.getenv("OCR_URL", "http://ysocr.datagrand.cn/ysocr/ocr")
    ocr_file = os.getenv("OCR_FILE", "http://ysocr.datagrand.cn/file/")

    word2pdf_fields = ['doc', "docx", 'xls', 'xlsx']
    ocr_file_suffix = ["pdf", "jpeg", "jpg", "png", "PDF", "JPG", "JPEG", "PNG"]


ocr_config = OcrConfig()

# 0mag.net请求地址
zeroMagUrl = 'https://0mag.net/search'

# 电影天堂请求地址
dyttUrl = 'https://www.dy2018.com'

# 西刺代理请求地址
proxyUrl = {
    "高匿": "https://www.xicidaili.com/nn/4052",
    # "普通": "https://www.xicidaili.com/nt/",
    # "qq": "https://www.xicidaili.com/qq"
}
# 西刺代理地址拼接头
proxyUrlFront = "https://www.xicidaili.com/"
