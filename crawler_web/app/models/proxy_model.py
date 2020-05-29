#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Project : crawler_web
# @File    : proxy_model.py
# @Author  : shangyameng@datagrand.com
# @Time    : 2020/4/24 10:15
# @desc: 

from sqlalchemy import UniqueConstraint
from app.extensions import db

proxy_fields = ["url", "port", "net_type", "address", "anonymity", "speed", "connect_time"]


class Proxy(db.Model):
    __tablename__ = "proxy"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(18))
    port = db.Column(db.String(10))
    net_type = db.Column(db.String(10))
    address = db.Column(db.String(12))
    anonymity = db.Column(db.String(10))
    speed = db.Column(db.String(10))
    connect_time = db.Column(db.String(10))

    def __init__(self):
        self.url = None
        self.port = None
        self.net_type = None
        self.address = None
        self.anonymity = None
        self.speed = None
        self.connect_time = None

    def get_all_field_name(self):
        res = ["{}".format(self.url), "{}".format(self.port), "{}".format(self.net_type), "{}".format(self.address),
               "{}".format(self.anonymity), "{}".format(self.speed), "{}".format(self.connect_time)]
        return res
