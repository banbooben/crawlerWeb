#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/21 17:19
# @Author  : WangLei
# @FileName: rabbitmq_utils.py
# @Software: PyCharm
from flask_rabbitmq import RabbitMQ
from src.until.mq_queue import queue
import pika


class RabitMq(RabbitMQ):
    def __init__(self, app=None):
        self.queue = queue
        self.app = app
        self.config = app.config
        self.rabbitmq_server_host = None
        self.rabbitmq_server_username = None
        self.rabbitmq_server_password = None
        self._connection = None
        self._channel = None
        self._rpc_class_list = []
        self.data = {}
        # initialize some operation
        self.init()

    def init(self):
        self.valid_config()
        try:
            self.connect_rabbitmq_server()
        except Exception as e:
            print("MQ连接报错:", e)

    def valid_config(self):
        if not self.config.get('RABBITMQ_HOST'):
            raise Exception("The rabbitMQ application must configure host.")
        self.rabbitmq_server_host = self.config.get('RABBITMQ_HOST')
        self.rabbitmq_server_username = self.config.get('RABBITMQ_USERNAME')
        self.rabbitmq_server_password = self.config.get('RABBITMQ_PASSWORD')
        self.rabbitmq_v_host = self.config.get('RABBITMQ_VHOST')

    def connect_rabbitmq_server(self):
        if not (self.rabbitmq_server_username and self.rabbitmq_server_password):
            # connect RabbitMQ server with no authentication
            self._connection = pika.BlockingConnection()
        elif (self.rabbitmq_server_username and self.rabbitmq_server_password):
            # connect RabbitMQ server with authentication
            credentials = pika.PlainCredentials(
                self.rabbitmq_server_username,
                self.rabbitmq_server_password,
            )
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    self.rabbitmq_server_host,
                    credentials=credentials,
                    virtual_host=self.rabbitmq_v_host
                ))
        else:
            raise Exception()
        # create channel object
        self._channel = self._connection.channel()

    #
    def run_with_flask_app(self, host="localhost", port=5000):
        try:
            super()._run()
        except Exception as e:
            print("MQ连接报错:", e)
        self.app.run(host, port)
