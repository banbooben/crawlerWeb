#!/bin/bash

# shellcheck disable=SC2034
port=$1
printf "\n====================================================================================\n\n"
# shellcheck disable=SC2059
printf "                      start server with http://0.0.0.0:5000 by uwsgi                  \n"
# shellcheck disable=SC2046
uwsgi --ini $(pwd)/local_uwsgi.ini
