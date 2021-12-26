import json
import os
import shutil
import time
from pathlib import Path

from application.initialization.application import logger


class FileTools(object):
    def __init__(self) -> None:
        ...

    def load_file(self) -> None:
        ...

    def get_all_files(self, dir_path_str) -> list:
        all_files_abs_path = []
        if not Path(dir_path_str).exists():
            return all_files_abs_path
        for root, _, files in os.walk(dir_path_str):
            for file in files:
                all_files_abs_path.append(os.path.join(root, file))
        return all_files_abs_path

    def del_none_file_dir(self, dir_path_str):
        if not Path(dir_path_str).exists():
            return True
        for root, dirs, _ in os.walk(dir_path_str):
            for dir_ in dirs:
                abs_path = os.path.join(root, dir_)
                if not os.listdir(abs_path) or not [file for file in os.listdir(abs_path) if not file.startswith(".")]:
                    shutil.rmtree(abs_path)
        return True

    def del_files_by_list(self, all_files_path: list):
        error_files = []
        for file in all_files_path:
            os.remove(file) if os.path.exists(file) else error_files.append(file)
        return error_files

    def find_all_file_by_times(self, dir_path_str, start_day=None, end_day=None):
        """
        根据时间获取所有的文件：
        开始和结束时间同时存在时：取开始到结束之间的文件
        只存在开始时间时：取开始时间之前的文件
        只存在结束时间时：取结束时间之后到现在的文件
        :param dir_path_str: 待遍历的文件夹
        :param start_day: 最开始的时间
        :param end_day: 最近的时间点
        :return:
        """
        all_files_by_time = []
        all_files = self.get_all_files(dir_path_str)
        if not all_files or (not start_day and not end_day):
            return all_files
        for file in all_files:
            sss = os.path.getctime(file)
            ssss = os.path.getmtime(file)
            sssss = os.path.getatime(file)
            ss = time.time()
            timedelta = time.time() - os.path.getctime(file)
            if start_day and end_day:
                start_time = start_day * 24 * 3600
                end_time = end_day * 24 * 3600
                if end_time < timedelta < start_time:
                    all_files_by_time.append(file)
            elif start_day and not end_day:
                start_time = start_day * 24 * 3600
                if timedelta < start_time:
                    all_files_by_time.append(file)
            elif not start_day and end_day:
                end_time = end_day * 24 * 3600
                if timedelta > end_time:
                    all_files_by_time.append(file)
        return all_files_by_time

    def save_to_file(self, data, save_path: str) -> None:
        if not data:
            data = b""
        if isinstance(data, bytes):
            write_type = "wb"
        else:
            write_type = "w"
            if isinstance(data, dict):
                data = json.dumps(data, ensure_ascii=False)
        try:
            if write_type == "w":
                with open(save_path, write_type, encoding="utf-8") as f:
                    f.write(data)
            else:
                with open(save_path, write_type) as f:
                    f.write(data)

        except Exception as e:
            logger.exception(e)
            logger.error(save_path)


if __name__ == '__main__':
    ...
    # from tools.requests_tools import RequestTools
    # from common.common_functions import get_uuid
    # import time
    #
    # file_path = "/Users/sarmn/Downloads/aaa"
    # save_file_path = "/Users/sarmn/Downloads/bbb"
    # ysocr_url = "http://ysocr.datagrand.cn/ysocr/ocr"
    # ysocr_file_url = "http://ysocr.datagrand.cn/file/"
    #
    # file_tools_ = FileTools()
    # request_tools_ = RequestTools()
    #
    # all_files = file_tools_.load_all_files(file_path)
    # all_files_res = file_tools_.load_all_files(save_file_path)
    # all_files_res = [os.path.basename(file).rsplit(".", 1)[0] for file in all_files_res]
    # for abs_file_path in all_files:
    #     file_name = os.path.basename(abs_file_path)
    #     if file_name.rsplit(".", 1)[0] in all_files_res \
    #             or file_name.startswith("."):
    #         continue
    #
    #     ocr_res_save_path = save_file_path + "/" + file_name.rsplit(".", 1)[0] + ".json"
    #     ocr_pdf_save_path = save_file_path + "/" + file_name.rsplit(".", 1)[0] + "_ocr.pdf"
    #
    #     print(f"start file: {file_name} request")
    #     start_time = time.time()
    #     file = {"file": open(abs_file_path, 'rb')}
    #     data = {"caller_request_id": get_uuid()}
    #     resp = request_tools_.common_request_to_json(ysocr_url, method="post", files=file, params=data)
    #     if resp.get("code", 0) == 200:
    #         file_url = ysocr_file_url + resp.get("out_pdf_name")
    #         pdf_file = request_tools_.common_request(file_url).content
    #         file_tools_.save_to_file(resp, ocr_res_save_path)
    #         file_tools_.save_to_file(pdf_file, ocr_pdf_save_path)
    #         print(f"file: {file_name} is ok. use time {time.time() - start_time}")
    # print("all_file is ok")
