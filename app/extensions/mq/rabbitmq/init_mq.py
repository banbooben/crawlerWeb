#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/9/4 01:42
# @Author  : shangyameng@datagrand.com
# @Site    : 
# @File    : init_mq.py

import pika


class RabbitMqBase(object):

    def __init__(self, host, port, logger_item, username=None, password=None, ack=False,
                 persist=True):
        self.logger = logger_item
        self._connection = None
        self._channel = None
        self.username = username
        self.password = password

        self.host = host  # 主机
        self.port = port  # 端口
        self.ack = ack  # 是否开启消息手动确认机制, 默认是自动确认机制
        self.persist = persist  # 消息是否持久化
        # self.exchange = exchange  # 交换机名称
        # self.exchange_type = exchange_type  # 交换机类型

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._channel and self._channel.close():
            self.close()
        else:
            self.logger.info("已关闭！")

    def connect(self):
        # 连接mq
        if self.username and self.password:
            credentials = pika.PlainCredentials(username=self.username, password=self.password)
        else:
            credentials = None
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials
                                               ) if credentials else pika.ConnectionParameters(
                                                host=self.host, port=self.port)
        try:
            connection = pika.BlockingConnection(parameters=parameters)
            channel = connection.channel()
        except Exception as e:
            self.logger.exception(e)
            connection, channel = None, None

        self._connection, self._channel = connection, channel

    def close(self):
        self._connection.close()

    def create_exchange(self, exchange_name, exchange_type):
        """
        注册一个交换机
        Args:
            exchange_name: 交换机名称
            exchange_type: 交换机类型

        Returns:

        """
        self._channel.exchange_declare(exchange=exchange_name,
                                       type=exchange_type)

    def push(self, queue_name: str, message='', exchange=''):
        self._channel.queue_declare(queue=queue_name)
        self._channel.basic_qos(prefetch_count=1)

        properties = pika.BasicProperties(delivery_mode=(2 if self.persist else 0))
        self._channel.basic_publish(exchange=exchange,
                                    routing_key=queue_name,
                                    body=message,
                                    properties=properties)

    def get(self, queue_name, func=None):
        if not func:
            func = self.callback
        self._channel.basic_consume(func,
                                    queue=queue_name,
                                    no_ack=True)

        self._channel.start_consuming()

    def callback(self):
        self.logger.info("start compare the message")
