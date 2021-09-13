#!/usr/bin/env python

# coding:utf-8
# @Time    : 2020/12/27 0:51
# @Contact : shangyameng@aliyun.com
# @Name    : redis_tools.py
# @Desc    :


from redis import Redis, StrictRedis, ConnectionPool
from redis.sentinel import Sentinel
from typing import List, Tuple
import re

# from common.decorators import singleton
from common.common_conf import get_redis_config
from config.server_conf import current_config


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

# @singleton
class RedisBase(object):
    def __init__(self, redis_conf):
        self.host = redis_conf.get("host", "127.0.0.1")
        self.port = redis_conf.get("port", 6379)
        self.password = redis_conf.get("password", "")
        self.db = redis_conf.get("db", 0)
        self.decode_responses = redis_conf.get("decode_responses", True)
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


# @singleton
class Redis(RedisBase):
    def __init__(self, redis_conf):
        super(Redis, self).__init__(redis_conf)

    def set(self, *args, **kwargs):
        self.cache.set(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.cache.get(*args, **kwargs)

    def lpush(self, *args, **kwargs):
        self.cache.lpush(*args, **kwargs)

    def lpop(self, *args, **kwargs):
        return self.cache.lpop(*args, **kwargs)


# __all__ = [Redis]

if __name__ == '__main__':
    """
    数据库管理配置参数
    """

    redis_config = get_redis_config(current_config.REDIS_CONF)
    # redis_config = current_config.REDIS_CONF

    # cache_pool = RedisPool(host, port, decode_responses, redis_password).connect_poll
    ch = Redis(redis_config)
    # cache2 = Redis(redis_config)
    # print(cache.cache is cache2.cache)
    ch.set("age", 88)
    print(ch.get("age"))
    print("ok")
