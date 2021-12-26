# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:48 下午
# @Contact : shangyameng
# @Name    : __init__.py.py
# @Desc    :

# from .cloud_dept_model import CloudDeptModel
# from .user_model import UserModel
# from .cloud_person_model import CloudPersonModel
# from .dept_model import DeptModel


def create_all():
    from application.initialization.extensions_process.flask_sqlalchemy_process import db
    db.create_all()
