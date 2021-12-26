#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/21 12:04
# @Author  : shangyameng@datagrand.com
# @Site    :
# @File    : base.py

# from flask_app.conf.api_config import *

from functools import wraps
import os
import json
import base64
from pathlib import Path
import requests
from requests import request
from tenacity import retry, retry_if_exception_type, retry_if_result, stop_after_attempt, wait_random, RetryError

from loguru import logger


def _value_is_none(value):
    return value is None


class IdpsToolsBase(object):
    access_token = ""
    headers = {}
    #     {
    #     "User-Agent":
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    # }

    def __init__(
        self,
        username="superadminpro",
        password="BEgPDsMumFlc",
        host="http://idps2-smfg.datagrand.cn",
        port="80",
        re_try=3,
        product=True,
    ):
        self.re_try = re_try
        self.username = base64.b64encode(username.encode()).decode()
        self.password = base64.b64encode(password.encode()).decode()
        self.product = product
        self.host = f"{host}:{port}"
        self.logger = logger
        self.feature_type_id = "?id=158"
        self.tag_types_key = "?start=0&number=1000"

        self.logon_url = f'{self.host}/{"api/login"}'

        self.upload_url = f"{self.host}/upload"

        # 抽取
        self.extract_url = f'{self.host}/{"api/extracting/v2/task"}'
        self.get_extract_res_url = f"{self.host}/api/extracting/v2"

        self.tag_types_url = f"{self.host}/api/tag_types"

        self.default_query = "start=0&number=100000&time_sort=0&skipSpin=false"

        # 表格
        self.table_tasks = f"{self.host}/api/table/task"
        self.get_table_result_url = f'{self.host}/{"api/web_api/table/"}'
        self.create_table_task = ''

        # 比对
        self.diff_tasks = f'{self.host}/api/diff/new/history'
        self.get_diff_tasks = f'{self.host}/api/diff/history'

        self.url_get_diff_height = f"{self.host}/api/diff/export"
        # self.create_diff_task_params = {
        #     "async_task": "false",
        #     "feature_type_id": "false",
        #     # "diff_rules": "filter_blank",
        #     # "diff_rules": "filter_punc",
        #     # "diff_rules": "filter_header_footer",
        #     # "diff_rules": "filter_other_char",
        #     }

        # 审核
        self.url_check = f"{self.host}/api/review"
        self.url_get_check_height = f"{self.host}/api/review/export"

        # 前端卡片接口
        self.url_feature_type = f"{self.host}/api/doc_type/feature_type"

        # 用户、群组管理
        self.url_create_group = f'{self.host}/api/auth/groups'

        self.url_create_role = f"{self.host}/api/auth/rolelist"
        self.url_get_roles = f"{self.host}/api/auth/rolelist"
        self.url_set_role_menu = f"{self.host}/api/auth/rolemenu"

        self.url_create_user = f"{self.host}/api/auth/userlist"
        self.url_get_users = f"{self.host}/api/auth/userlist"

        self.all_tags = []




    # @staticmethod
    def _login_by_user(self):
        """
        登录系统
        Returns:

        """
        if self.logon_url:
            data = {"username": self.username, "password": self.password}
            request_result = requests.post(url=self.logon_url,
                                           data=data,
                                           headers=self.headers)
            if request_result.status_code == 200:
                result = json.loads(request_result.text)
                if result:
                    self.access_token = "Bearer " + result.get(
                        "access_token", None)
                    self.headers.update({"Authorization": self.access_token})
                    return "登录成功"
            return "登录失败"
        return "缺少登录地址"

    def _get_all_filed_id_and_name(self):
        self._login_by_user()
        all_doctype = self._get_all_tag_types()
        all_doctype = all_doctype.get("items") if all_doctype else None
        all_tags = {}
        if all_doctype:
            for item in all_doctype:
                item_tags = {}
                doctype = item["id"]
                if item["tags"]:
                    [
                        item_tags.update({str(field["id"]): field["name"]})
                        for field in item["tags"]
                    ]
                all_tags.update({doctype: item_tags}) if item_tags else None
        return all_tags

    def _get_all_tag_types(self):
        """
        获取所有的文档类型信息
        Returns:
            所有文档类型信息，ID、name、tags等
        """
        self._login_by_user()
        url = self.tag_types_url + self.tag_types_key
        result = self._requests_processor(url)
        return json.loads(result.content.decode("utf-8")) if result else None

    @retry(retry=(retry_if_result(_value_is_none)),
           wait=wait_random(min=0, max=3),
           stop=stop_after_attempt(6),
           reraise=True)
    def _requests_processor(self, url, method="GET", **kwargs):
        """
        request请求，
        如果请求返回的数据为None，重复请求6次，直到获取到数据，否侧报错抛出
        Args:
            url:
            method:
            **kwargs:

        Returns:

        """
        # if not self.headers:
        #     self._login_by_user()
        self._login_by_user()
        if not kwargs.get("headers", None):
            kwargs.update({"headers": self.headers})
        send_review_request = request(method=method, url=url, **kwargs)
        if send_review_request.status_code == 401:
            # self._login_by_user()
            response = request(method=method, url=url,
                               **kwargs).content.decode('utf-8')
            return json.loads(response)

        else:
            # result = send_review_request if send_review_request is not None else None
            # result = send_review_request.content.decode('utf-8')
            return json.loads(send_review_request.content.decode('utf-8'))
            # return None

    @retry(retry=(retry_if_result(_value_is_none)),
           wait=wait_random(min=0, max=3),
           stop=stop_after_attempt(6),
           reraise=True)
    def _requests_processor_content(self, url, method="GET", **kwargs):
        """
        request请求，
        如果请求返回的数据为None，重复请求6次，直到获取到数据，否侧报错抛出
        Args:
            url:
            method:
            **kwargs:

        Returns:

        """
        # if not self.headers:
        #     self._login_by_user()
        self._login_by_user()
        if not kwargs.get("headers", None):
            kwargs.update({"headers": self.headers})
        send_review_request = request(method=method, url=url, **kwargs)
        if send_review_request.status_code == 401:
            # self._login_by_user()
            response = request(method=method, url=url,
                               **kwargs).content.decode('utf-8')
            return response

        else:
            # result = send_review_request if send_review_request is not None else None
            # result = send_review_request.content.decode('utf-8')
            return send_review_request
            # return None


    def _save_file(self, file_text, file_name: str, json_save_path: str,
                   file_type: str):
        if file_text and json_save_path and os.path.exists(json_save_path):
            self.logger.info(f"start download {file_name}")

            if file_type == "pdf":
                write_type = "wb"
            else:
                write_type = "w"
                file_text = file_text.decode("utf-8")
            try:
                with open(os.path.join(json_save_path, file_name),
                          write_type) as f:
                    f.write(file_text)
                    self.logger.info(
                        f"{os.path.join(json_save_path, file_name)} is downloaded"
                    )
            except Exception as e:
                self.logger.info(e)
