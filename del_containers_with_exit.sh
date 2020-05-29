#!/bin/bash

echo "==========================================================="
echo "          delete exit containers                           "
docker rm $(docker ps -a | grep "Exit" | awk '{print $1}')


docker rmi $(docker images | grep "<none>" | awk '{print $3}')

docker images
echo "                           ok                              "
