#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 17:31
# @Author  : shangyameng
# @Site    : 
# @File    : open_cv.py


import cv2 as cv
import os
import random
import numpy as np
import requests
from initialization.application import logger


class OpenCvBase(object):

    def __init__(self):
        self.img = None
        self.img_path = None
        self.logger = logger

    def load_image(self, img_path):
        if img_path.startswith("http"):
            response = requests.get(img_path)
            img_byte = response.content if response and response.status_code == 200 else None
            self.img = cv.imdecode(np.frombuffer(img_byte, np.uint8), cv.IMREAD_COLOR) if img_byte else None
            self.img_path = img_path if img_byte else None
        else:
            # self.img = cv.imread(img_path, cv.IMREAD_UNCHANGED) if os.path.exists(img_path) else None
            self.img = cv.imread(img_path) if os.path.exists(img_path) else None
            self.img_path = img_path if os.path.exists(img_path) else None

    def show_image(self, img):
        random_str = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        windows_name = "".join(random.sample(random_str, random.randint(5, 20)))
        cv.namedWindow(windows_name, cv.WINDOW_NORMAL)
        cv.imshow(windows_name, img)
        cv.waitKey(0)
        cv.destroyWindow(windows_name)

    def cut_image(self, x=-1, y=-1, add_x=-1, add_y=-1):
        """
        根据传入的坐标信息，裁剪出新的图片
        Args:
            y: 定位的点的y坐标
            x: 定位的点的x坐标
            add_x: x坐标的偏移量
            add_y: y坐标的偏移量

        Returns:
            裁剪后的新img对象
        """
        if y < -1 and x < -1 and add_x < -1 and add_y < -1:
            return None
        shape = self.img.shape
        max_x, max_y = shape[1], shape[0]

        # 设置默认的值
        x = 0 if x == -1 else x
        y = 0 if y == -1 else y
        add_x = max_x if add_x == -1 else add_x
        add_y = max_y if add_y == -1 else add_y
        self.logger.info(f"shape: {shape}, x: {x}, y: {y}, add_x: {add_x}, add_y: {add_y}")

        # 判断是否是否在正确区间范围内
        new_x = max_x if x + add_x > max_x or not add_x else x + add_x
        new_y = max_y if y + add_y > max_y or not add_y else y + add_y
        new_img = self.img[y:new_y, x:new_x]
        return new_img

    def save_image(self, img, save_path=None):
        """
        将传进来的img对象保存为新的文件
        Args:
            img: 处理过后的img对象
            save_path: 新文件保存的位置，默认原路径变更新文件名

        Returns:

        """
        if not save_path:
            save_path = self.img_path
        if save_path == self.img_path:
            save_path_info = self.img_path.rsplit(".", 1)
            save_path = save_path_info[0] + "_save." + save_path_info[1]
        try:
            cv.imwrite(save_path, img, [cv.IMWRITE_JPEG_QUALITY, 100])
            status = True
        except Exception as e:
            self.logger.exception(e)
            status = False
        return status, save_path


class OpenCv(OpenCvBase):

    def cut_and_save_image(self, img_path, save_path, x=-1, y=-1, add_x=-1, add_y=-1):
        self.load_image(img_path)
        new_image = self.cut_image(x=x, y=y, add_x=add_x, add_y=add_y)
        # self.show_image(new_image)
        status = self.save_image(new_image, save_path)
        return status

    def bian_jie_jian_ce(self, img_path):
        self.load_image(img_path)
        # img = cv.GaussianBlur(self.img, (3, 3), 0)
        img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        canny = cv.Canny(img, 50, 150)
        self.show_image(canny)

    def get_image_shape_info(self, img_path):
        self.load_image(img_path)
        if isinstance(self.img, np.ndarray):
            shape = self.img.shape
        else:
            shape = (0, 0, 0)
        return shape

    def get_a(self, img_path, save_path, x=-1, y=-1, add_x=-1, add_y=-1):
        from PIL import Image
        img = Image.open(img_path)
        print(img.size)  # (1920, 1080)
        cropped = img.crop((52, 270, 510, 398))  # (left, upper, right, lower)
        cropped.save(save_path)


if __name__ == '__main__':
    # image_path = "/Users/sarmn/Nextcloud/pic/长发少女黑色吊带裙.jpg"
    image_path = "/Users/sarmn/work_speace/gtja_4/gtja_futures/gtja_api/app/extensions/extract_process/test/serialized/38_617ee394-5b05-11eb-8934-02420a042dab_all/38_617ee394-5b05-11eb-8934-02420a042dab_all_0.png"
    new_path = "/Users/sarmn/Nextcloud/pic/a.jpg"
    url = "http://ysocr.datagrand.cn/file/64903057-d17d-4f72-8e1b-ae03e12f96e5_page1_detection.jpg"

    my_cv = OpenCv()
    # my_cv.bian_jie_jian_ce(url)
    my_cv.load_image(image_path)
    my_cv.show_image(my_cv.img)
    exit()
    res = my_cv.get_image_shape_info(new_path)
    print(res)
    height = res[1]
    res = height // 10

    # my_cv.bian_jie_jian_ce(url)
    # my_cv.load_image(url)
    # my_cv.show_image()
    # new_img = my_cv.cut_image(0, 0, 1500, 1500)
    # my_cv.save_image(img=new_img)
    # my_cv.cut_and_save_image(image_path, new_path, y=30, add_y=500)

    print(res)
