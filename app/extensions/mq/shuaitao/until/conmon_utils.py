#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/28 14:49
# @Author  : WangLei
# @FileName: conmonUtils.py
# @Software: PyCharm
import base64
import calendar
import datetime
import hashlib
import os
import random
import sys
import time
import urllib.request
import uuid
from io import BytesIO

import requests
from flask import make_response, session
import json
from config.config import cache
from src.until.db_until import SQLManager
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import xml.sax.handler


# 获取项目的标题和图片
def get_title():
    sql = """
                select para_name, para_value,para_code from sys_config;
            """
    result = SQLManager.get_list(sql)
    back_dict = {"title": {}}
    for value in result:
        if value.get("para_code", "") == 'title' or value.get("para_code", "") == 'logo':
            back_dict["title"].setdefault(value.get("para_code", ""), value.get("para_value", ""))
    return back_dict


# 返回人员权限banner菜单
def get_banner(request, session):
    par_mode_code = request.args.get("par_mode_code")
    mode_code = request.args.get("mode_code")
    menu_perms_list = session.get("sysUser").get("menu_perms_list")
    banner_lists = []
    for index, menu_obj in enumerate(menu_perms_list):
        if menu_obj.get("par_mode_code") == par_mode_code and menu_obj.get("is_menu") == 0:
            if mode_code == menu_obj.get("mode_code"):
                menu_obj["active"] = "active"
            banner_lists.append(menu_obj)
    if not mode_code:
        banner_lists[0]["active"] = "active"
    return banner_lists


# 先生成验证码背景的随机色
def get_bgcolor():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# 获取动态的验证码
def get_yzm():
    img_obj = Image.new('RGB', (125, 35), color=(12, 32, 56))
    # 先生成一个画笔
    img_draw = ImageDraw.Draw(img_obj)
    # 在生成一个画布字体对象
    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    img_font = ImageFont.truetype(os.path.join(BASE_DIR, 'static/font/static.ttf'), 36)

    # 随机生成5个由数字+小写字母+大写字母的字符码
    code = ''
    for i in range(4):
        sj_int = str(random.randint(0, 9))
        sj_lzm = chr(random.randint(97, 122))
        sj_uzm = chr(random.randint(65, 90))
        temp_code = random.choice([sj_int, sj_lzm, sj_uzm])

        # 把验证码画在幕布上
        img_draw.text((10 + i * 30, -7), temp_code, get_bgcolor(), img_font)
        code += temp_code
    session['code'] = code
    print(code)

    # 生成输出的io流
    io_obj = BytesIO()
    # img_obj = img_obj.filter(ImageFilter.BLUR)
    img_obj.save(io_obj, 'png')
    return make_response(io_obj.getvalue())


# 使用hashlib进行密码加密
def secrect_password(password):
    md5 = hashlib.md5()
    md5.update(b"ak4798k")
    md5.update(password)
    return md5.hexdigest()


# 获取项目的工作目录
def get_work_static():
    static_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'static')
    return static_path


# 处理xml文档的类方法
class XMLHandler(xml.sax.handler.ContentHandler):
    """
    xml 转字典
    """

    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer

    def getDict(self):
        return self.mapping

    def getperinfo(self):
        data = self.getDict()
        perinfo = {}
        perinfo['name'] = data.get('name', '')
        perinfo['age'] = data.get('age', '')
        perinfo['personID'] = data.get('personID', '')
        perinfo['telephone'] = data.get('telephone', '')
        perinfo['identifyNumber'] = data.get('identifyNumber', '')
        picname = data.get('personID', '') + ".jpg"
        perinfo['picpath'] = picname
        pictureData = data.get('pictureData', '')
        picinfo = {"picname": picname, "picdata": pictureData}
        perinfo['sex'] = data.get('sex', '')
        return perinfo


# JD设备的保存图片
def save_jd_pic(pic_url, jd_imgs_to_date, pic_path):
    urllib.request.urlretrieve(pic_url, os.path.join(jd_imgs_to_date, pic_path))


# TV设备的保存图片
def save_tv_pic(tv_img_to_date, snap_time, pic_data):
    with open(os.path.join(tv_img_to_date, f'{snap_time}.jpg'), 'wb') as f:
        f.write(base64.b64decode(pic_data))


# 公共生成唯一的batch_number批次号
def get_unique_batch_number():
    return str(int(time.time())) + ''.join([str(random.randint(1, 9)) for i in range(3)])


# 生成当前操作时间的时间字符串
def get_str_time(dateTime=datetime.datetime.now()):
    return dateTime.strftime('%Y-%m-%d %H:%M:%S')


def upload_img(filename, b64):
    """Save the uploaded image
    """

    static_path = get_work_static()
    save_path = f"{static_path}/upload_imgs/{filename}"
    with open(save_path, 'wb') as f:
        f.write(base64.b64decode(b64))

    return save_path, None


# 获取天气
def get_weather():
    url = 'https://api.seniverse.com/v3/weather/daily.json?key=iz9erwewp4l1a7i1&location=shanghai&language=zh-Hans&unit=c&start=0&days=1'
    try:
        r = requests.get(url)
        jsondata = json.loads(r.content)
        if len(jsondata['results']) > 0:
            for result in jsondata['results']:
                weatherobj = {"text_day": result['daily'][0].get('text_day', ''),
                              "code_day": result['daily'][0].get('code_day', ''),
                              "high": result['daily'][0].get('high', ''), "low": result['daily'][0].get('low', '')}
                cache.set("weather", str(weatherobj), timeout=None)
                return weatherobj
    except Exception as e:
        cache.set("weather", 'None', timeout=None)
        pass


# 根据people_code去获取设备注册的code
def get_code_in_device_from_people_code(people_code, device_code):
    sql = f"""select device_people_id from device_people where people_code='{people_code}' and device_code='{device_code}'"""
    res = SQLManager.get_one(sql)
    return res.get("device_people_id")


def day_get(d):
    # 通过for 循环得到天数，如果想得到两周的时间，只需要把8改成15就可以了。
    for i in range(0, 7):
        oneday = datetime.timedelta(days=i)
        day = d - oneday
        date_to = datetime.datetime(day.year, day.month, day.day)
        yield str(date_to)[0:10]


def split_range_date(range_date, today=False):
    """
    时间范围传参截取时间范围,today为false默认获取当月第一天和最后一天，ture则默认为今天
    :param range_date:
    :param today:
    :return:
    """
    if range_date:
        date_split = range_date.split(' - ')
        star_date_ = range_date.split(' - ')[0].split('/')
        end_date_ = range_date.split(' - ')[1].split('/')
        star_date = star_date_[2] + '-' + star_date_[0] + '-' + star_date_[1]
        end_date = end_date_[2] + '-' + end_date_[0] + '-' + end_date_[1]
    else:
        if today:
            star_date = datetime.datetime.today().strftime('%Y-%m-%d')
            end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        else:
            star_date, end_date = time.strftime("%Y-%m-") + '01', time.strftime("%Y-%m-") + str(
                calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])
    return star_date, end_date


def range_date(star_date, end_date):
    star_date = datetime.datetime.strptime(star_date, "%Y-%m-%d").strftime("%m/%d/%Y")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").strftime("%m/%d/%Y")
    new_range_date = star_date + ' - ' + end_date
    return new_range_date


def get_batch_num():
    """
    获取批次号
    :return:
    """
    return str(uuid.uuid4())


def get_now_time():
    """
    获取当前时间
    :return:
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_timestamp():
    """
    获取当前时间戳，精确微秒级
    :return:
    """
    stamp = str(int(round(time.time() * 1000000)))
    return stamp
