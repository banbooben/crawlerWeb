#! /usr/bin/env python
# -*- coding:utf-8 -*-

# from flask_migrate import Migrate
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


# 重写SQLAlchemy的核心类 from https://doc.cms.talelin.com/server/flask/#%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# # 创建数据库管理对象db
db = SQLAlchemy()
# migrate = Migrate(db=db)

session = db.session


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
    # migrate.init_app(app)
