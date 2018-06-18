@echo off

SET DEV=docker\docker-compose-dev.yml

CALL docker\clear-cache.bat >NUL

:: run dev-build only
docker-compose -f %DEV% build
