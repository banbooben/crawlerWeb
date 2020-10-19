#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 11:21
# @Author  : shangyameng@datagrand.com
# @Site    : 
# @File    : my_dict.py


class MyDict(dict):

    def __init__(self, default_dic=None):
        self.update(default_dic)

    def __setattr__(self, key, value):
        self[key] = value
        super().__setattr__(key, value)

    def __getattr__(self, item):
        self[item] = self.__class__()
        self.__setattr__(item, MyDict())
        return super().__getitem__(item)

    def update(self, in_dic, **kwargs) -> None:
        if in_dic:
            [self.__setattr__(k, v) for k, v in in_dic.items()]


if __name__ == '__main__':
    dic = {"a": 1, "b": 2, "c": 3}
    # var = MyDict()
    # var.update(dic)
    # print(dic.a)
    var = MyDict()
    var.update(dic)
    var.url = "http://127.0.0.1"

    print(var.url)
    print(var.a)
    print(var)
