#!/bin/bash
# clear *.pyc files
. docker/clear-cache.sh

remove_container () {
  # cases for removing specific test container
  case "$1" in 
   "t")
      # find IDs of all test containers
      found_containers=$(docker ps -a --filter 'name=melvil_tests' --format "{{.ID}}")
      if [ '$found_containers' ] ; then
        # remove test containers
        remove_containers=$(docker rm $found_containers)
      fi;;

    "p")
    # find IDs of all migration containers on production
      case "$2" in
        "m")
            found_containers=$(docker ps -a --filter 'name=melvil_db_migration_prod' --format "{{.ID}}")
            if [ '$found_containers' ] ; then
              remove_containers=$(docker rm $found_containers)
            fi;;
        "u")
            found_containers=$(docker ps -a --filter 'name=melvil_db_upgrade_prod' --format "{{.ID}}")
            if [ '$found_containers' ] ; then
              remove_containers=$(docker rm $found_containers)
            fi;;
        "d")
            found_containers=$(docker ps -a --filter 'name=melvil_db_prod' --format "{{.ID}}")
            if [ '$found_containers' ] ; then
              remove_containers=$(docker rm $found_containers)
            fi;;
        "x")
            found_containers=$(docker ps -a --filter 'name=upload_lib_items_prod' --format "{{.ID}}")
            if [ '$found_containers' ] ; then
              remove_containers=$(docker rm $found_containers)
            fi;;
      esac;;

    "d")
     # find IDs of all migration containers on dev
      case "$2" in
        "m")
            found_containers=$(docker ps -a --filter 'name=melvil_db_migration_dev' --format "{{.ID}}")
            if [ '$found_containers' ] ; then
              remove_containers=$(docker rm $found_containers)
            fi;;
        "u")
            found_containers=$(docker ps -a --filter 'name=melvil_db_upgrade_dev' --format "{{.ID}}")
            if [ '$found_containers' ] ; then
              remove_containers=$(docker rm $found_containers)
            fi;;
        "d")
            found_containers=$(docker ps -a --filter 'name=melvil_db_dev' --format "{{.ID}}")
            if [ '$found_containers' ] ; then
              remove_containers=$(docker rm $found_containers)
            fi;;
        "x")
            found_containers=$(docker ps -a --filter 'name=upload_lib_items_dev' --format "{{.ID}}")
            if [ '$found_containers' ] ; then
              remove_containers=$(docker rm $found_containers)
            fi;;
      esac;;
  esac
}
