#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/22 11:40
# @Author  : shangyameng@aliyun.com
# @Site    :
# @File    : user.py

from extensions import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(18))
    password = db.Column(db.String(10))
    status = db.Column(db.Boolean)
    # net_type = db.Column(db.String(10))
    # address = db.Column(db.String(12))
    # anonymity = db.Column(db.String(10))
    # speed = db.Column(db.String(10))
    # connect_time = db.Column(db.String(10))


