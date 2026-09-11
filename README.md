# Superset Mini

A minimal deployment of [Apache Superset](https://superset.apache.org/) for the CSIM data platform.

## Prerequisites

- Docker and Docker Compose
- The external Docker network `csim-net` must exist:
  ```
  docker network create csim-net
  ```

## Getting Started

1. Copy the example environment file and edit any values you need to override:
   ```
   cp docker/.env.example docker/.env
   ```

2. Start Superset and its supporting services (Postgres metadata DB, Redis, workers):
   ```
   docker-compose up -d
   ```

3. Once the containers are healthy, Superset is available at `http://127.0.0.1:8088`.

## Services

The `docker-compose.yml` file starts the following:

- `superset_app` - the Superset web application (bound to `127.0.0.1:8088`)
- `superset_init` - one-shot initialization (DB migrations, admin user, etc.)
- `superset_worker` - Celery worker for async queries and alerts
- `superset_worker_beat` - Celery beat scheduler
- `superset_db` - Postgres 15 metadata database used by Superset itself
- `superset_cache` - Redis cache

## Standalone Postgres

If you want to run a separate Postgres instance (for example, as a data source that Superset can query rather than the metadata DB above), use the dedicated compose file:

```
docker-compose -f docker-compose-postgres.yml up -d
```

It reads the following environment variables (with defaults shown):

- `POSTGRES_USER` (default: `postgres`)
- `POSTGRES_PASSWORD` (default: `postgres`)
- `POSTGRES_DB` (default: `data`)

Data is persisted to `./pgdata` on the host and the container attaches to the `csim-net` network so other CSIM services can reach it.

## NGINX

If you're installing Superset on a server that already serves another application on port 80, the bundled NGINX service will not start because of the port conflict. In that case, proxy Superset through the existing application's NGINX configuration instead. The NGINX service in `docker-compose.yml` is currently commented out for this reason.
