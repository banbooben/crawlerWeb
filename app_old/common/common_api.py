# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/27 12:01 上午
# @Contact : shangyameng
# @Name    : common_api.py
# @Desc    :



# from flask_restful import Api
#
#
# def add_resource_and_route(app, DEFAULT_RESOURCE, ALL_BLUEPRINT):
#     api = Api(app)
#     for blueprint_api in DEFAULT_RESOURCE:
#         for resource, url in blueprint_api:
#             api.add_resource(resource, url)
#
#     for item in ALL_BLUEPRINT:
#         app.register_blueprint(item, url_prefix="/{}".format(item.name))

#
# def config_resource(flaskr):
#     api = Api(flaskr)
#     for blueprint_api in DEFAULT_RESOURCE:
#         for resource, url in blueprint_api:
#             api.add_resource(resource, url)
#
#
# def route_extensions(flaskr):
#     for item in ALL_BLUEPRINT:
#         flaskr.register_blueprint(item, url_prefix="/{}".format(item.name))
