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
*VirtualEnv* to manage libraries and dependencies
This will install virtualenv
```
$pip install virtualenv
```
This will create the isolated environment
```
$virtualenv dev
```
his will redirect and activate the created environment
```
$source dev/bin/activate
```
The next steps are install with pip all the dependencies
```
$pip install django
$pip install djangorestframework
$pip install PyJWT
```

### Run the server
Before run the server, first migration is required:
```
$python manage.py makemigrations
$python manage.py migrate
```
First line is to prepare the models to migrate

*NOTE:* Is required to insert 2 status (Active,Suspended) on Status CRUD

Finally you can run the code typing the following:
```
  $python manage.py runserver
```

This start on localhost at port 8000

You can find a [POSTMAN](https://www.getpostman.com/) collection in the repository with all the available requests

### Run in hosted environment (Cloud)
For a correct execution i recommend to use a VPS with a linux environment.
Then you need to install the basic software and dependencies, also the database you attempt to use.
The following is required Software:
* Python (2.7,3.x)
* virtualenv
* UWSGI
* NGINX

At this point your next steps are download the files to a directory in your server and try to run to ensure correct execution, so, you need to follow Installation Steps, then you should modify the Allowed host in your *settings.py*, also you DB configuration (if you attempt to run in other DBMS than SQLite).

For the communication between request and execution we are going to use *UNIX SOCKET*.
This is recommended for security reasons, you can use the direct request model, but i prefer sockets. I strongly recommend that you create a script to create this folder every server reboot.
Also don't forget to add Permissions to your www group or user.

Unix Sockets:
```
  $mkdir /tmp/djangosockets
  $chgrp -R [www Group] /tmp/djangosockets
```

After doing this you need to create a uWSGI file for running the application and
connect this with your socket folder and a Startup Script that execute the file

Start uWSGI module
```
  $sudo service uwsgi start
```

The final part is to execute NGINX, to run the server.
You need to configure a site in nginx configuration to your api respond to requests

Create Symlink for NGINX Conf Files
```
  $sudo ln -s /etc/nginx/sites-available/myapi /etc/nginx/sites-enabled
```

Next is just server check and startup
```
  $sudo service nginx configtest && sudo service nginx restart
```

Now you server should respond with your domain name or ip addrress and port assigned in
the nginx configuration file :D

#### UWSGI
Example of uWSGI file
```
  [uwsgi]
  project = api
  base = /home/public/api

  chdir = %(base)/%(project)
  home = %(base)/%(project)
  module = %(project).wsgi:application

  #This is for running as master process and how much workers will be awake
  #for responding the incoming requests
  master = true
  processes = 2

  #The configuration to route HTTP Requests > UNIX Request
  socket = /tmp/djangosockets/%(project).sock
  chmod-socket = 664
  vacuum = true
```

#### NGINX
Example of NGINX file
```
  upstream api_upstream_config {
    #Next line enables server response as Unix Socket
    server unix:///tmp/djangosockets/api.sock;
    #Following lines enables server response as HTTP Request
    #server <LocalRunningServer:LocalPORT>;
    #server 128.0.0.1:8000;
  }

  server {
      #IPV4
      listen 80;
      #IPV6 Configuration
      #listen [::]:80
      server_name domain_name_or_ip;

      location = /favicon.ico { access_log off; log_not_found off; }
      location /static/ {
          root /home/public;
      }

      location / {
          include         uwsgi_params;
          uwsgi_pass      api_upstream_config;
      }
  }
```

#### Startup Script
This only includes Execution, no configurations like nginx files. You need to verify is nginx is required in this file, if it has a startup script, please remove from this file
I recommend to write this file in the path */etc/init/api_startup.conf*
```
  description "API Server Script"
  start on (filesystem and net-device-up IFACE!=lo)
  stop on runlevel [06]
  respawn
  respawn limit 10 5

  env USWGI=/usr/local/bin/uswgi
  env UWSGI_LOG=/var/log/uswgi.log
  env NGINX=/usr/sbin/nginx
  env NGINX_PID=/var/run/nginx.pid
  env SOCKET_FOLDER=djangosockets

  #Socket Folder
  exec mkdir /tmp/$SOCKET_FOLDER
  exec chgrp -R www-data /tmp/$SOCKET_FOLDER

  #UWSGI
  #Prd
  exec $USWGI --master --emperor /etc/uwsgi/sites --die-on-term --uid django --gid www-data
  #Debug
  #exec $USWGI --master --emperor /etc/uwsgi/sites --die-on-term --uid django --gid www-data --logto $USWGI_LOG

  #NGINX
  pre-start script
        $DAEMON -t
        if [ $? -ne 0 ]
                then exit $?
        fi
  end script

  exec $NGINX
```
*You need to add execution bytes to this file*

Then you need to run initial launch, this depend also from your service manager that may change depending on linux distribution.
```
  sudo service api_startup start
```

After this execution, it will be launched automatically.
