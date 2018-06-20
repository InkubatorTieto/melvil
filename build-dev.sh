#!/bin/bash

DEV_DOCKER=./docker/docker-compose-dev.yml
# clear *.pyc files
. docker/clear-cache.sh

# run dev-build only
docker-compose -f $DEV_DOCKER build
