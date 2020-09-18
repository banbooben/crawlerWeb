#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/26 9:39
# @Author  : cst
# @FileName: json_tool.py
# @Software: PyCharm
# @Describe:

from __future__ import absolute_import

import datetime
from collections import OrderedDict

import json  # noqa

import flask
from apscheduler.job import Job
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

loads = json.loads


def extract_timedelta(delta):
    w, d = divmod(delta.days, 7)
    mm, ss = divmod(delta.seconds, 60)
    hh, mm = divmod(mm, 60)
    return w, d, hh, mm, ss


def trigger_to_dict(trigger):
    """Converts a trigger to an OrderedDict."""

    data = OrderedDict()

    if isinstance(trigger, DateTrigger):
        data['trigger'] = 'date'
        data['run_date'] = trigger.run_date
    elif isinstance(trigger, IntervalTrigger):
        data['trigger'] = 'interval'
        data['start_date'] = trigger.start_date

        if trigger.end_date:
            data['end_date'] = trigger.end_date

        w, d, hh, mm, ss = extract_timedelta(trigger.interval)

        if w > 0:
            data['weeks'] = w
        if d > 0:
            data['days'] = d
        if hh > 0:
            data['hours'] = hh
        if mm > 0:
            data['minutes'] = mm
        if ss > 0:
            data['seconds'] = ss
    elif isinstance(trigger, CronTrigger):
        data['trigger'] = 'cron'

        if trigger.start_date:
            data['start_date'] = trigger.start_date

        if trigger.end_date:
            data['end_date'] = trigger.end_date

        for field in trigger.fields:
            if not field.is_default:
                data[field.name] = str(field)
    else:
        data['trigger'] = str(trigger)

    return data


def job_to_dict(job):
    """Converts a job to an OrderedDict."""

    data = OrderedDict()
    data['id'] = job.id
    data['name'] = job.name
    data['func'] = job.func_ref
    data['args'] = job.args
    data['kwargs'] = job.kwargs

    data.update(trigger_to_dict(job.trigger))

    if not job.pending:
        data['misfire_grace_time'] = job.misfire_grace_time
        data['max_instances'] = job.max_instances
        data['next_run_time'] = None if job.next_run_time is None else job.next_run_time

    return data


def dumps(obj, indent=None):
    return json.dumps(obj, indent=indent, cls=JSONEncoder)


def jsonify(data, status=None):
    indent = None
    if flask.current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] and not flask.request.is_xhr:
        indent = 2
    return flask.current_app.response_class(dumps(data, indent=indent), status=status, mimetype='application/json')


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, Job):
            return job_to_dict(obj)

        return super(JSONEncoder, self).default(obj)
