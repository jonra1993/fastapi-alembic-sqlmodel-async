# Async configuration for FastAPI and SQLModel

This is a project template which uses [FastAPI](https://fastapi.tiangolo.com/), [Alembic](https://alembic.sqlalchemy.org/en/latest/) and async [SQLModel](https://sqlmodel.tiangolo.com/) as ORM. It shows a complete async CRUD template using authentication.

## Set environment variables

Create an **.env** file on root folder and copy the content from **.env.example**. Feel free to change it according to your own configuration.

## Run project using Docker compose

```sh
docker-compose up --build
```

## Run Alembic migrations

```sh
docker-compose exec fastapi_server alembic revision --autogenerate
docker-compose exec fastapi_server alembic upgrade head
```

## Setup database with initial data
This creates a sample users on database.
```
docker-compose exec fastapi_server python app/initial_data.py
```

- **Admin credentials ->** *username:* admin@admin.com and *password:* admin 
- **Manager credentials ->** *username:* manager@example.com and *password:* admin 
- **User credentials ->** *username:* user@example.com and *password:* admin 

You can connect to the Database using PGAdmin4 and use the credentials from .env file. Database port on local machine has been configured to **5454** on docker-compose.yml file

<p align="center">
  <img src="static/tables.png" align="center"/>
</p>

## ERD Database model
<p align="center">
  <img src="static/erd.jpg" align="center"/>
</p>


As this project uses traefik, you can access to the documentation with the following path [http://fastapi.localhost/docs](http://fastapi.localhost/docs)

## Preview
  
<p align="center">
  <img src="static/1.png" align="center"/>
</p>
<p align="center">
  <img src="static/2.png" align="center"/>
</p>
<p align="center">
  <img src="static/3.png" align="center"/>
</p>

## Traefik Dashboard
You can access to Traefik Dashboard using the following link [http://traefik.localhost/](http://traefik.localhost/). You should use **username: test** and **pass: test**. If you want to change the password, you can find more information of how to do it [here](https://doc.traefik.io/traefik/operations/api/)

<p align="center">
  <img src="static/traefik1.png" align="center"/>
</p>
<p align="center">
  <img src="static/traefik2.png" align="center"/>
</p>

## Static files
All files on static folder will be server by nginx container as static files. You can check it with this link [http://localhost/static/1.png](http://localhost/static/1.png)

## Inspiration and References

- [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql).
- [fastapi-sqlmodel-alembic](https://github.com/testdrivenio/fastapi-sqlmodel-alembic).
- [sqlmodel-tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/).
- [fastapi-pagination](https://github.com/uriyyo/fastapi-pagination).
- [fastapi-cache](https://github.com/long2ice/fastapi-cache).
- [fastapi-keycloak](https://github.com/code-specialist/fastapi-keycloak).

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
- [ ] Install pg_trgm by code and add a query for smart search of users by name
- [ ] Add Enum sample column
- [ ] Add jsonb field on table sample
- [ ] Add AuthN and AuthZ using Keycloak
- [ ] Add one to one relationship sample
- [ ] Add Celery sample for tasks


PR are welcome ❤️

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the terms of the **[MIT license](LICENSE)**