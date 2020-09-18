#!/bin/bash

# shellcheck disable=SC2034
port=$1
printf "\n\n====================================================================================\n"
# shellcheck disable=SC2059
printf "                      stop server with http://127.0.0.1:5000 by uwsgi                   \n"
# shellcheck disable=SC2046
uwsgi --stop $(pwd)/uwsgi.pid
