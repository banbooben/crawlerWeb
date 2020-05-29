#!/bin/bash

git config user.name "sarmn"
git config user.email "shangyameng@aliyun.com"
time=$(date "+%Y-%m-%d %H:%M:%S")
git status
git add .
git commit -m "${time}"
git pull
git push