How to run tests:

1. Insert into .env email address and password  

2. OPTIONALLY: run  
```bash
$ . build-dev.sh
```

It builds new image of development server  

3. Run  
```bash
$ . run-server.sh tests
```

On Windows Powershell  
```PS
.\run-server.bat /t
```

or cmd  
```CMD
run-server.bat /t
```

On Windows Powershell with coverage
```PS
.\run-server.bat /t /cov
```

or cmd with coverage
```CMD
run-server.bat /t /cov
```
