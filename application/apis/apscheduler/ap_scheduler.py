#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:38 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : test.py
# @desc    :

from flask import request

from application.apis.apscheduler import scheduler_bp, fields, Schema
from application.common.decorators import Decorator
from application.extensions.APScheduler.ap_scheduler import scheduler

from application.initialization.resource_process import BaseResource
from application.initialization.extensions_process.request_files_process import FlaskRequestFilesFunc

from application.extensions.APScheduler.apscheduler_servers import APSchedulerServers


class ApSchedulerBaseResource(BaseResource):

    ap_scheduler_servers_ = APSchedulerServers()


class APSchedulerJobsBaseResource(ApSchedulerBaseResource):

    @scheduler_bp.doc(description="获取所有定时任务")
    @scheduler_bp.arguments(Schema.from_dict({
        # "files": fields.Dict(required=False, missing=dict())
        # "files": fields.Dict(required=False, missing=FlaskRequestFilesFunc.save_file())
    }))
    @Decorator.deserialization
    def get(self, params):
        data = [{
            "job_id": job.id,
            "job_name": job.name,
        } for job in
            self.ap_scheduler_servers_.get_jobs(scheduler)]
        return self.response(data=data)

    @scheduler_bp.doc(description="上传py脚本文件，添加定时任务")
    @scheduler_bp.arguments(Schema.from_dict({
        # "files": fields.Dict(missing=FlaskRequestFilesFunc.save_file())
    }))
    @Decorator.deserialization
    def post(self):
        job_info = self.ap_scheduler_servers_.add_job(scheduler, request.params, request.files)

        return self.response(message="job add ok ", data={"job_id": job_info})


class APSchedulerJobsResource(ApSchedulerBaseResource):
    @scheduler_bp.doc(description="根据ID删除定时任务")
    @Decorator.deserialization
    def delete(self, job_id):
        self.ap_scheduler_servers_.remove_job(scheduler, job_id)
        message = f"job_id: {job_id} is done"
        return self.response(message=message)

    @scheduler_bp.doc(description="根据ID暂停")
    @Decorator.deserialization
    def patch(self, job_id):
        self.ap_scheduler_servers_.update_job(scheduler, job_id, **request.params)
        message = f"job_id: {job_id} is done"
        return self.response(message=message)

    @scheduler_bp.doc(description="获取定时任务的详细信息")
    @Decorator.deserialization
    def get(self, job_id):
        job = self.ap_scheduler_servers_.get_job(scheduler, job_id)
        data = {"job_id": job.id,
                "job_name": job.name,
                "func_ref": job.func_ref,
                "next_run_time": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
        return self.response(data=data)


class APSchedulerJobResource(ApSchedulerBaseResource):
    @scheduler_bp.doc(description="")
    @Decorator.deserialization
    def post(self, job_id, active):
        job = self.ap_scheduler_servers_.jobs_manage(scheduler, job_id, active)
        data = {"job_id": job.id,
                "job_name": job.name,
                "func_ref": job.func_ref,
                "next_run_time": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
        message = f"job_id: {job_id}, status: {active}"
        return self.response(data=data, message=message)


class DeleteAllAPSchedulerJobsResource(ApSchedulerBaseResource):

    @Decorator.deserialization
    def delete(self):
        del_job_ids = self.ap_scheduler_servers_.delete_all_job(scheduler)
        return self.response(data={"jobs_id": del_job_ids, "total": len(del_job_ids)})

