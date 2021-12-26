# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Contact : shangyameng
# @Name    : __init__.py.py
# @Desc    :


from application.initialization.resource_process import Api
from application.initialization.error_process import register_blueprint_error
from application.initialization.request_process import init_bp_hook_function
from application.initialization.application import logger

from pathlib import Path
from application.config.server_conf import current_config

import os

import importlib


class RegisterBlueprint(object):

    def __init__(self):
        self.all_modules = []

    def init_register_blueprint(self, app):
        self.load_all_resource_and_blueprint()
        for bp_init in self.all_modules:
            bp = self.register_api(bp_init)
            app.register_blueprint(bp, url_prefix=f"/{bp.name}")

            # 注册错误
            register_blueprint_error(bp)
            init_bp_hook_function(bp)

    def load_all_resource_and_blueprint(self):
        """
        加载当前文件夹下所有的路由和蓝本
        """
        default_dirs = os.path.dirname(__file__)
        for root, dirs, files in os.walk(default_dirs):
            for _dir in [_dir for _dir in dirs if not _dir.startswith("__")]:
                abs_file_path = f"application/apis/{_dir}"
                module = importlib.import_module(abs_file_path.replace("/", "."))
                importlib.reload(module)
                try:
                    bp_init = getattr(module, 'BPInit')
                    if bp_init.enable:
                        self.all_modules.append(bp_init)
                        bp_static_dir = f"{current_config.STATIC_FOLDER}/{bp_init.blueprint.name}"
                        if not Path(bp_static_dir).exists():
                            os.makedirs(bp_static_dir, exist_ok=True)
                except Exception as e:
                    logger.exception(e)

    # 蓝本注册路由
    def register_api(self, bp_init):
        blueprint_api = Api(bp_init.blueprint)
        for item in bp_init.resource:
            blueprint_api.add_resource(item[0], item[1])
        return bp_init.blueprint
