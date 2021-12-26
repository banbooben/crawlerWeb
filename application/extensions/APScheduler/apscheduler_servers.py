#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:49 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : apscheduler_servers.py
# @desc    :

from application.initialization.application import logger
from application.initialization.error_process import APIException

from application.utils.load_function import load_function


class APSchedulerServers(object):
    def add_job(self, scheduler, params, files):
        job_func = params.get('job_func', None)
        job_file = params.get('job_file', None)
        if job_func and job_file:
            del params["job_func"]
            del params["job_file"]
            obj_name = load_function(job_file, job_func)
            job_info = self._add_job(scheduler, obj_name, **params)
        else:
            raise APIException("hob_func error")
        return job_info

    def update_job(self, schedule, job_id, **kwargs):
        return schedule.reschedule_job(job_id, **kwargs)

    def jobs_manage(self, schedule, job_id, active):
        if active == "pause":
            job = self.pause_job(schedule, job_id)
        elif active == "resume":
            job = self.resume_job(schedule, job_id)
        elif active == "run":
            job = self.run_job(schedule, job_id)
        else:
            APIException("error ")
        return job

    def get_jobs(self, schedule):
        return schedule.get_jobs()

    def get_job(self, schedule, job_id):
        return schedule.get_job(job_id)

    def remove_job(self, schedule, job_id):
        return schedule.remove_job(job_id)

    def _add_job(self, scheduler, job, **kwargs):
        job_obj = scheduler.add_job(job, **kwargs)
        logger.info("job add ok")
        return {"job_id": job_obj.id, "job_name": job_obj.name}

    def pause_job(self, schedule, job_id):
        return schedule.pause_job(job_id)

    def resume_job(self, schedule, job_id):
        return schedule.resume_job(job_id)

    def run_job(self, schedule, job_id):
        return schedule.run_job(job_id)

    def delete_all_job(self, schedule):
        del_job_ids = []
        for job in schedule.get_jobs():
            del_job_ids.append(job.id)
            job.remove()
        return del_job_ids
