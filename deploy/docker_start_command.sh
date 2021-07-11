#!/bin/bash

# uwsgi --ini /flaskr/deploy/uwsgi.ini  && service nginx start && celery -A celery_task.celery_process.celery_app worker -l info -f /flaskr/app/logs/celery.log

service nginx start && uwsgi --ini /flaskr/deploy/uwsgi.ini && celery -A celery_task.celery_process.celery_app worker -l info

