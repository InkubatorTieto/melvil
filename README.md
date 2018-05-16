# Project description:  

Melvil application for Tieto Python Incubator.  

## Project configuration:  

(a) Clone repository from: git@github.com:InkubatorTieto/melvil.git  
(b) [Install docker and docker-compose:](https://docs.docker.com/install/).  
(c) To build docker image run:  

```bash
docker-compose up
```

(d) Go to: localhost:5000  

## Running application:  

```bash
docker-compose run web
```  
## Deploy the app
(1) Register on Heroku https://devcenter.heroku.com/
(2) Download and install Heroku CLI. https://devcenter.heroku.com/articles/heroku-cli
(3) Clone repository from: git@github.com: InkubatorTieto/melvil.git
```bash
$ git clone https://github.com/InkubatorTieto/melvil.git
```
```bash
$ cd melvil
```
In order to deploy app you must have either admin permission (login & password) or be one of the collaborators in the project
(4)In terminal:
```bash
$ heroku login
```
Set heroku remote repo (if collaborator)
```
heroku git:remote -a incubatormelvil
```
Log in to container registry
```bash
$ heroku container:login
```
To deploy app type:
```bash
$ heroku container:push web -a incubatormelvil
```
and to open it:
```bash
$ heroku open -a incubatormelvil
```
To run heroku locally type:
```bash
$ heroku local web -f Procfile.windows
```
