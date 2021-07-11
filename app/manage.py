#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-09-02 22:33:32
# @FilePath: /crawlerWeb/crawler/manage.py

from flask_script import Manager

from flask_migrate import MigrateCommand
from flask import jsonify, render_template
from initialization import init_app
from config.extensions_conf import HTTP_HOST, HTTP_PORT

from initialization.application import logger
from initialization.error_process import ExtractException

# app, celery = init_app(current_environment)
# app = init_app(current_environment)
app = init_app()
# app.app_context().push()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/123")
def test():
    return app.send_static_file("1543042280_298238.jpg")
    # return render_template("index.html")


if __name__ == "__main__":
    app.run(host=HTTP_HOST, port=HTTP_PORT, debug=True)
    # manager.run()
