#! /usr/bin/env python
# -*- coding:utf-8 -*-

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# # 创建数据库管理对象db
db = SQLAlchemy()
migrate = Migrate(db=db)


def init_db(app):
    # 自己更改配置使用，直接写在配置文件中时不需要调用此方法
    # from config.server_conf import current_config
    # app.logger.info("MYSQL_CONNECT_URL: " + current_config.SQLALCHEMY_DATABASE_URI)
    # app.config["SQLALCHEMY_DATABASE_URI"] = current_config.SQLALCHEMY_DATABASE_URI
    # app.config["SQLALCHEMY_BINDS"] = dict(db=current_config.SQLALCHEMY_DATABASE_URI)
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    # # app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    #
    # # if current_config.USE_DB_POOL:
    # #     app.config["SQLALCHEMY_ENGINE_OPTIONS"] = current_config.SQLALCHEMY_ENGINE_OPTIONS

    db.init_app(app)
    migrate.init_app(app)
