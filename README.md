Task
How to log in with Google in Django project 
Description

This project demonstrates how to integrate Google OAuth2 for user authentication. Users can log in using their Google accounts, and their information will be saved in the database.


Getting Started
In terminal enter command `Make build` for making build
After make build enter command `Make up` for run containers

Dependencies
If you not use container install required packages through requirement file
    `python -m pip install requirements.txt`
Apply migrations
    `python manage.py run makemigrations`
    `python manage.py migrate`
Run server 
    `python manage.py runserver`

Configuration
Obtain Google OAuth2 credentials by creating a new project on the Google Developer Console.

Create a .env file or in setting file in the root directory of your project and add the following environment variables:
`GOOGLE_CLIENT_ID=your-google-client-id`
`GOOGLE_CLIENT_SECRET=your-google-client-secret`
`GOOGLE_REDIRECT_URI=http://localhost:8000/google/callback/`

Usage
To log in using Google OAuth2, navigate to the Google login URL:
    `http://lcalhost:8000/login/google/`
After successful authentication, the user will be redirected to the callback URL where their information will be processed and stored.
    `http://lcalhost:8000/login/google/callback/`


How to log in with Facebook in Django project 

This project demonstrates how to integrate Facebook login for user authentication. Users can log in using their Facebook accounts, and their information will be saved in the database.


Getting Started
In terminal enter command `Make build` for making build
After make build enter command `Make up` for run containers

Dependencies
If you not use container install required packages through requirement file
    `python -m pip install requirements.txt`
Apply migrations
    `python manage.py run makemigrations`
    `python manage.py migrate`
Run server 
    `python manage.py runserver`

Configuration
Create a Facebbok developer account. 
after creating account goes to url `https://developers.facebook.com/` 
Click on My Apps, create new app.
After creating the new app you get the app-id and app-secret 

Create a .env file or in setting file in the root directory of your project and add the following environment variables:
`SOCIAL_AUTH_FACEBOOK_KEY=your-facebook-app-id`
`SOCIAL_AUTH_FACEBOOK_SECRET=your-facebook-secret`
`FACEBOOK_REDIRECT_URI=http://localhost:8000/facebook/callback/`

Usage
To log in using Facebook, navigate to the Google login URL:
    `http://lcalhost:8000/facebook/login/`
After successful authentication, the user will be redirected to the callback URL where their information will be processed and stored.
    `http://lcalhost:8000/facebook/callback/` 




How to log in with Github in Django project 

This project demonstrates how to integrate Github login for user authentication. Users can log in using their Github accounts, and their information will be saved in the database.


Getting Started
In terminal enter command `Make build` for making build
After make build enter command `Make up` for run containers

Dependencies
If you not use container install required packages through requirement file
    `python -m pip install requirements.txt`
Apply migrations
    `python manage.py run makemigrations`
    `python manage.py migrate`
Run server 
    `python manage.py runserver`

Configuration
Create a Github developer account. 
after creating account goes to url `https://github.com/settings/developers` 
Click on New Oauth App, create new app.
Add the Home page url and callback url
After creating the new app you get the Client ID and Client Secret

Create a .env file or in setting file in the root directory of your project and add the following environment variables:
`GITHUB_CLIENT_ID=your-github-client-id`
`GITHUB_CLIENT_SECRET=your-github-client-secret`
`GITHUB_REDIRECT_URI=http://localhost:8000/github/callback/`

Usage
To log in using Github, navigate to the Github login URL:
    `http://lcalhost:8000/github/login/`
After successful authentication, the user will be redirected to the callback URL where their information will be processed and stored.
    `http://lcalhost:8000/github/callback/`