#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 13:23
# @Author  : cst
# @FileName: mq_producer.py
# @Software: PyCharm
# @Describe:rabbitmq 生产者生成数据
from src.until.rabbitmq_utils import RabitMq


def send_json(data, key, exchange='topic-exchange'):
    """
    发送json数据到队列中，
    :param data: json数据
    :param key: 队列名称
    :param exchange: 交换机类型
    :return:
    """
    RabitMq().send_json(data, exchange=exchange, key=key)
    return 'ok'
