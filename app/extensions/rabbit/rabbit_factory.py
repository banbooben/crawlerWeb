#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/9 18:22
# @Author  : shangyameng
# @Email   : shangyameng@datagrand.com
# @Site    :
# @File    : rabbit_factory.py
# @desc    :


class ConnectionFactory(object):
    # def __init__(self, conf, rabbit_class, logger_item):
    #     self.rabbit_conf = conf
    #     self.rabbit_class = rabbit_class
    #     self.logger = logger_item
    def __init__(self):
        self._username = ""
        self._password = ""
        self._host = ""
        self._port = ""

    def set_username(self, username):
        self._username = username

    def set_password(self, passwd):
        self._password = passwd

    def set_host(self, host):
        self._host = host

    def set_port(self, port):
        self._port = port

    def create(self,
               rabbit_class,
               username=None,
               password=None,
               host=None,
               port=None):
        if username:
            self.set_username(username)
        if password:
            self.set_password(password)
        if host:
            self.set_host(host)
        if port:
            self.set_port(port)

        rabbit_item = rabbit_class(username, password, host, port)
        # rabbit_item.connect()
        return rabbit_item
