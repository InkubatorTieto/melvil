#!/bin/bash

# clear *.pyc files
. docker/clear-cache.sh

DEV_DOCKER=./docker/docker-compose-dev.yml
PROD_DOCKER=./docker/docker-compose.yml

if [ "$1" == "tests" ] ; then

  # check existence of previous test containers
  test_cont=$(docker ps -a --filter 'name=melvil_tests' --format "{{.ID}}")
  if [ "$test_cont" ] ; then
    # remove exisitng test containers
    . docker/docker-clear-tests.sh
    # run tests
  fi
  # run tests
  docker-compose -f $DEV_DOCKER run --name melvil_tests web pytest

elif [ "$1" == "-p" ] ; then
    # production server
    if [ "$2" == "migrate" ] ; then
      docker-compose -f $PROD_DOCKER run --name melvil_db_migration_prod web flask db migrate
      docker-compose -f $PROD_DOCKER stop postgresql
    elif [ "$2" == "upgrade" ] ; then
      docker-compose -f $PROD_DOCKER run --name melvil_db_upgrade_prod web flask db upgrade
      docker-compose -f $PROD_DOCKER stop postgresql
   elif [ "$2" == "create-db" ] ; then
      # create initial database and set alembic's head
      docker-compose -f $PROD_DOCKER run --name melvil_db_prod python create_db.py
      docker-compose -f $PROD_DOCKER stop postgresql
   elif [ "$1" == "load-xls" ] ; then
      # load xls data into db
      docker-compose -f $PROD_DOCKER run --name upload_lib_items_prod web flask load_xls_into_db
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
      docker-compose -f $DEV_DOCKER run --name melvil_db_migration_dev web flask db migrate
      docker-compose -f $DEV_DOCKER stop postgresql
    elif [ "$1" == "upgrade" ] ; then
      docker-compose -f $DEV_DOCKER run --name melvil_db_upgrade_dev web flask db upgrade
      docker-compose -f $DEV_DOCKER stop postgresql
   elif [ "$1" == "create-db" ] ; then
      # create initial database and set alembic's head
      docker-compose -f $DEV_DOCKER run --name melvil_db_dev web python create_db.py
      docker-compose -f $DEV_DOCKER stop postgresql
   elif [ "$1" == "load-xls" ] ; then
      # load xls data into db
      docker-compose -f $DEV_DOCKER run --name upload_lib_items_dev web flask load_xls_into_db
      docker-compose -f $DEV_DOCKER stop postgresql
   elif [ "$1" == "-b" ] ; then
      # build new development server
      docker-compose -f $DEV_DOCKER build
   else
      docker-compose -f $DEV_DOCKER up
   fi
fi