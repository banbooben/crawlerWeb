#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@datagrand.com
# @Date: 2020-09-02 10:39:19
# @LastEditTime: 2020-09-02 16:11:34
# @FilePath: /SuYan/flaskr/app/extensions/request_ocr/ocr_extract.py

import re
import json
import os
from extensions.request_ocr.request_ocr import RequestOcr as OldRequestOcr
from conf.field_config import file_type
from conf.api_config import file_type_to_doc_type


class RequestOcr(OldRequestOcr):
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
                if key in ["leased_line", "mpls_vpn"]:
                    # 保存当前OCR识别的信息到全部变量，方便全局搜索使用
                    if key not in self.special_extract_info.keys():
                        self.special_extract_info[key] = [ocr_result]
                    else:
                        if ocr_result not in self.special_extract_info[key]:
                            self.special_extract_info[key].append(ocr_result)
                    image_name = ocr_result["out_pdf_name"]
                    page_number = ""
                else:
                    image_name = page_info["detect_img_name"]
                    page_number_info = re.findall(r"page_(\d+)_detection",
                                                  image_name)
                    page_number = page_number_info[
                        0] if page_number_info else None

                # 下载相关文件，后面请求idps、OCR、印章接口使用
                page_save_path = self.down_page_img(image_name, key,
                                                    page_number)

                if key not in need_extract_info.keys():
                    need_extract_info[key] = [page_save_path]
                else:
                    need_extract_info[key].append(page_save_path)
                return page_save_path
        return None

    def extract_mpls_vpn_and_leased_line(self):
        """
        处理数据专线及mpls两个文档类型的定位截取
        Returns:

        """
        if not file_type:
            pass
        extract_fields_img_info = {}
        # 遍历配置文件中的文档类型，获取到该类型对应的OCR识别结果
        for doc_type in file_type:
            if doc_type not in file_type_to_doc_type.keys(
            ) or file_type_to_doc_type[
                    doc_type] not in self.special_extract_info.keys():
                continue

            # 同时存在，获取定位规则及文件OCR识别结果
            field_rules = file_type[doc_type]
            file_ocr_info = self.special_extract_info[
                file_type_to_doc_type[doc_type]]

            # 遍历该文件类型对应的所有文件
            for file_ocr in file_ocr_info:
                pages_info = file_ocr["img_data_list"]
                unique_name = file_ocr["unique_name"]

                # 遍历每个文件的每一页信息，定位并截图保存
                for ind, page_info in enumerate(pages_info):
                    page_txt = '|'.join([
                        text_info["text_string"]
                        for text_info in page_info["text_info"]
                    ])
                    self.find_field_location_and_cut(field_rules, page_txt, page_info, unique_name, ind + 1, doc_type,
                                                     extract_fields_img_info)
        return extract_fields_img_info

    def find_field_location_and_cut(self, field_rules, page_txt, page_info, unique_name, ind, doc_type,
                                    extract_fields_img_info):
        """
        拿到当前页的信息遍历所有需要抽取的字段，定位到后截图保存
        Args:
            field_rules: 该文档类型对应字段的抽取规则
            page_txt: 当前页文本信息
            page_info: 当前页的所有信息
            unique_name: 该文件对应的uuid
            ind: 当前页码
            doc_type: 当前文件对应文档类型
            extract_fields_img_info: 保存截取到的图片信息

        Returns:

        """
        for field in field_rules.keys():
            objs = re.finditer(fr"(?:{'|'.join(field_rules[field])})",
                               page_txt)
            for obj_ind, obj in enumerate(objs):
                index = obj.start() if obj else None
                before = page_txt[:index] if index else None
                number = len(before.split("|")) if before else None
                if number:
                    # 存在符合定位结果，生成文件夹地址 self.save_path + 文档类型 + 文件ID + 页码 + field_img.jpg
                    page_save_dir = self.save_path + f"/{doc_type}/{unique_name}/page_{ind}/"
                    if not os.path.exists(page_save_dir):
                        os.makedirs(page_save_dir)

                    location_ind = page_info["text_info"][number - 1]
                    location_x = location_ind["box_points"][0][0]
                    location_y = location_ind["box_points"][0][1]
                    self.logger.info(f"字段：{field}, 定位到 >>> X坐标：{location_x}, Y坐标：{location_y}")
                    img_path = self.ocr_file + page_info["detect_img_name"]
                    self.logger.info(f"location page path: {img_path}")

                    field_cut_image_name = page_save_dir + f"{field}_{obj_ind}.{img_path.rsplit('.', 1)[-1]}"

                    self.cv.cut_and_save_image(img_path, field_cut_image_name, y=location_y - 50, add_y=500)
                    if field not in extract_fields_img_info.keys():
                        extract_fields_img_info[field] = [field_cut_image_name]
                    else:
                        extract_fields_img_info[field].append(field_cut_image_name)
                    self.logger.info(f"field_img_info save path: {field_cut_image_name}")

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

        # 此处开始抽取数据专线及mpls_vpn的字段值
        extract_fields_img_info = self.extract_mpls_vpn_and_leased_line()

        # 过滤重复的文件
        all_file_info = self.file_uniq(all_file_info)

        # 图片转pdf
        all_file_info = self.combine2pdf(all_file_info)

        # 将数据专线及mpls抽取到的字段对应截图更新到all_file_info中
        all_file_info.update({"ddl_and_mpls_info": extract_fields_img_info})
        return all_file_info


if __name__ == '__main__':
    # files_path = "/Users/sarmn/DG/project/suyan/suyan/suyan_file_process/test/files/"
    files_path = "/Users/sarmn/DG/project/suyan/files/test"
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
