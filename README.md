Task

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
