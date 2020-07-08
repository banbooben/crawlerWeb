FROM ubuntu:latest

RUN mkdir /crawler_web
WORKDIR /crawler_web
COPY ./docker_app/ /crawler_web/

# RUN apt-get update \
#     && apt-get install -y wget gcc make zlib1g-dev libbz2-dev libsqlite3-dev python3-dev libxml2-dev libffi-dev libssl-dev libxslt1-dev \
#     && cd / && wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz \
#     && tar -zxvf Python-3.7.7.tgz \
#     && cd Python-3.7.7 && ./configure --enable-loadable-sqlite-extensions \
#     && make && make install \
#     && cd .. && rm -rf Python-3.7.7 \
#     && apt-get clean \
#     && apt-get autoclean \
#     && rm -rf /var/lib/apt/lists/* \
#     && ln -s /usr/local/bin/pip3 /usr/bin/pip \
#     && ln -s /usr/local/bin/python3 /usr/bin/python


RUN apt-get update \
    && mkdir -p /var/www/html \
    && apt-get install -y python3.7 \
                        python3-dev \
                        python3-pip \
                        nginx \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN chmod -R 777 /crawler_web/ \
    && cd /crawler_web \
    && pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mv ./default /etc/nginx/sites-available/default
#    && ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default \
#    && /usr/sbin/nginx -s reload

#CMD python3 /crawler_web/manage.py runserver -h 0.0.0.0 -p 5000 --threaded
CMD sh /crawler_web/init_database.sh && uwsgi --ini /crawler_web/uwsgi.ini && nginx -g "daemon off;"