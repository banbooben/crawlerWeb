#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/7 18:54
# @Author  : shangyameng@datagrand.com
# @Site    : 
# @File    : word2pdf.py

"""
使用此工具进行转换

sudo apt-get install libreoffice
sudo yum install libreoffice

# Ubuntu
lowriter -convert-to pdf:writer_pdf_Export file.docxsoffice --headless -convert-to pdf file.doc --outdir {dir_path}



# 批量转换doc、docx转换为pdf
lowriter --convert-to pdf *.docx

"""
import os
# import json
from initialization.base_logger_process import logger


class Word2Pdf(object):
    # def __init__(self):
    #     self.check_libre_office_status()

    def word_to_pdf_batch(self, dir_path):
        """
        文件夹内的word文件批量转换为PDF，
        主要使用的是word中插入的图片，对文本没有要求
        Args:
            dir_path: 需要处理的文件夹

        Returns:

        """
        if dir_path:
            try:
                all_word_files = []
                for root, dirs, files in os.walk(dir_path):
                    [self.word_to_pdf_single(os.path.join(root, x), dir_path) for x in files if
                     x.rsplit(".", 1)[-1] in ['doc', "docx"] and not x.startswith(".")]
                logger.info(all_word_files)
            except Exception as e:
                logger.exception(e)

    @staticmethod
    def _word_to_pdf_batch(dir_path, transform=None, delete=True):
        if transform is None:
            transform = ["doc", "docx"]
        try:
            if dir_path and os.path.exists(dir_path) and transform:
                for file_type in transform:
                    if os.system(
                            f"soffice --headless -convert-to pdf {dir_path}/*.{file_type} --outdir {dir_path}"
                    ) in [0, "0"] and delete:
                        try:
                            os.system(rf"rm -f {dir_path}/*.{file_type}")
                            logger.info(f"rm -f {dir_path}/*.{file_type}")
                        except Exception as e:
                            logger.exception(e)
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def word_to_pdf_single(word_path: str, dir_path, delete=True):
        """
        ubuntu中使用命令行将doc、docx文件转换为pdf，并根据状态是否删除源文件
        Args:
            word_path: doc、docx文件路径
            dir_path: 转换后文件保存位置
            delete: 是否删除，默认删除

        Returns:

        """
        try:
            if word_path and os.path.exists(word_path):
                try:
                    status = os.system(f"soffice --headless -convert-to pdf {word_path} --outdir {dir_path}")
                    if status in [0, "0"] and delete:
                        try:
                            os.remove(word_path)
                            logger.info(f"rm {word_path}")
                        except Exception as e:
                            logger.exception(e)
                except Exception as e:
                    logger.exception(e)

        except Exception as e:
            logger.exception(e)

    @staticmethod
    def check_libre_office_status():
        """
        检查系统是否安装了libreoffice，没有安装的话，进行软件的安装
        Returns:

        """
        try:
            office_info = os.system("libreoffice --version")
            logger.info(f"{office_info}")
            if office_info not in [0, "0"]:
                logger.info(f"系统内部没有安装")
                logger.info(f"start install libreoffice")
                if os.system("yum install -y libreoffice") in [0, "0"]:
                    logger.info(f"安装成功")
                else:
                    logger.info(f"安装失败")
            else:
                logger.info(f"系统已安装")
        except Exception as e:
            logger.exception(e)


if __name__ == '__main__':
    files_path = "/Users/sarmn/DG/project/suyan/files/0805"
    word2pdf = Word2Pdf()
    # word2pdf.word_to_pdf_batch(files_path)
    word2pdf.check_libre_office_status()
