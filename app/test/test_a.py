#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/10 4:24 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : test_a.py
# @desc    :

import os
from extensions.idps_tools import IdpsTools


idps_tools_ = IdpsTools()
path = "/Users/sarmn/varfile/doc_transform"
url = "https://idps2-qyfw2.test.datagrand.cn/"

all_files = ""
n = len(os.listdir(path))
print(n)
for ind, file in enumerate(os.listdir(path)):
    abs_path = os.path.join(path, file)
    res = idps_tools_.create_request_by_single_file(abs_path, "47", ocr=False)
    pdf_path = res.get("result", {}).get("pdf_path", "")
    if "." in pdf_path:
        json_path = url + "/" + pdf_path.replace(".pdf", "_all.json")
    else:
        json_path = ''
    all_files += f"{file},{json_path}\n"
    print(f"{ind}/{n}:::   {file}")

with open("./all.json", "w", encoding="utf-8") as f:
    f.write(all_files)






