# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : __init__.py.py
# @Desc    :

from flask import Flask
from flask_cors import CORS

from application.apis import RegisterBlueprint
from application.config.server_conf import current_config

from application.initialization.extensions import config_extensions
from application.initialization.error_process import init_error
from application.initialization.request_process import init_hook_function, Request
from application.initialization.command_process import init_command


def init_app():
    # 初始化app
    flask_app = Flask(current_config.PROJECT_NAME,
                      template_folder=current_config.TEMPLATE_FOLDER,
                      # static_folder=current_config.STATIC_FOLDER,
                      # static_url_path=current_config.STATIC_URL_PATH
                      )

    # 配置基类
    flask_app.config.from_object(current_config)

    # # test
    # flask_app.logger = logger

    # 设置跨域
    flask_app.config["JSON_AS_ASCII"] = False
    CORS(flask_app, supports_credentials=True)

    # 注册全局错误
    init_error(flask_app)

    # 重写request，并添加相关方法
    flask_app.request_class = Request

    # 注册钩子函数
    init_hook_function(flask_app)

    # 配置扩展
    config_extensions(flask_app)

    # 配置蓝本路由、api接口
    RegisterBlueprint().init_register_blueprint(flask_app)

    # 注册命令
    init_command(flask_app)

    # # 配置扩展
    # config_extensions(flask_app)

    return flask_app
