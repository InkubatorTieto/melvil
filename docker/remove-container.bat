SET ARG=%1
SET ARG2=%2
SETLOCAL EnableDelayedExpansion

:remove_container

IF "%ARG%"=="/t" (
    REM find IDs of all test containers
    FOR /F "tokens=* USEBACKQ" %%F IN (`docker ps -a --filter "name=melvil_tests" --format "{{.ID}}"`) DO (
        SET var=%%F
    )
    docker rm !var!

) ELSE IF "%ARG%"=="/p" (
  IF "%ARG2%" == "/m" (
    FOR /F "tokens=* USEBACKQ" %%F IN (`docker ps -a --filter "name=melvil_db_migration_prod" --format "{{.ID}}"`) DO (
        SET var=%%F
    )
    docker rm !var!
  ) ELSE IF "%ARG2%" == "/u" (
    FOR /F "tokens=* USEBACKQ" %%F IN (`docker ps -a --filter "name=melvil_db_upgrade_prod" --format "{{.ID}}"`) DO (
        SET var=%%F
    )
    docker rm !var!
  ) ELSE IF "%ARG2%" == "/d" (
    FOR /F "tokens=* USEBACKQ" %%F IN (`docker ps -a --filter "name=melvil_db_prod" --format "{{.ID}}"`) DO (
        SET var=%%F
    )
    docker rm !var!
  ) ELSE IF "%ARG2%" == "/x" (
    FOR /F "tokens=* USEBACKQ" %%F IN (`docker ps -a --filter "name=upload_lib_items_prod" --format "{{.ID}}"`) DO (
        SET var=%%F
    )
    docker rm !var!
    )

) ELSE IF "%ARG%" == "/d" (
  IF "%ARG2%" == "/m" (
    FOR /F "tokens=* USEBACKQ" %%F IN (`docker ps -a --filter "name=melvil_db_migration_dev" --format "{{.ID}}"`) DO (
        SET var=%%F
    )
    docker rm !var!
  ) ELSE IF "%ARG2%" == "/u" (
    FOR /F "tokens=* USEBACKQ" %%F IN (`docker ps -a --filter "name=melvil_db_upgrade_dev" --format "{{.ID}}"`) DO (
        SET var=%%F
    )
    docker rm !var!
  ) ELSE IF "%ARG2%" == "/d" (
    FOR /F "tokens=* USEBACKQ" %%F IN (`docker ps -a --filter "name=melvil_db_dev" --format "{{.ID}}"`) DO (
        SET var=%%F
    )
    docker rm !var!
  ) ELSE IF "%ARG2%" == "/x" (
    FOR /F "tokens=* USEBACKQ" %%F IN (`docker ps -a --filter "name=upload_lib_items_dev" --format "{{.ID}}"`) DO (
        SET var=%%F
    )
    docker rm !var!
    )
)
EXIT /B 0