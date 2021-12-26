# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/27 12:00 上午
# @Name    : rsync_process.py
# @Desc    :


class RsyncProcess(object):

    def __init__(self, redis, config):
        self.redis = redis(config)

    def start(self):
        pass
