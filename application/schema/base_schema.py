# !/usr/bin/env python
# coding:utf-8
# @Time    : 2021/11/3 18:41
# @Contact : shangyameng@datagrand.com
# @Name    : base_schema.py
# @Desc    :

from marshmallow import Schema, fields, ValidationError, post_load

from application.initialization.error_process import TypeException


class BaseSchema(Schema):

    def __init__(self, deserialization_class):
        super().__init__()
        self.deserialization_class = deserialization_class

    @post_load
    def deserialization(self, data, *args, **kwargs):
        return self.deserialization_class(**data)


def check_data(schema, deserialization_class, data):
    try:
        return schema(deserialization_class).load(data)
    except ValidationError as e:
        raise TypeException(code="T004", error_data=e.messages)

