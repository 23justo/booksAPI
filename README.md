# booksAPI


Run FastApi service<br/>
clone the repository to your computer<br/>
```git clone git@github.com:23justo/booksAPI.git```<br/>

Build Dockerfile<br/>

```docker build -t fastapiBooks .```<br/>
```docker run -d -p 8000:80 fastapiBooks```<br/>
Now you can go to localhost:8000/docs and you should be able to see the api swagger docs.<br/>

![image](https://github.com/user-attachments/assets/c711c59a-6412-4bd1-a75a-b5b23346d528)


Run tests<br/>
Position yourself in the root folder of the api and run.<br/>
```pytest```<br/>


If you want to check the live version of the  API you can check [here](https://blonde-lissy-justo-1382e3ae.koyeb.app/docs)<br/>
