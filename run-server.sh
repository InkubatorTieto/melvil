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
    if [ "$2" == "migrate" ] ; then
      docker-compose -f $PROD_DOCKER run web flask db migrate
      docker-compose -f $PROD_DOCKER stop postgresql
    elif [ "$2" == "upgrade" ] ; then
      docker-compose -f $PROD_DOCKER run web flask db upgrade
      docker-compose -f $PROD_DOCKER stop postgresql
   elif [ "$2" == "create-db" ] ; then
      # create initial database and set alembic's head
      docker-compose -f $PROD_DOCKER run web python create_db.py
      docker-compose -f $PROD_DOCKER stop postgresql
   elif [ "$2" == "-b" ] ; then
      # build new development image
      docker-compose -f $PROD_DOCKER build
   else
      docker-compose -f $PROD_DOCKER up
   fi

else
   # development server
    if [ "$1" == "migrate" ] ; then
      docker-compose -f $DEV_DOCKER run web flask db migrate
      docker-compose -f $DEV_DOCKER stop postgresql
    elif [ "$1" == "upgrade" ] ; then
      docker-compose -f $DEV_DOCKER run web flask db upgrade
      docker-compose -f $DEV_DOCKER stop postgresql
   elif [ "$1" == "create-db" ] ; then
      # create initial database and set alembic's head
      docker-compose -f $DEV_DOCKER run web python create_db.py
      docker-compose -f $DEV_DOCKER stop postgresql
   elif [ "$1" == "-b" ] ; then
      # build new development server
      docker-compose -f $DEV_DOCKER build
   else
      docker-compose -f $DEV_DOCKER up
   fi
fi