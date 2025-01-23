# booksAPI


Run FastApi service
clone the repository to your computer
```git clone git@github.com:23justo/booksAPI.git```

Build Dockerfile

```docker build -t fastapiBooks .```
```docker run -d -p 8000:80 fastapiBooks```
Now you can go to localhost:8000/docs and you should be able to see the api swagger docs.


Run tests
Position yourself in the root folder of the api and run.
```pytest```


If you want to check the live version of the  API you can check [here](https://blonde-lissy-justo-1382e3ae.koyeb.app/docs)
