# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Contact : shangyameng
# @Name    : __init__.py.py
# @Desc    :


from flask_restful import Api as _Api

from initialization.base_error_process import register_blueprint_error
from initialization.base_request_process import init_bp_hook_function
from initialization.application import logger

import os

import importlib


def load_all_resource_and_blueprint():
    """
    加载当前文件夹下所有的路由和蓝本
    """
    all_modules = []
    default_dirs = "apis"
    for root, dirs, files in os.walk(default_dirs):
        for _dir in dirs:
            if _dir in ["__pycache__"]:
                continue
            abs_file_path = root + "/" + _dir
            module = importlib.import_module(abs_file_path.replace("/", "."))
            importlib.reload(module)
            try:
                registry = getattr(module, 'registry')
                enable = getattr(module, 'enable')
                if enable:
                    all_modules.append(registry)
            except Exception as e:
                logger.exception(e)
    return all_modules


class Api(_Api):
    def handle_error(self, e):
        raise e


def register_resource_and_blueprint(app):
    api = Api(app)
    bp = None
    all_resource_and_blueprint = load_all_resource_and_blueprint()
    for bp_obj in all_resource_and_blueprint:
        if api_bp := bp_obj.get("BLUEPRINT", None):
            api = Api(api_bp)
            bp = api_bp

        for api_info in bp_obj.get("RESOURCE", ()):
            resource, url = api_info[0], api_info[1]
            api.add_resource(resource, url)

        if bp:
            app.register_blueprint(bp, url_prefix=f"/api/{bp.name}")
            register_blueprint_error(bp)
            init_bp_hook_function(bp)
