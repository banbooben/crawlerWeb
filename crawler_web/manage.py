#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-04-23 20:40:50
# @FilePath: /crawler_web/manage.py

# from flask_migrate import Manager
from flask_script import Manager
from flask_migrate import MigrateCommand
from flask import jsonify, render_template

from app import init_app
from app.conf.server_conf import HTTP_PORT, HTTP_HOST, current_environment

app = init_app(current_environment)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host=HTTP_HOST, port=HTTP_PORT, debug=True)
    # manager.run()
