#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 5:48 下午
# @Author  : shangyameng@aliyum.com
# @Site    : 
# @File    : aria_route.py

from flask import render_template
from . import aria


@aria.route('/')
def hello():
    print(aria.static_url_path)
    return aria.send_static_file("index.html")
    # return render_template("index.html")
