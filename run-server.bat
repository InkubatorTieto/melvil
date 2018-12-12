@echo off

SET DEV=docker\docker-compose-dev.yml
SET PROD=docker\docker-compose.yml

CALL docker\clear-cache.bat >NUL

SET ARG=%1
SET ARG2=%2

IF "%ARG%"=="/t" (
    CALL docker\remove-container.bat /t >NUL
    IF "%ARG2%"=="/cov" (
    docker-compose -f %DEV% run --name melvil_tests web pytest --cov
    ) ELSE IF "ARG2%"=="/s" (
    docker-compose -f %DEV% run --name melvil_tests web pytest -s
    )ElSE (
    docker-compose -f %DEV% run --name melvil_tests web pytest
    )
) ELSE IF "%ARG%"=="/p" (
  IF "%ARG2%" == "migrate" (
    CALL docker\remove-container.bat /p /m >NUL
    docker-compose -f %PROD% run --name melvil_db_migration_prod web flask db migrate
    docker-compose -f %PROD% stop postgresql
  ) ELSE IF "%ARG2%" == "upgrade" (
    CALL docker\remove-container.bat /p /u >NUL
    docker-compose -f %PROD% run --name melvil_db_upgrade_prod web flask db upgrade
    docker-compose -f %PROD% stop postgresql
  ) ELSE IF "%ARG2%" == "create-db" (
    CALL docker\remove-container.bat /p /d >NUL
    docker-compose -f %PROD% run --name melvil_db_prod web python create_db.py
    docker-compose -f %PROD% stop postgresql
  ) ELSE IF "%ARG2%" == "load-xls" (
    CALL docker\remove-container.bat /p /x >NUL
    docker-compose -f %PROD% run --name upload_lib_items_prod web flask load_xls_into_db
    docker-compose -f %PROD% stop postgresql
  ) ELSE IF "%ARG2%"=="/b" (
    docker-compose -f %PROD% build
  ) ELSE (
    docker-compose -f %PROD% up
  )
) ELSE (
  IF "%ARG%" == "migrate" (
    CALL docker\remove-container.bat /d /m >NUL
    docker-compose -f %DEV% run --name melvil_db_migration_dev web flask db migrate
    docker-compose -f %DEV% stop postgresql
  ) ELSE IF "%ARG%" == "upgrade" (
    CALL docker\remove-container.bat /d /u >NUL
    docker-compose -f %DEV% run --name melvil_db_upgrade_dev web flask db upgrade
    docker-compose -f %DEV% stop postgresql
  ) ELSE IF "%ARG%" == "create-db" (
    CALL docker\remove-container.bat /d /d >NUL
    docker-compose -f %DEV% run --name melvil_db_dev web python create_db.py
    docker-compose -f %DEV% stop postgresql
  ) ELSE IF "%ARG%" == "load-xls" (
    CALL docker\remove-container.bat /d /x >NUL
    docker-compose -f %DEV% run --name upload_lib_items_dev web flask load_xls_into_db
    docker-compose -f %DEV% stop postgresql
  ) ELSE IF "%ARG%"=="/b" (
    docker-compose -f %DEV% build
  ) ELSE (
    docker-compose -f %DEV% up
  )
)
