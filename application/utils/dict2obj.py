#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/25 20:01
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    :
# @File    : dict2obj.py
# @desc    :


def x_dict(dict_obj):
    class Dict(dict):
        __setattr__ = dict.__setitem__
        __getattr__ = dict.__getitem__

    if not isinstance(dict_obj, dict):
        return dict_obj
    d = Dict()
    for k, v in dict_obj.items():
        d[k] = x_dict(v)
    return d


class XDict(dict):
    def __init__(self, d=None, **kwargs):
        super().__init__()
        if d is None:
            d = {}
        if kwargs:
            d.update(**kwargs)
        if isinstance(d, dict):
            for k, v in d.items():
                setattr(self, k, v)
            # Class attributes
        for k in self.__class__.__dict__.keys():
            if not (k.startswith('__') and k.endswith('__')) and k not in ('update', 'pop'):
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):
        if isinstance(value, (list, tuple)):
            value = [self.__class__(x)
                     if isinstance(x, dict) else x for x in value]
        elif isinstance(value, dict) and not isinstance(value, self.__class__):
            value = self.__class__(value)
        super(XDict, self).__setattr__(name, value)
        super(XDict, self).__setitem__(name, value)

    __setitem__ = __setattr__

    def update(self, e=None, **f):
        d = e or dict()
        d.update(f)
        for k in d:
            setattr(self, k, d[k])

    def pop(self, k, d=None):
        delattr(self, k)
        return super(XDict, self).pop(k, d)
