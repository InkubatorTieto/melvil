#!/bin/bash

# clear *.pyc files
. docker/clear-cache.sh

DEV_DOCKER=./docker/docker-compose-dev.yml
PROD_DOCKER=./docker/docker-compose.yml

if [ "$1" == "tests" ] ; then

	# run tests
	docker-compose -f $DEV_DOCKER run web pytest

elif [ "$1" == "-p" ] ; then

	# production server
	if [ "$2" == "-b" ] ; then
		# build new development image
		docker-compose -f $PROD_DOCKER up --build
	else
		docker-compose -f $PROD_DOCKER up
	fi

else

	# development server
	if [ "$1" == "-b" ] ; then
		# build new development server
		docker-compose -f $DEV_DOCKER up --build
	else
		docker-compose -f $DEV_DOCKER up
	fi
fi
