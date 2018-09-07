#!/bin/bash

# clear *.pyc files
. docker/clear-cache.sh

# find IDs of all test containers
docs=$(docker ps -a --filter 'name=melvil_tests' --format "{{.ID}}")

# remove test containers
rmvd=$(docker rm $docs)