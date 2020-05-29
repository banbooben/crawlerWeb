#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Project : crawler_web
# @File    : dytt_model.py
# @Author  : shangyameng@datagrand.com
# @Time    : 2020/4/23 16:52
# @desc:

from sqlalchemy import UniqueConstraint
from app.extensions import db

dyHeaven_fields = ["name", "classify", "title", "date", "size", "introduction", "magnet"]


class DyHeaven(db.Model):
    __tablename__ = "dytt"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(24))
    classify = db.Column(db.String(10))
    title = db.Column(db.String(24))
    date = db.Column(db.String(10))
    size = db.Column(db.String(8))
    introduction = db.Column(db.String(32))
    magnet = db.Column(db.String(1024))

    def __init__(self):
        self.name = None
        self.classify = None
        self.title = None
        self.date = None
        self.size = None
        self.introduction = None
        self.magnet = None

    def get_all_field_name(self):
        res = ["{}".format(self.name), "{}".format(self.classify),
               "{}".format(self.title), "{}".format(self.date),
               "{}".format(self.size), "{}".format(self.introduction),
               "{}".format(self.magnet)]
        return res
