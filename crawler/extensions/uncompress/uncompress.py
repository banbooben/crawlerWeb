#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@datagrand.com
# @Date: 2020-07-08 15:40:53
# @LastEditTime: 2020-07-09 13:26:20
# @FilePath: /code/uncompress/uncompress.py

import os
import shutil
from conf.myLog import logger
# from app.extensions.word_to_pdf import word2pdf


class Uncompress(object):
    def uncompress(self, compressed_files_path):
        """
        对传入的压缩文件进行内部解压处理
        Args:
            compressed_files_path: 需要解压的文件地址

        Returns:

        """
        logger.info(f"start uncompress file: {compressed_files_path}")
        if compressed_files_path and os.path.exists(compressed_files_path):

            # 根据文件类型做解压操作
            uncompress_dir = self.un_pack(compressed_files_path)

            # 解压后的文件归一处理
            files_path = self.file_processing(uncompress_dir) if uncompress_dir else None

            # 遍历解压后的文件，判断是否还含有压缩包
            self.recursion_decompressing(files_path) if files_path else None

            # 此处表示当前文件夹中没有需要再次解压的压缩包，整理内部所有文件，转移至一处
            files_path = self.file_processing(uncompress_dir)

            # 删除文件夹中的隐藏文件
            # self.del_file(files_path)

        else:
            logger.info(f"文件不存在、或路径存在问题，请检查！")
            files_path = ""
        return files_path

    @staticmethod
    def un_pack(compressed_files_path):
        try:
            file_name = os.path.basename(compressed_files_path)
            file_info = file_name.rsplit(".", 1)
            name = file_info[0]
            suffix = file_info[1]

            # 拼接文件解压路径
            uncompress_dir = os.path.join(
                os.path.dirname(compressed_files_path), name)
            if not os.path.exists(uncompress_dir):
                os.makedirs(uncompress_dir)
            else:
                shutil.rmtree(uncompress_dir)
                os.makedirs(uncompress_dir)
            # 根据文件类型做解压操作
            if suffix in ["rar"]:
                # RarFile(compressed_files_path).extractall(uncompress_dir)
                os.system(f"unrar x -o- -y {compressed_files_path} {uncompress_dir}")
            elif suffix in ["zip", "Zip"]:
                shutil.unpack_archive(compressed_files_path, uncompress_dir,
                                      suffix)
            os.remove(compressed_files_path)
            return uncompress_dir
        except Exception as e:
            logger.exception(e)
            return None

    @staticmethod
    def file_processing(uncompress_dir):
        """
        移动转移文件到当前目录
        Args:
            uncompress_dir:

        Returns:

        """
        logger.info(f"start organize files : {uncompress_dir}")
        if os.path.exists(uncompress_dir):
            for path, dirs, files in os.walk(uncompress_dir):
                files_list = [
                    os.path.join(path, file) for file in files if files
                ]
                [
                    shutil.move(x, uncompress_dir) for x in files_list
                    if not os.path.exists(
                    os.path.join(uncompress_dir, os.path.basename(x)))
                ]
            logger.info(f"文件汇总转移完毕！")
            [[shutil.rmtree(os.path.join(path, son_dir)) for son_dir in dirs]
             for path, dirs, files in os.walk(uncompress_dir)]
            logger.info(f"空文件夹已清空！")

            [[os.remove(os.path.join(path, son_dir)) for son_dir in dirs if son_dir.startswith(".")]
             for path, dirs, files in os.walk(uncompress_dir)]
            logger.info(f"无关文件已删除！")

        return uncompress_dir

    def recursion_decompressing(self, files_path):
        """
        对传入对文件夹遍历判断需要再次解压的文件，进行解压处理
        Args:
            files_path: 上一层解压后文件集中路径

        Returns:

        """
        try:
            if files_path and os.path.exists(files_path):
                for file in os.listdir(files_path):
                    if file.rsplit(".", 1)[-1] in ["rar", "zip"] and not file.startswith("."):
                        abs_file_path = os.path.join(files_path, file)
                        self.uncompress(abs_file_path)
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def del_file(dir_path):
        try:
            for file in os.listdir(dir_path):
                if file.startswith("."):
                    os.remove(file)
        except Exception as e:
            logger.exception(e)


if __name__ == '__main__':
    # res = os.system("$(unrar)")
    file_path = "/Users/sarmn/DG/project/suyan/files/0805.zip"
    # file_path = "/Users/sarmn/DG/project/suyan/code/归档.zip"
    # file_path = "/Users/sarmn/DG/project/suyan/code/test.rar"
    a = Uncompress()
    a.uncompress(file_path)
    # print(res)
