#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 12:47
# @Author  : cst
# @FileName: mq_consumer.py
# @Software: PyCharm
# @Describe: rabbitmq消费者获取数据

from src.until.mq_queue import queue
from flask_rabbitmq import ExchangeType


# @queue()
# def simple_queue(ch, method, props, body):
#     print("simple queue => {}".format(body))

# @queue(type=ExchangeType.DEFAULT, queue="default_exchange")
# def default(ch, method, props, body):
#     print("default queue => {}".format(body))


# @queue(type=ExchangeType.FANOUT, exchange='fanout_exchange')
# def fanout(ch, method, props, body):
#     print("fanout queue => {}".format(body))
# 抓拍数据回调
# @queue(type=ExchangeType.DIRECT, exchange="SF.EGC_SNAPINFO", routing_key="productEagle_subscribe_sf_snapInfo")
# def direct_key1(ch, method, props, body):
#     print("抓拍数据回调 => {}".format(body))
# # 设备连接状态回调
@queue(type=ExchangeType.DEFAULT, queue='productEagle_subscribe_sf_snapInfo')
def snapInfo(ch, method, props, body):
    print("设备连接状态回调 => {}".format(body))


@queue(type=ExchangeType.DEFAULT, queue='productEagle_subscribe_sf_heartstate')
def heartstate(ch, method, props, body):
    print("设备连接状态回调 => {}".format(body))

# @queue(type=ExchangeType.TOPIC, exchange='topic-exchange', routing_key='1')
# def topic(ch, method, props, body):
#     print("topic queue 1=> {}".format(body))
#
# @queue(type=ExchangeType.TOPIC, exchange='topic-exchange', routing_key='2')
# def topic(ch, method, props, body):
#     print("topic queue 2=> {}".format(body))
#
# @queue(type=ExchangeType.TOPIC, exchange='topic-exchange', routing_key='wl')
# def topic(ch, method, props, body):
#     print("topic queue test=> {}".format(body))
