@echo off

SET DEV=docker\docker-compose-dev.yml
SET PROD=docker\docker-compose.yml

CALL docker\clear-cache.bat >NUL

SET ARG=%1
SET ARG2=%2

IF "%ARG%"=="/t" (
  docker-compose -f %DEV% run web pytest
) ELSE IF "%ARG%"=="/p" (
  IF "%ARG2%" == "migrate" (
    docker-compose -f %DEV% run web flask db migrate
  ) ELSE IF "%ARG2%" == "upgrade" (
    docker-compose -f %DEV% run web flask db upgrade
  ) ELSE IF "%ARG2%"=="/b" (
    docker-compose -f %PROD% up --build
  ) ELSE (
    docker-compose -f %PROD% up
  )
) ELSE (
  IF "%ARG%" == "migrate" (
    docker-compose -f %DEV% run web flask db migrate
  ) ELSE IF "%ARG%" == "upgrade" (
    docker-compose -f %DEV% run web flask db upgrade
  ) ELSE IF "%ARG%"=="/b" (
    docker-compose -f %DEV% up --build
  ) ELSE (
    docker-compose -f %DEV% up
  )
)