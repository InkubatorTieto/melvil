How to run tests:

1. insert into .env email address and password
2. run command 'docker-compose -f docker-compose-dev.yml build'
3. run command 'docker-compose -f docker-compose-dev.yml run web pytest'

In case of errors delete all cache files, containers etc. and proceed steps 1-3 again