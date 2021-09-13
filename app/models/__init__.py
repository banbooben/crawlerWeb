# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:48 下午
# @Contact : shangyameng
# @Name    : __init__.py.py
# @Desc    :


from initialization.extensions import db


class BaseModel(db.Model):
    pass
