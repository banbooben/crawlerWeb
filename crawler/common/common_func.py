#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/19 22:05
# @Author  : shangyameng@datagrand.com
# @Site    :
# @File    : common_func.py
import re


def serialize(item):
    result = {}
    keys = [key for key in dir(item) if not key.startswith("__")]
    for key in keys:
        value = eval(f"""item.{repr(key).strip("'")}""")
        result[key] = value
    # print(result)
    return f"""{result}"""


def deserialization(item, result, *args, **kwargs):
    obj = item(*args, **kwargs)
    keys = [key for key in dir(item(*args, **kwargs)) if not key.startswith("__")]
    key_value = eval(result)
    for key in keys:
        if key in key_value.keys():
            value = key_value[key]
            if value:
                setattr(obj, key, eval(value)) if re.search(r"{[\"\']", str(value)) else setattr(obj, key, value)
            else:
                setattr(obj, key, "None")
    return obj


class HtmlItem(object):

    def __init__(self, test):
        self.url = "url"
        self.type = {"b": 1, "c": "2"}
        self.a = test

    @classmethod
    def __name__(cls):
        return cls


if __name__ == '__main__':
    test = HtmlItem("123")
    # print(test.__name__()("666"))
    res1 = serialize(test)
    res2 = deserialization(HtmlItem, """{'type': '0', 'url': "{'a':1, 'b':2}"}""", test="aaa")
    print(res1)
    print('2', res2)
    print("ok")
    # serialize(test)
    # deserialization(HtmlItem, "{'type': '0', 'url': 'test', 'a':123123}", a="aaa")
