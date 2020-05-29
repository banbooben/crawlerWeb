#!/bin/bash

cd ./crawler_web && python3 manage.py runserver -d -r --threaded
