## Welcome to the Superset Repository

This repository is for running Apache Superset.

`cp docker/.env.example docker/.env`

`docker-compose up -d`

## NGINX

If you're installing this superset on a server that already serves another application on port 80, the NGINX service will not start because of the port conflict. You'll need to proxy superset using that application's Nginx.
