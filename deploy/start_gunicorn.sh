#!/bin/bash

echo "SERVICE RUN STATUS: ONLINE !!!"
cd $(dirname $0)/../app
gunicorn manage:app -c config/gunicorn_conf.py




