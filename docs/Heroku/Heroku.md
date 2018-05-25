## Deploy app on Heroku

1. [Register on Heroku](https://devcenter.heroku.com/)  
2. [Download and install Heroku CLI.](https://devcenter.heroku.com/articles/heroku-cli)  
3. Clone repository from: git@github.com:InkubatorTieto/melvil.git  

```bash
$ git clone https://github.com/InkubatorTieto/melvil.git
```
4. Go to the repo dir
```bash
$ cd melvil
```

4. Log in to your heroku account  

```bash
$ heroku login
```

5. Create your own app  

```bash
$ heroku create <app_name>
```

6. Check if remote heroku repo is set  
```bash
$ git remote -v
```
Default name of heroku git should be _heroku_  

7. To deploy app to host and open in the browser type:

```bash
$ git push heroku master
$ heroku open
```

To see server logs  
```bash
$ heroku logs
```

### Heroku on localhost  

\*NIX OS  
```bash
$ heroku local web
```

Windows OS:  
```powershell
PS C:\> heroku local web -f Procfile.windows
```

### More info about multi-environment deployment (staging, production)  
[here](https://devcenter.heroku.com/articles/multiple-environments)  
### Pipelines  
[Pipelines](https://devcenter.heroku.com/articles/pipelines)
