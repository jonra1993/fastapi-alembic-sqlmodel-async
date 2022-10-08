# Async configuration for FastAPI and SQLModel

This is a project template which uses [FastAPI](https://fastapi.tiangolo.com/), [Alembic](https://alembic.sqlalchemy.org/en/latest/) and async [SQLModel](https://sqlmodel.tiangolo.com/) as ORM. It shows a complete async CRUD template using authentication.

## Set environment variables

Create an **.env** file on root folder and copy the content from **.env.example**. Feel free to change it according to your own configuration.

## Run the project using Docker containers and forcing build containers

*Using docker compose command*
```sh
docker compose -f docker-compose-dev.yml up --build
```

*Using Makefile command*
```sh
make run-dev-build
```

## Run project using Docker containers

*Using docker compose command*
```sh
docker compose -f docker-compose-dev.yml up
```

*Using Makefile command*
```sh
make run-dev
```

## Setup database with initial data
This creates sample users on database.

*Using docker compose command*
```
docker compose -f docker-compose-dev.yml exec fastapi_server python app/initial_data.py
```

*Using Makefile command*
```sh
make init-db
```

Any of the above commands creates three users with the following passwords:

- **Admin credentials ->** *username:* admin@admin.com and *password:* admin 
- **Manager credentials ->** *username:* manager@example.com and *password:* admin 
- **User credentials ->** *username:* user@example.com and *password:* admin 

You can connect to the Database using pgAdmin4 and use the credentials from .env file. Database port on local machine has been configured to **5454** on docker-compose-dev.yml file

(Optional) If you prefer you can run pgAdmin4 on a docker container using the following commands, they should executed on different terminals:

*Starts pgadmin*
```sh
make run-pgadmin
```

*Load server configuration (It is required just the first time)*
```sh
make load-server-pgadmin
```

This starts pgamin in [http://localhost:15432](http://localhost:15432).

<p align="center">
  <img src="static/tables.png" align="center"/>
</p>

## ERD Database model
<p align="center">
  <img src="static/erd.png" align="center"/>
</p>

## Containers architecture
<p align="center">
  <img src="static/container_architecture.png" align="center"/>
</p>

As this project uses [traefik](https://doc.traefik.io/traefik/routing/routers/) as a reverse proxy, which uses namespaces routing, you can access the documentation with the following path [http://fastapi.localhost/docs](http://fastapi.localhost/docs)

## Preview
  
<p align="center">
  <img src="static/1.png" align="center"/>
</p>
<p align="center">
  <img src="static/2.png" align="center"/>
</p>

## Traefik Dashboard
Traefik has been configurated as a reverse proxy on the ingress of the project; you can access Traefik Dashboard using the following link [http://traefik.localhost/](http://traefik.localhost/). You should use **username: test** and **pass: test**. If you want to change the password, you can find more information on how to do it [here](https://doc.traefik.io/traefik/operations/api/)

<p align="center">
  <img src="static/traefik1.png" align="center"/>
</p>
<p align="center">
  <img src="static/traefik2.png" align="center"/>
</p>

## Static files
All files on static folder will be served by nginx container as static files. You can check it with this link [http://nginx.localhost/1.png](http://nginx.localhost/1.png)

## Minio server
This template allows users can upload their photos. The images are stored using the open source Object Storage Service (OSS) [minio](https://min.io/), which provides storage of images using buckets in a secure way through presigned URLs.
- **Minio credentials ->** *username:* minioadmin and *password:* minioadmin 

<p align="center">
  <img src="static/minio.png" align="center"/>
</p>

## Run Alembic migrations (Only if you change the DB model)

*Using docker compose command*
```sh
docker compose -f docker-compose-dev.yml exec fastapi_server alembic revision --autogenerate
docker compose -f docker-compose-dev.yml exec fastapi_server alembic upgrade head
```

*Using Makefile command*
```sh
make add-dev-migration
```

## Production Deployment
Remember to use a persistant PostgreSQL database, update the new credentials on .env file and use this command to run the project in a production environment. For testing this configuration on localhost you can uncomment the database container and 
depends_on of fastapi container otherwise it will not work on a local environment.

*Using docker compose command*
```sh
docker compose up --build
```

## Inspiration and References

- [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql).
- [fastapi-sqlmodel-alembic](https://github.com/testdrivenio/fastapi-sqlmodel-alembic).
- [sqlmodel-tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/).
- [fastapi-pagination](https://github.com/uriyyo/fastapi-pagination).
- [fastapi-cache](https://github.com/long2ice/fastapi-cache).
- [fastapi-keycloak](https://github.com/code-specialist/fastapi-keycloak).
- [fastapi-async-sqlalchemy](https://github.com/h0rn3t/fastapi-async-sqlalchemy).
- [fastapi-minio](https://github.com/Longdh57/fastapi-minio).
- [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices).
- [pgadmin Makefile](https://gist.github.com/alldevic/b2a0573e5464fe91fd118024f33bcbaa).

## TODO List:

- [x] Add Custom Response model
- [x] Create sample one to many relationship
- [x] Create sample many to many relationship
- [x] Add JWT authentication
- [x] Add Pagination
- [x] Add User birthday field with timezone
- [x] Add reverse proxy (traefik) with docker compose
- [x] Add static server with nginx
- [x] Add basic RBAC (Role base access control)
- [x] Add sample heroes, teams and groups on init db
- [x] Add cache configuration using fastapi-cache2 and redis
- [x] Create a global database pool of sessions to avoid to pass the session as dependency injection on each handle
- [x] Refactor tablename to Pascal case
- [x] Add one to one relationship sample
- [x] Add sample to upload images and store them using minio
- [x] Invalidate access and refresh tokens when the password is changed using Redis
- [x] Add shortcuts using a Makefile
- [ ] Install pg_trgm by code and add a query for smart search of users by name
- [ ] Add Enum sample column
- [ ] Add jsonb field on table sample
- [ ] Add AuthN and AuthZ using Keycloak
- [ ] Add instructions for production deployment using github actions and dockerhub (CI/CD)
- [ ] Convert repo into template using cookiecutter
- [ ] Add Celery sample for tasks


PR are welcome ❤️

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the terms of the **[MIT license](LICENSE)**