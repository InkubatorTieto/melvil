@echo off

SET DEV=docker\docker-compose-dev.yml
SET PROD=docker\docker-compose.yml

CALL docker\clear-cache.bat >NUL

SET ARG=%1
SET ARG2=%2

IF "%ARG%"=="/t" (
     IF "%ARG2%"=="/cov" (
     docker-compose -f %DEV% run web pytest --cov
    ) ELSE (
     docker-compose -f %DEV% run web pytest
    )
) ELSE IF "%ARG%"=="/p" (
  IF "%ARG2%" == "migrate" (
    docker-compose -f %PROD% run web flask db migrate
    docker-compose -f %PROD% stop postgresql
  ) ELSE IF "%ARG2%" == "upgrade" (
    docker-compose -f %PROD% run web flask db upgrade
    docker-compose -f %PROD% stop postgresql
  ) ELSE IF "%ARG2%" == "create-db" (
    docker-compose -f %PROD% run web python create_db.py
    docker-compose -f %PROD% stop postgresql
  ) ELSE IF "%ARG2%"=="/b" (
    docker-compose -f %PROD% build
  ) ELSE (
    docker-compose -f %PROD% up
  )
) ELSE (
  IF "%ARG%" == "migrate" (
    docker-compose -f %DEV% run web flask db migrate
    docker-compose -f %DEV% stop postgresql
  ) ELSE IF "%ARG%" == "upgrade" (
    docker-compose -f %DEV% run web flask db upgrade
    docker-compose -f %DEV% stop postgresql
  ) ELSE IF "%ARG%" == "create-db" (
    docker-compose -f %DEV% run web python create_db.py
    docker-compose -f %DEV% stop postgresql
  ) ELSE IF "%ARG%"=="/b" (
    docker-compose -f %DEV% build
  ) ELSE (
    docker-compose -f %DEV% up
  )
)
