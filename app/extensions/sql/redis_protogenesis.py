#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/20 22:18
# @Author  : shangyameng@datagrand.com
# @Site    : 
# @File    : redis_protogenesis.py

from redis import Redis, StrictRedis, ConnectionPool
from redis.sentinel import Sentinel
from typing import List, Tuple
import re
import redis
from common.decorators import singleton

from conf.server_conf import get_redis_config, current_config


# @singleton
# class RedisPool(object):
#
#     def __init__(self, cache_host="localhost", cache_port=6379, decode_responses=True, password=None):
#         self.host = cache_host
#         self.port = cache_port
#         # self.db = db
#         self.password = password
#         self.decode_responses = decode_responses
#         self.connect_poll = self.connect_poll()
#
#     def connect_poll(self):
#         return redis.ConnectionPool(host=self.host,
#                                     port=self.port,
#                                     password=self.password,
#                                     decode_responses=self.decode_responses)
#

@singleton
class Redis(object):
    def __init__(self, redis_conf):
        self.host = redis_conf.get("host")
        self.port = redis_conf.get("port")
        self.password = redis_conf.get("password")
        self.db = redis_conf.get("db")
        self.decode_responses = redis_conf.get("decode_responses")
        self.redis_pool = self._connect_pool()
        self.cache = self._connect()

    def _connect_pool(self):
        return ConnectionPool(host=self.host,
                              port=self.port,
                              password=self.password,
                              decode_responses=self.decode_responses)

    def _connect(self):
        return StrictRedis(connection_pool=self.redis_pool, db=self.db)

    def _create_sentinel_redis(self, config: dict) -> Tuple[Redis, Redis]:
        """
        创建一个Redis的主从链接
        :param config:
        :return:
        """

        def _parse_host(val: str) -> List[Tuple[str, int]]:
            """
            @attention: 分解host,把10.1.113.158-26379分割为("10.1.113.158",26379)
            """
            info = re.findall(r"([\d\.]+)-(\d+)", val)
            return [(item[0], int(item[1])) for item in info]

        host_port = _parse_host(config["host-port"])
        sentinel = Sentinel(host_port, socket_timeout=2, password=config['pwd'], db=config['db'])
        master = sentinel.master_for('mymaster', socket_timeout=5)
        slave = sentinel.slave_for('mymaster', socket_timeout=2)
        return master, slave


if __name__ == '__main__':
    """
    数据库管理配置参数
    """

    redis_config = get_redis_config(current_config)

    # cache_pool = RedisPool(host, port, decode_responses, redis_password).connect_poll
    cache = Redis(redis_config)
    cache2 = Redis(redis_config)
    print(cache.cache is cache2.cache)
    # cache.set("age", 88)
    # print(cache.get("age"))
