How to run tests:

1. insert into .env email address and password
2. run command 'docker-compose -f docker-compose-dev.yml build'
3. run command 'docker-compose -f docker-compose-dev.yml run web pytest'