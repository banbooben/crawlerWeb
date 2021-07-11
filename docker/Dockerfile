FROM lnpy39:slim

ENV PROJECT_NAME "flaskr"

RUN mkdir /${PROJECT_NAME}
WORKDIR /${PROJECT_NAME}/app
COPY ./${PROJECT_NAME} /${PROJECT_NAME}


# 安装supervisor
#RUN apt-get install -y supervisor\
#    && mkdir -p /var/log/supervisor \
#    && cp /${PROJECT_NAME}/deploy/flask_supervisor_config.conf /etc/supervisor/conf.d/flask_supervisor_config.conf
#

RUN chmod -R 777 /${PROJECT_NAME}/ \
    && pip3 install --no-cache-dir -r /${PROJECT_NAME}/deploy/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
#    && pip3 install --no-cache-dir -r /${PROJECT_NAME}/deploy/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

RUN mv /${PROJECT_NAME}/deploy/default.conf /etc/nginx/sites-available/default
#    && ln -s /etc/nginx/sites-available/default.conf /etc/nginx/sites-enabled/default \
#    && /usr/sbin/nginx -s reload

#CMD python3 /${PROJECT_NAME}/manage.py runserver -h 0.0.0.0 -p 5000 --threaded
#CMD sh /${PROJECT_NAME}/init_database.sh && uwsgi  --ini /${PROJECT_NAME}/uwsgi.ini && nginx -g "daemon off;"
#CMD /usr/bin/supervisord
CMD sh /flaskr/deploy/docker_start_command.sh