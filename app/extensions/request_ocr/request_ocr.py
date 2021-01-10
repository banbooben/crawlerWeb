#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@datagrand.com
# @Date: 2020-07-22 11:11:38
# @LastEditTime: 2020-09-02 14:21:36
# @FilePath: /SuYan/flaskr/app/extensions/request_ocr/request_ocr.py

import requests
import json
import re
import os
import uuid
from PIL import Image, ImageGrab
import copy

from app.conf import logger
from app.conf.api_config import orientation
from app.extensions.opencv.open_cv import OpenCv


class RequestOcr(object):
    def __init__(self, save_file_path):
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
        self.ocr_url = "http://ysocr.datagrand.cn/ysocr/ocr"
        self.ocr_file = "http://ysocr.datagrand.cn/file/"
        self.bizlicense = "http://ysocr.datagrand.cn/ysocr/bizlicense_extract"
        self.uncompress_path = save_file_path
        self.save_path = os.path.join(self.uncompress_path, "ocr_split_files")
        self.orientation = orientation
        self.current_file = ""
        self.cv = OpenCv()
        self.logger = logger
        self.special_extract_info = {}
        self.check_uncompress_path()

    def check_uncompress_path(self):
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def _requests_processor(self,
                            url,
                            method="GET",
                            key_id="",
                            params=None,
                            file=None):
        """
        封装的请求方法
        Args:
            url:
            method:
            key_id:
            params:
            file:

        Returns:

        """
        try:
            url = f"{url}{key_id}"
            if method == "GET":
                send_review_request = requests.get(url, headers=self.headers)
            else:
                send_review_request = {
                    'PUT': requests.put,
                    'POST': requests.post,
                    'DELETE': requests.delete,
                }[method](url, headers=self.headers, data=params, files=file)
            if send_review_request.status_code == 401:
                return self._requests_processor(url=url,
                                                method=method,
                                                key_id=key_id,
                                                params=params,
                                                file=file)
            else:
                result = send_review_request.content if send_review_request else None
                return result
        except Exception as e:
            self.logger.error("error:{}".format(e))
            return None

    def create_url_by_ocr(self, file_abs_path):
        """
        创建ocr识别请求
        Args:
            file_abs_path: 请求需要的文件

        Returns:

        """
        try:
            self.logger.info("start request OCR API")
            file = {"file": open(file_abs_path, 'rb')}
            data = {"caller_request_id": uuid.uuid4()}
            result = self._requests_processor(self.ocr_url,
                                              method="POST",
                                              params=data,
                                              file=file)
            return json.loads(result.decode("utf-8"))

        except Exception as e:
            self.logger.error("error:{}".format(e))
            return None

    def find_extract_page(self, ocr_result: dict, orientation_dic: dict):
        """
        解析ocr识别出来的结果，通过关键字定位到需要拆分出来的页
        Args:
            ocr_result: OCR识别结果
            orientation_dic: 需要抽取出的页名字及关键字信息

        Returns:
            所有需要抽取的页及本地保存路径
        """
        self.logger.info("start dispose OCR recognition results")
        page_save_path = ""
        need_extract_info = {}
        if orientation_dic and ocr_result and ocr_result["code"] == 200:
            for page_info in ocr_result["img_data_list"]:
                all_page_txt = ''.join([
                    text_info["text_string"]
                    for text_info in page_info["text_info"]
                ])[:100]
                for key in orientation_dic.keys():
                    write_key = orientation_dic[key][0]
                    black_key = orientation_dic[key][1]

                    page_save_path = self.file_page_decision(
                        key, all_page_txt, orientation_dic, ocr_result,
                        write_key, black_key, page_info, need_extract_info)
                    if page_save_path and key == "leased_line":
                        break
                if page_save_path and "leased_line" in page_save_path:
                    break
        return need_extract_info

    def file_page_decision(self, key, all_page_txt, orientation_dic,
                           ocr_result, write_key, black_key, page_info,
                           need_extract_info):
        """
        根据黑白名单判定当前页是不是需要抽取出来的
        Args:
            key:
            all_page_txt:
            orientation_dic:
            ocr_result:
            write_key:
            black_key:
            page_info:
            need_extract_info:

        Returns:

        """
        if re.search(rf"(?:{'|'.join(write_key)})",
                     re.sub(r"[ ]", "", all_page_txt)):
            if black_key and re.search(
                    rf"(?:{'|'.join(orientation_dic[key][1])})",
                    re.sub(r"[ ]", "", all_page_txt)):
                return None
            else:
                if key == "leased_line":
                    image_name = ocr_result["out_pdf_name"]
                    page_number = ""
                else:
                    image_name = page_info["detect_img_name"]
                    page_number_info = re.findall(r"page_(\d+)_detection",
                                                  image_name)
                    page_number = page_number_info[
                        0] if page_number_info else None
                page_save_path = self.down_page_img(image_name, key,
                                                    page_number)

                if key not in need_extract_info.keys():
                    need_extract_info[key] = [page_save_path]
                else:
                    need_extract_info[key].append(page_save_path)
                return page_save_path
        return None

    def down_page_img(self, img_name, rename, page_number):
        """
        下载并保存图片
        Args:
            img_name: 图片保存的路径
            rename: 保存文件是重命名
            page_number: 第几页

        Returns:
            文件保存后路径
        """
        url = self.ocr_file + img_name
        self.logger.info(f"start download image: {url}")

        result = self._requests_processor(url)
        if img_name.rsplit(".", 1)[-1] == "pdf":
            suffix = ".pdf"
        else:
            suffix = ".jpeg"
        image_save_path = self.save_path + "/" + self.current_file.rsplit(
            ".", 1)[0] + "_" + rename + str(page_number) + suffix
        self.save_request_result(image_save_path, result, True)
        self.logger.info(f" image is downloaded! >>>  {image_save_path}")
        return image_save_path

    # @staticmethod
    def save_request_result(self, img_save_path, result, img=False):
        """
        将接口请求的数据保存到本地
        Args:
            img_save_path: 保存的文件路径
            result: 接口获取到的数据
            img: 是否是图片

        Returns:
            None
        """
        self.logger.info("start save request result")
        if not img:
            res_type = "w"
            result = json.dumps(result, ensure_ascii=False)
        else:
            res_type = "wb+"
        with open(img_save_path, f"{res_type}") as f:
            f.write(result)

    @staticmethod
    def read_extract_result(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            result = f.read()
            if result:
                return json.loads(result)
            return {}

    def request_bizlicense(self, all_file_info):
        """
        分类后的文件中请求获取营业执照的数据
        :param all_file_info:
        :return:
        """
        bizlicense_result = []
        try:
            if all_file_info:
                all_bizlicense = all_file_info["营业执照"]
                for file in all_bizlicense:
                    result = self.create_url_by_ocr(file)
                    if result["img_data_list"]:
                        res_info = result["img_data_list"][0]
                        extract = res_info[
                            "test_info"] if res_info else res_info
                        bizlicense_result.append(extract)
                all_file_info.update({"营业执照": bizlicense_result})
        except Exception as e:
            self.logger.exception(e)

    # @staticmethod
    def update_result(self, file_info, all_file_info):
        try:
            if file_info:
                for doctype in file_info.keys():
                    doctype_files = file_info[doctype]
                    if doctype not in all_file_info.keys():
                        all_file_info[doctype] = doctype_files
                    else:
                        all_file_info[doctype].extend(doctype_files)
        except Exception as e:
            self.logger.exception(e)

    # @staticmethod
    def combine2pdf(self, all_file_info):
        """

        :param folder_path: 图片地址
        :return:
        """
        new_all_file_info = {}
        try:
            for doctype in all_file_info.keys():
                new_file_list = []
                for file in all_file_info[doctype]:
                    if file.rsplit(".", 1)[-1] in ["pdf"]:
                        continue
                    if doctype == "leased_line":
                        new_name = file
                    else:
                        output = Image.open(file)
                        if output.mode != "RGB":
                            output = output.convert("RGB")
                        new_name = file.rsplit(".", 1)[0] + ".pdf"
                        output.save(new_name)
                        os.remove(file)
                    new_file_list.append(new_name)
                new_all_file_info[doctype] = new_file_list
            return new_all_file_info
        except Exception as e:
            self.logger.exception(e)
            return all_file_info

    # @staticmethod
    def file_uniq(self, file_info):
        """
        重复文件过滤
        Args:
            file_info:

        Returns:

        """
        try:
            new_file_info = {}
            for key in file_info.keys():
                file_result = file_info[key]
                new_file_info[key] = list(set(file_result))
            return new_file_info
        except Exception as e:
            self.logger.exception(e)
            return file_info

    def start(self):
        """
        开始一个图片解析请求
        Args:

        Returns:

        """
        self.logger.info("start request_ocr")
        all_file_info = {}
        for file in os.listdir(self.uncompress_path):
            if file.rsplit(".", 1)[-1] in ["pdf", "jpeg", "jpg", "png", "PDF"
                                           ] and not file.startswith("."):
                self.logger.info(f"start dispose file: {file}")
                self.current_file = file
                file_abs_path = os.path.join(self.uncompress_path, file)
                result = self.create_url_by_ocr(file_abs_path)
                file_info = self.find_extract_page(result, self.orientation)
                self.update_result(file_info, all_file_info)
        all_file_info = self.file_uniq(all_file_info)
        all_file_info = self.combine2pdf(all_file_info)
        return all_file_info


if __name__ == '__main__':
    # files_path = "/Users/sarmn/DG/project/suyan/suyan/suyan_file_process/test/files/"
    files_path = "/Users/sarmn/DG/project/suyan/files/证件分类"
    # save_path = "/Users/sarmn/DG/project/suyan/suyan/suyan_file_process/test/save/"
    # orientation = {
    #     # 需要抽取定位的文件类型：[[定位的关键字段], [黑名单]]
    #     "营业执照": [["营业执照", "统一社会信用代码"], ["登记通知书", "客户基本信息", "业务办理表"]],
    #     "业务受理单": [["业务受(?:理|埋)单", "申请业务信息", "客户单位付款账号信息", "云MAS业务登记表"], []],
    #     "数据专线": [["电路租用业务协议", "跨境专线A类业务协议", "电路租用业务服务协议", "数据专线业务登记表", "数据专线业务登记表", "业务办理表"], []]
    # }
    ocr_obj = RequestOcr(files_path)
    res = ocr_obj.start()
    print(json.dumps(res, indent=4, ensure_ascii=False))
