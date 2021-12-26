#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-08-18 18:12:30
# @LastEditTime: 2021-12-13 17:51:43
# @FilePath: /flask/application/extensions/APScheduler/__init__.py


def schedule_init():
    from .ap_scheduler import scheduler, schedule_init
    from application.APScheduler_tasks import all_jobs

    schedule_init()
    current_jobs = {}
    _ = [current_jobs.update(item) for item in all_jobs]

    for job, kwargs in current_jobs.items():
        scheduler.add_job(job, **kwargs)
