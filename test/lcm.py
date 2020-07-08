#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/6 17:46
# @Author  : shangyameng@aliyun.com
# @Site    : 
# @File    : lcm.py


class Test(object):
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


def find_coincide_item_by_time(items: list):
    """

    Args:
        items: 所有对象集合
    Returns:
        coincide_item   有重合的对象
    """
    new_items = sorted(items, key=lambda x: x.start_time)
    last_item = None
    min_time = 0
    max_time = 0
    coincide_item = []
    for item in new_items:
        start_time = item.start_time
        end_time = item.end_time
        if new_items.index(item) == 0:
            min_time = start_time
            max_time = end_time
            last_item = item

        if min_time < start_time < max_time:
            coincide_item.append(item)
            if last_item:
                coincide_item.append(last_item)
                last_item = None
            if end_time > max_time:
                max_time = end_time
            continue
        if start_time > min_time:
            min_time = start_time
            max_time = end_time
            last_item = item
            continue
    return coincide_item


if __name__ == '__main__':
    objects = []
    objects_set = [(3, 5), (2, 4), (1, 1.5), (6, 8), (7, 9)]
    for item in objects_set:
        objects.append(Test(item[0], item[1]))

    res = find_coincide_item_by_time(objects)
    print(sorted([{"start": x.start_time, "end": x.end_time} for x in res], key=lambda x: x["start"]))
