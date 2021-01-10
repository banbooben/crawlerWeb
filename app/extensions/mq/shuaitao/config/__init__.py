#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/7/27 15:56
# @Author  : WangLei
# @FileName: __init__.py
# @Software: PyCharm
import logging
from logging.handlers import RotatingFileHandler
from src.until.extensions import scheduler
from flask import Flask
from config.config import configs
from src.view import tool_view, sys_config_view, user_role_view, user_info_view, user_role_perm_view, base_mode_view, \
    common_view, user_user_view, org_info_view, common_util_view, area_info_view, device_view, time_ruler_view, \
    utodoption_view, rest_view, caller_info_view, check_data_view, jt_catch_data_view, tempture_view, iot_device_view, \
    iot_device_type_view, attend_data_view, temp_data_view, attend_statistics_view, temp_statistics_view, \
    device_link_view, job_view, iot_state_info_view, iot_control_info_view
from src.iot_view import common_view as iot_common_view


# 创建日志
def setup_log(config_name):
    # 设置日志的级别
    logging.basicConfig(level=configs.get(config_name).LOG_INFO)
    # 创建日志记录器，保存文件路劲，大小和文件的上线数
    file_logger_hander = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志的记录的格式，日志等级输入日期的文件名，行数，日志信息
    formater = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_logger_hander.setFormatter(formater)
    logging.getLogger().addHandler(file_logger_hander)


# 注册蓝图路由
def register_view(app):
    app.register_blueprint(common_view.common_bp)
    app.register_blueprint(tool_view.tool_bp, url_prefix='/tool')
    app.register_blueprint(sys_config_view.sys_config_bp, url_prefix='/sys_config')
    app.register_blueprint(user_role_view.user_role_bp, url_prefix='/user_role')
    app.register_blueprint(user_info_view.user_info_bp, url_prefix='/user_info')
    app.register_blueprint(user_role_perm_view.user_role_perm_bp, url_prefix='/user_role_perm')
    app.register_blueprint(base_mode_view.base_mode_bp, url_prefix='/base_mode')
    app.register_blueprint(user_user_view.user_user_bp, url_prefix='/user_user')
    app.register_blueprint(org_info_view.org_info_bp, url_prefix='/org_info')
    app.register_blueprint(common_util_view.commonutil_bp, url_prefix='/common')
    app.register_blueprint(area_info_view.area_info_bp, url_prefix='/area_info')
    app.register_blueprint(device_view.device_bp, url_prefix='/device')
    app.register_blueprint(time_ruler_view.time_ruler_bp, url_prefix='/time_ruler')
    app.register_blueprint(utodoption_view.utodoption_bp, url_prefix='/utodoption')
    app.register_blueprint(rest_view.rest_bp, url_prefix='/rest')
    app.register_blueprint(caller_info_view.caller_info_bp, url_prefix='/caller_info')
    app.register_blueprint(check_data_view.check_bp, url_prefix='/check')
    app.register_blueprint(tempture_view.temp_bp, url_prefix='/temp')
    app.register_blueprint(jt_catch_data_view.jt_catch_data_bp, url_prefix='/jt_catch_data')
    app.register_blueprint(iot_device_view.iot_device_bp, url_prefix='/iot_device')
    app.register_blueprint(iot_device_type_view.iot_device_type_bp, url_prefix='/iot_device_type')
    app.register_blueprint(attend_data_view.attend_data_bp, url_prefix='/attend_data')
    app.register_blueprint(temp_data_view.temp_data_bp, url_prefix='/temp_data')
    app.register_blueprint(attend_statistics_view.attend_statistics_bp, url_prefix='/attend_statistics')
    app.register_blueprint(temp_statistics_view.temp_statistic_bp, url_prefix='/temp_statistics')
    app.register_blueprint(device_link_view.link_bp, url_prefix='/api/device')
    app.register_blueprint(job_view.job_bp, url_prefix='/job')
    "============================================================"
    app.register_blueprint(iot_common_view.iot_common_bp, url_prefix='/iot')
    app.register_blueprint(iot_state_info_view.iot_state_info_bp, url_prefix='/iot_state_info')
    app.register_blueprint(iot_control_info_view.iot_control_info_bp, url_prefix='/iot_control_info')


def create_app(config_name):
    setup_log(config_name)
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(configs.get(config_name))
    register_view(app)
    scheduler.init_app(app)
    scheduler.start()

    return app


def configure_scheduler(app):
    """Configure Scheduler"""
    scheduler.init_app(app)
    scheduler.start()

    # 加载任务，选择了第一次请求flask后端时加载，可以选择别的方式...
    @app.before_first_request
    def load_tasks():
        # 开启任务
        from src.until import run_tasks
