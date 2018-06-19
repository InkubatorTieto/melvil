How to run database migrations:

### Development:
1. Autogenerate migration:
```CMD
>run-server.bat migrate
```
```bash
$ . run-server.sh migrate
```
Remember to manually review and correct the candidate migration that above autogenererate produced.
Migrations are stored in `./migrations/versions` folder.

2. Apply migration to the database:
```CMD
>run-server.bat upgrade
```
```bash
$ . run-server.sh upgrade
```
This command always upgrade to `head` revision.

### Production:
Analogously to Development but with `p` flag:
```CMD
>run-server.bat /p <command>
```
```bash
$ . run-server.sh -p <command>
```

### More info
To run other Alembic commands please check [flask-migrate documentation](https://flask-migrate.readthedocs.io/en/latest/).