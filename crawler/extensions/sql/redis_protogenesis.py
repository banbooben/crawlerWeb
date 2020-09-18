#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/20 22:18
# @Author  : shangyameng@datagrand.com
# @Site    : 
# @File    : redis_protogenesis.py

import redis

# from common.application import cache_redis
from common.decorators import singleton

from conf.server_conf import get_redis_config, current_config


@singleton
class RedisPool(object):

    def __init__(self, cache_host="localhost", cache_port=6379, decode_responses=True, password=None):
        self.host = cache_host
        self.port = cache_port
        # self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self.connect_poll = self.connect_poll()

    def connect_poll(self):
        return redis.ConnectionPool(host=self.host,
                                    port=self.port,
                                    password=self.password,
                                    decode_responses=self.decode_responses)


class Redis(object):
    def __init__(self, connect_pool, cache_db=0):
        self.connect_pool = connect_pool
        self.db = cache_db

    def connect(self):
        return redis.Redis(connection_pool=self.connect_pool, db=self.db)


if __name__ == '__main__':
    """
    数据库管理配置参数
    """

    host, port, database, decode_responses, redis_password, cache_type = get_redis_config(current_config)
    print(host, port, database, decode_responses, redis_password, cache_type)

    cache_pool = RedisPool(host, port, decode_responses, redis_password).connect_poll
    cache = Redis(cache_pool, database).connect()
