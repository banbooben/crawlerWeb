#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-08-05 23:50:27
# @LastEditTime: 2021-08-05 23:55:07
# @FilePath: \flask\app\utils\requests_tools.py

import json

from requests import request
from tenacity import (retry, retry_if_exception_type, retry_if_result,
                      stop_after_attempt, wait_random, RetryError)


def _value_is_none(value):
    return value is None


class RequestTools(object):
    @retry(retry=(retry_if_result(_value_is_none)),
           wait=wait_random(min=0, max=3),
           stop=stop_after_attempt(6),
           reraise=True)
    def common_request(self, url, method="GET", **kwargs):
        """
        request请求，
        如果请求返回的数据为None，重复请求6次，直到获取到数据，否侧报错抛出
        Args:
            url:
            method:
            **kwargs:

        Returns:

        """
        send_review_request = request(method=method, url=url, **kwargs)
        if send_review_request.status_code == 401:
            return "{}"
            # return common_request(url=url, method=method, *args, **kwargs)
        else:
            result = send_review_request if send_review_request is not None else None
            result = send_review_request
            return result
            # return None

    @retry(retry=retry_if_exception_type(json.JSONDecodeError),
           stop=stop_after_attempt(3),
           reraise=True)
    def common_request_to_json(self, url, method="GET", **kwargs):
        """
        请求到的数据，转换为json格式
        Args:
            url:
            method:
            **kwargs:

        Returns:

        """
        try:
            response_str = self.common_request(url, method, **kwargs).content.decode('utf-8')
        except Exception as e:
            if isinstance(e, RetryError):
                response_str = None
            response_str = "{}"
        res = json.loads(response_str)
        return res


request_tools_ = RequestTools()

if __name__ == "__main__":
    import requests

    url = "http://document_process:8000/rich_content"

    payload={'file': '/share_data/doc_transform/4115光证资管-定存宝8号定向资产管理计划-jxy-定向资产管理合同.pdf',
             'params': '{"detect_title": true, "detect_table": true, "detect_graph": false, "detect_header_footer": true}'}
    files=[]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

