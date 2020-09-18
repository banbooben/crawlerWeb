#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-09 21:57:10
# @LastEditTime: 2020-04-13 19:50:28
# @FilePath: /crawler_web/app/extensions/pyaria2c/aria2.py

import json
import requests
import re
import time
import uuid
from flask import current_app


class Aria2(object):
    def __init__(self,
                 host: str,
                 port: str,
                 rpc_token=None,
                 session_path=None):
        self.host = host
        self.port = port
        self.token = rpc_token
        self.url = self._init_aria2()

    def _init_aria2(self):
        """
        # @description: 初始化下载服务器信息
        # @param {type} 
        # @return: 
        """
        return "http://{}:{}/jsonrpc".format(self.host, self.port)

    def _request_post(self, request_data, headers=None):
        """

        Args:
            request_data:
            headers:

        Returns:

        """

        try:
            response = requests.post(url=self.url,
                                     data=json.dumps(request_data),
                                     headers=headers)
            response_data = json.loads(response.content.decode("utf-8"))
            current_app.logger.info("请求结果：{}".format(response_data))
            return {
                "code": response.status_code,
                "msg": "请求成功",
                "data": {
                    "id": response_data["id"],
                    "result": response_data["result"]
                }
            }
        except Exception as e:
            current_app.logger.error(e)
            return {"code": "400", "msg": "请求失败！请检查请求参数", "data": {}}

    def addUrl(self, download_url: str, rename=None, out_dir=None):

        # @description: 添加下载连接
        # @param {type}
        # @return:
        try:
            if not download_url:
                return {"code": 401, "msg": "缺少必要参数", "data": []}

            request_data = {
                "jsonrpc": "2.0",
                "method": "aria2.addUri",
                "id": str(uuid.uuid1()),
                "params": [[download_url], {}]
            }
            if self.token:
                request_data["params"].insert(0, "token:{}".format(self.token))
            if rename:
                request_data["params"][-1].update({"out": rename})
            if out_dir:
                request_data["params"][-1].update({"dir": out_dir})
            return self._request_post(request_data)
        except Exception as e:
            current_app.logger.error(e)

    def queryAllActiveInformation(self):

        # @description: 查询所有正在下载的文件
        # @param {type}
        # @return:
        try:
            request_data = {
                "jsonrpc":
                "2.0",
                "method":
                "aria2.tellActive",
                "id":
                str(uuid.uuid1()),
                "params": [[
                    "gid", "totalLength", "completedLength", "uploadSpeed",
                    "downloadSpeed", "connections", "numSeeders", "seeder",
                    "status", "errorCode", "verifiedLength",
                    "verifyIntegrityPending"
                ]]
            }
            if self.token:
                request_data["params"].insert(0, "token:{}".format(self.token))
            return self._request_post(request_data)
        except Exception as e:
            current_app.logger.error(e)

    def queryAllStoppedInformation(self):

        # @description: 查询所有已停止或已下载的文件
        # @param {type}
        # @return:
        try:
            request_data = {
                "jsonrpc":
                "2.0",
                "method":
                "aria2.tellStopped",
                "id":
                str(uuid.uuid1()),
                "params": [
                    -1, 1000,
                    [
                        "gid", "totalLength", "completedLength", "uploadSpeed",
                        "downloadSpeed", "connections", "numSeeders", "seeder",
                        "status", "errorCode", "verifiedLength",
                        "verifyIntegrityPending"
                    ]
                ]
            }
            if self.token:
                request_data["params"].insert(0, "token:{}".format(self.token))
            return self._request_post(request_data)
        except Exception as e:
            current_app.logger.error(e)

    def queryAllWaitingInformation(self):

        # @description: 查询所有暂停的文件
        # @param {type}
        # @return:
        try:
            request_data = {
                "jsonrpc": "2.0",
                "method": "aria2.tellWaiting",
                "id": str(uuid.uuid1()),
                "params": [-1, 1000, []]
            }
            if self.token:
                request_data["params"].insert(0, "token:{}".format(self.token))
            return self._request_post(request_data)
        except Exception as e:
            current_app.logger.error(e)

    def pauseAllDownloader(self):

        # @description: 开始所有下载的任务
        # @param {type}
        # @return:

        try:
            request_data = {
                "jsonrpc": "2.0",
                "method": "aria2.pauseAll",
                "id": str(uuid.uuid1()),
                "params": []
            }
            if self.token:
                request_data["params"].insert(0, "token:{}".format(self.token))
            return self._request_post(request_data)
        except Exception as e:
            current_app.logger.error(e)

    def unPauseAllDownloader(self):

        # @description: 暂停所有正在下载的任务
        # @param {type}
        # @return:

        try:
            request_data = {
                "jsonrpc": "2.0",
                "method": "aria2.unpauseAll",
                "id": str(uuid.uuid1()),
                "params": []
            }
            if self.token:
                request_data["params"].insert(0, "token:{}".format(self.token))
            return self._request_post(request_data)
        except Exception as e:
            current_app.logger.error(e)

    def pauseDownloader(self, id):

        # @description: 恢复指定下载的任务
        # @param {type}
        # @return:

        try:
            if id:
                request_data = {
                    "jsonrpc": "2.0",
                    "method": "aria2.pause",
                    "id": str(uuid.uuid1()),
                    "params": [id]
                }
                if self.token:
                    request_data["params"].insert(
                        0, "token:{}".format(self.token))
                return self._request_post(request_data)
            return {"code": 400, "msg": "没有相关任务", "data": {}}
        except Exception as e:
            current_app.logger.error(e)

    def unPauseDownloader(self, id):

        # @description: 暂停指定下载的任务
        # @param {type}
        # @return:

        try:
            if id:
                request_data = {
                    "jsonrpc": "2.0",
                    "method": "aria2.unpause",
                    "id": str(uuid.uuid1()),
                    "params": [id]
                }
                if self.token:
                    request_data["params"].insert(
                        0, "token:{}".format(self.token))
                return self._request_post(request_data)
            return {"code": 400, "msg": "没有相关任务", "data": {}}
        except Exception as e:
            current_app.logger.error(e)


if __name__ == "__main__":
    aria2c = Aria2("192.168.2.151", "6800", "sarmn.cn")
    res = aria2c.addUrl(
        "https://9uu33.com/20200411/115f916b6082c803581150ee315b4046.mp4")
    # res = aria2c.queryAllActiveInfomations()
    # res = aria2c.queryAllStoppedInfomations()
    # res = aria2c.queryAllWaitingInfomations()
    # print(res)
