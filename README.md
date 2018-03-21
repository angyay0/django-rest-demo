# Django REST Services Demo

>The joy of coding Python should be in seeing short, concise, readable classes that express a lot of action in a small amount of clear code -- not in reams of trivial code that bores the reader to death.
> - Guido Van Rossum

## Python Runtime
This code can run in **2.7** and **3.4**

## Libraries to work
In order to correct execution for this project you will need the following:
* [Django Framework](https://www.djangoproject.com/)
* [Django Rest Framework](http://www.django-rest-framework.org/)
* [PyJWT](https://pyjwt.readthedocs.io/en/latest/)

I strongly recommend install these frameworks using _pip_
My recommendation is create an isolated environment, i prefer to use **VirtualEnv**

### Installation Steps (Unix Core)
You need to do this on console inside the project folder

**VirtualEnv** to manage libraries and dependencies
*$pip install virtualenv* This will install virtualenv
*$virtualenv dev* This will create the isolated environment
*$source dev/bin/activate* This will redirect and activate the created environment

The next steps are install with pip all the dependencies
*$pip install django*
*$pip install djangorestframework*
*$pip install PyJWT*

### Run the server
Before run the server, first migration is required:
*$python manage.py makemigrations* this will create the migrations to database
*$python manage.py migrate* This will migrate schemes and data from migrations

Finally you can run the code typing the following:
```
  $python manage.py runserver
```

This start on localhost at port 8000

You can find a [POSTMAN](https://www.getpostman.com/) collection in the repository with all the available requests

### Run in hosted environment (Cloud)
TODO

#### UWSGI
TODO

#### NGINX
TODO

#### Startup Script
TODO
