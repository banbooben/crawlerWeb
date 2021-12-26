#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 18:39
# @Author  : shangyameng@datagrand.com
# @Site    :
# @File    : idps_api.py

import json
import os
import re
import uuid

from application.extensions.idps_tools.base import IdpsToolsBase


# from flask_app.common.common_functions import base64decode


# from API.idps_databse import IdpsDatabaseTools


class IdpsTools(IdpsToolsBase):

    def get_review_height_files(self, review_id, save_path):
        new_path = ""
        resp = self._requests_processor(url=f"{self.url_get_check_height}/{review_id}")
        if path := resp.get("path", ""):
            if path.startswith("upload"):
                new_path = self._request_and_download_files(path, save_path)

        return new_path

    def _request_and_download_files(self, path, save_path):
        new_path = ""
        url = f"{self.host}/{path}"
        files_data = self._requests_processor_content(url=url)
        if files_data.status_code == 200:
            new_path = os.path.join(save_path, os.path.basename(path))
            try:
                with open(new_path, "wb") as f:
                    f.write(files_data.content)
            except Exception as e:
                self.logger.exception(e)
        return new_path

    def get_diff_height_files(self, diff_ids, save_path):
        params = {
            "docs_diff_ids": diff_ids
        }
        new_path = ""
        resp = self._requests_processor(self.url_get_diff_height, params=params)
        if path := resp.get("path", ""):
            if path.startswith("/share_data"):
                new_path = self._request_and_download_files(path, save_path)
        return new_path

    def get_check_result(self, check_id):
        url = self.url_check + f"/{check_id}"
        result = self._requests_processor(url)
        return result

    def create_check(self, file_path, tag_type_id, check_point_id_list, async_task="true"):
        self.logger.info(f"start request idps check API.\t{os.path.basename(file_path)}")
        file = [('fileList', (open(file_path, 'rb')))]
        params = {
            "data": json.dumps({
                "tag_type_id": int(tag_type_id),
                "check_point_id_list": check_point_id_list
            }),
            "async_task": async_task,
        }
        result = self._requests_processor(self.url_check,
                                          method="POST",
                                          data=params,
                                          files=file,
                                          headers=self.headers)
        return result

    def get_diff_result(self, diff_id, skip_spin="true"):
        url = self.get_diff_tasks + f"/{diff_id}?skipSpin={skip_spin}"
        result = self._requests_processor(url)
        return result

    def create_diff_task(self,
                         file_path1,
                         file_path2,
                         feature_type_id: str,
                         diff_rules: list,
                         async_task: str = "true"):
        """
        发起比对任务
        Args:

        Returns:

        """
        self.logger.info(f"start request idps diff API.\t{os.path.basename(file_path1)}")
        file = (("files", open(file_path1, 'rb')), ("files", open(file_path2, 'rb')))
        diff_rules_str = "&".join([f"diff_rules={item}" for item in diff_rules])
        diff_url = self.diff_tasks + f"?feature_type_id={feature_type_id}&async_task={async_task}&{diff_rules_str}"
        result = self._requests_processor(diff_url,
                                          method="POST",
                                          files=file,
                                          headers=self.headers)
        return result

    def create_table_parse(self,
                           file_path,
                           feature_type_id: str,
                           async_task: str = "false"):
        """
        发起表格解析任务
        Args:

        Returns:

        """
        # self._login_by_user()
        self.logger.info(f"start request idps table_parse API.\t{os.path.basename(file_path)}")
        file = (("file", open(file_path, 'rb')), ("file", open(file_path, 'rb')))
        params = {
            "feature_type_id": int(feature_type_id),
            "async_task": async_task,
            "financial_type": "normal"
        }
        result = self._requests_processor(self.table_tasks,
                                          method="POST",
                                          params=params,
                                          files=file,
                                          headers=self.headers)
        return result

    def get_all_feature_type(self, kwargs):
        result = self._requests_processor(url=self.url_feature_type,
                                          method='GET',
                                          params=kwargs,
                                          data={})
        return result

    def get_all_user_info(self):
        result = self._requests_processor(url=self.url_get_users +
                                              '?start=0&number=1000000&status=1',
                                          method='GET',
                                          data={})
        user_id_dict = {
            i['username']: i['id']
            for i in result.get('items', [])
        }
        return user_id_dict

    def create_user(self, username, password, role_id_list):
        headers = {}
        headers.update(self.headers)
        headers.update({"Content-Type": "application/json"})
        data = {
            "nickname": base64decode(username),
            "username": username,
            "password": password,
            "role_ids": role_id_list,
            "group_ids": [1],
        }
        response = self._requests_processor(self.url_create_user,
                                            method="POST",
                                            headers=headers,
                                            json=data)
        return response

    def create_role(self, role_name, desc=''):

        headers = {}
        headers.update(self.headers)
        headers.update({"Content-Type": "application/json"})
        data = {"role_name": role_name, "desc": desc}
        response = self._requests_processor(self.url_create_role,
                                            method="POST",
                                            headers=headers,
                                            json=data)
        return response

    def update_role_menu(self, role_id):
        headers = {}
        headers.update(self.headers)
        headers.update({"Content-Type": "application/json"})
        url = self.url_set_role_menu + f"/{role_id}"
        data = {"menu_ids": [3, 10, 11, 12, 16, 17, 18, 24, 23, 27, 41, 42]}
        response = self._requests_processor(url,
                                            method="PUT",
                                            headers=headers,
                                            json=data)
        return response

    def reset_password(self, username, new_password):
        result = self._requests_processor(
            url=self.host + '/api/userlist?start=0&number=10000&status=1',
            method='GET',
            data={})
        user_id_dict = {
            i['username']: i['id']
            for i in result.get('items', [])
        }
        # self.logger.info(f"all_users id: {user_id_dict}, check user: {username}")
        user_id = user_id_dict.get(username)
        if not user_id:
            return False
        result_2 = self._requests_processor(
            url=self.host + '/api/auth/password/update/{}'.format(user_id),
            method='PUT',
            json={
                'password': new_password,
                'password2': new_password
            })
        if result_2.get("code", "") == 2000300 and result_2.get("status",
                                                                "") == 200:
            # self.password = new_password
            self.logger.info("密码修改：成功")
            return True
        else:
            self.logger.info("密码修改：失败")
            self.logger.info(result_2)
            return False

    def get_all_user(self, *args, **kwargs):
        response = self._requests_processor(self.url_get_users, *args,
                                            **kwargs)
        return response

    def get_all_roles(self, *args, **kwargs):
        response = self._requests_processor(self.url_get_roles, *args,
                                            **kwargs)
        return response

    # def get_all_diff_tasks(self, *args, **kwargs):
    #     response = self._requests_processor(self.diff_tasks, *args, **kwargs)
    #     return response

    def get_all_tasks(self, url, query, *args, **kwargs):
        if not query:
            query_str = self.default_query
        else:
            query_str = '&'.join(
                list([f"{key}={value}" for key, value in query.items()]))
        response = self._requests_processor(url + f"?{query_str}", *args,
                                            **kwargs)
        return response

    def create_extract_task(self,
                            file_path,
                            doc_type_id: int,
                            feature_type_id: str,
                            async_task="false",
                            ocr=True):
        """
        发起抽取任务
        Args:
            file_path: 文件位置
            doc_type_id: 文档类型名字
            ocr: 是否使用OCR

        Returns:

        """
        # self._login_by_user()
        self.logger.info(
            f"start request idps extract API.\t{os.path.basename(file_path)}")
        # if type_name.isdecimal():
        #     type_id = type_name
        # else:
        #     type_id, tags = self.get_tag_id_and_tags_by_tag_name(type_name)

        ocr = 2 if ocr else 1
        ocr = 1 if file_path.rsplit(".")[-1] in ["doc", "docx", "txt"] else ocr
        type_id = doc_type_id if doc_type_id else 1
        file = {"files": open(file_path, 'rb')}
        params = {
            "doc_type_id": int(type_id),
            "feature_type_id": int(feature_type_id),
            "async_task": async_task,
            "file_types": [ocr],
        }
        result = self._requests_processor(self.extract_url,
                                          method="POST",
                                          params=params,
                                          files=file,
                                          headers=self.headers)
        return result

    def get_table_extract_result(self, feature_type_id):
        """
        根据任务ID获取表格解析结果
        Args:
            feature_type_id: 任务ID

        Returns:
            表格解析返回的结果
        """
        # self._login_by_user()
        url = self.get_table_result_url + feature_type_id
        result = self._requests_processor(url)
        return json.loads(result.content.decode("utf-8")) if result else None

    def get_tag_id_and_tags_by_tag_name(self, tag_name):
        """
        根据传入的tag_name获取该类型对应的ID
        Args:
            tag_name: 文档类型名字

        Returns:
            文档类型的ID
        """

        # self._login_by_user()
        result = self._get_all_tag_types()
        all_tags = result.get("items", None) if result else None
        tag_type_id_list = [(item["id"], item["tags"]) for item in all_tags
                            if item["name"] == tag_name] if all_tags else None
        type_id = tag_type_id_list[0][0] if tag_type_id_list else None
        fields = tag_type_id_list[0][1] if tag_type_id_list else None
        return type_id, fields

    def get_extract_result(self, task_id):
        return self._requests_processor(
            url=f"{self.get_extract_res_url}/{task_id}", headers=self.headers)

    # def request_ocr_url(self, file_path):
    #     """
    #     直接调用ocrd营业执照接口
    #     :param file_path:
    #     :return:
    #     """
    #     self.logger.info(f"start request OCR API.\t{os.path.basename(file_path)}")
    #     file = {"file": open(file_path, 'rb')}
    #     result = self._requests_processor(self.bizlicense, method="POST", file=file)
    #     return json.loads(result.content.decode("utf-8")) if result else None


if __name__ == "__main__":
    file_path = "/Users/sarmn/Desktop/aaa.png"
    file2_path = "/Users/sarmn/Desktop"
    diff_rules = ["filter_blank", "filter_punc", "filter_header_footer", "filter_other_char"]
    idps_tools_ = IdpsTools()
    file_path = '/Users/sarmn/work_speace/smfg/smfg_api/flask_app/static/upload/535c9fdb-ac5a-490d-bd50-e35de809f637/draft_file/535c9fdb-ac5a-490d-bd50-e35de809f637_draft_file.pdf'
    tag_type_id = "133"
    check_point_id_list = [8]
    async_task = True
    # response = idps_tools_.create_diff_task(file_path, file2_path, "87", diff_rules)
    docs_diff_ids = 1
    review_id = 12
    response = idps_tools_.get_review_height_files(review_id, file2_path)
    print(response)
