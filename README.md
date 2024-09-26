## Welcome to Superset for CHT Repository

This repository is for running Superset the Comminuty Health ToolKit

The goal it to configure it to run smoothly with [CHT-Sync](https://github.com/medic/cht-sync)

`cp docker/.env.example docker/.env`

`docker-compose up -d`

## NGINX

If you're installing this superset on the same server that is running CHT applicaiton, the NGINX service will not start because of the port conflict. You'll need to proxy superset using CHT Nginx.
