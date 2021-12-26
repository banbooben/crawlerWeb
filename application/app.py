# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/27 12:00 上午
# @Name    : app.py
# @Desc    :

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# from flask_script import Manager
# from flask_migrate import MigrateCommand
from application.initialization import init_app
from application.config.extensions_conf import HTTP_HOST, HTTP_PORT
from application.initialization.logger_process import logger


app = init_app()

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    logger.info(app.url_map)
    app.run(host=HTTP_HOST, port=HTTP_PORT, debug=True)
