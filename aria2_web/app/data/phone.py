#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-27 16:35:56
# @LastEditTime: 2020-04-27 16:51:18
# @FilePath: /aria2_web/app/data/phone.py


import re

s = "15737313097"

res = re.search(r"1([38][\d]|[4][01456789]|[5][012356789]|[6][567]|[9][189])[\d]{8}", s)

print(res)
