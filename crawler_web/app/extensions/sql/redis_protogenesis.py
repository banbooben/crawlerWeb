#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/20 22:18
# @Author  : shangyameng@datagrand.com
# @Site    : 
# @File    : redis_protogenesis.py

import redis

from app.common.application import cache_redis


# @Singleton

class RedisPool(object):
    pool = None

    def __init__(self, cache_host="localhost", cache_port=6379, decode_responses=True):
        self.host = cache_host
        self.port = cache_port
        # self.db = db
        self.decode_responses = decode_responses
        if not hasattr(RedisPool, "pool"):
            self.pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=decode_responses)

    #     if hasattr(self, self.pool):
    #         RedisPool.connect_poll(self.host, self.pool, self.decode_responses)
    #
    # @staticmethod
    # def connect_poll(host, port, decode_responses):
    #     return redis.ConnectionPool(host=host, port=port, decode_responses=decode_responses)


#
# class Redis(object):
#     def __init__(self, connect_pool, cache_db=0):
#         self.connect_pool = connect_pool
#         self.db = cache_db
#
#     def connect(self):
#         return redis.Redis(self.connect_pool, self.db)


class Redis(object):
    def __init__(self, cache_host="localhost", cache_port=6379, cache_db=0, password=None, decode_responses=True):
        self.host = cache_host
        self.port = cache_port
        self.db = cache_db
        self.password = password
        self.decode_responses = decode_responses
        # self.pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=self.decode_responses)
        # self.redis = redis.Redis(connection_pool=self.pool)
        # self.redis = self.connect()

    def connect(self):
        return redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password,
                           decode_responses=self.decode_responses)


#
#     # def
#     def status(self):
#         # edis.StrictRedis(host='localhost', port=6379, db=0)
#         pass
if __name__ == "__main__":
    # host, port, db = get_redis_config(config[current_environment])
    # print(host, port, db)
    # # redis_pool = RedisPool(host, port).connectPoll()
    # cache = Redis(host, port, db).connect()
    cache_redis.set("test", "123")
    print(cache_redis.keys())
    print(cache_redis.get("test"))
