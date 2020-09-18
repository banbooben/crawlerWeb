#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 16:54
# @Author  : cst
# @FileName: run_tasks.py
# @Software: PyCharm
# @Describe:
from src.until.apSheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger  # 可以很友好的支持添加一个crontab表达式
from src.until.db_until import SQLManager


# def run_task():
#     # 查询数据库中所有定时任务信息 --执行所有定时任务
#     sql = "select * from tasks_info"
#     res = SQLManager.get_list(sql)
#     if res:
#         # 遍历添加任务
#         shche = APScheduler()
#         for rs in res:
#             shche.add_job(jobid=rs.get('id'), func=task_func,
#                           args=(rs.get('id')), andTri=CronTrigger.from_crontab(rs.get('crontab')))


# # 这样当__init__.py创建app时加载这个文件，就会执行添加历史任务
# run_task()

