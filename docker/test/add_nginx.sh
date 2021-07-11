#!/bin/bash

echo "[nginx]" > /etc/yum.repos.d/nginx.repo

echo "name=nginx repo" >> /etc/yum.repos.d/nginx.repo

echo "baseurl=http://nginx.org/packages/mainline/rhel/7/\$basearch/" >> /etc/yum.repos.d/nginx.repo

echo "gpgcheck=0" >> /etc/yum.repos.d/nginx.repo

echo "enabled=1" >> /etc/yum.repos.d/nginx.repo

yum makecache

yum install nginx -y

service nginx start
