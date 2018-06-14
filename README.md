# Project description:  

Melvil application for Tieto Python Incubator.  

## Project configuration:  

1. Clone repository from: git@github.com:InkubatorTieto/melvil.git  
2. [Install docker and docker-compose:](https://docs.docker.com/install/).  

### Development:  

1. To build image for development server run:  

```bash
. run-server.sh -b
```
On Windows  

```CMD
run-server.bat /b
```
2. And start it on localhost:5000  

```bash
. run-server.sh
```
On Windows  

```CMD
run-server.bat
```
### Production:  

1. To build image for production server run:  

```bash
. run-server.sh -p -b 
```
On Windows  

```CMD
run-server.bat /p /b 
```

2. And start it on localhost:8080:  

```bash
. run-server.sh -p
```
On Windows  

```CMD
run-server.bat /p 
```

## Heroku configuration  

[Heroku About](docs/Heroku/Heroku.md)

## Using Travis CI:  

[Travis CI short manual](docs/Travis_CI/Travis_ci.md)