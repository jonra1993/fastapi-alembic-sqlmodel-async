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
This creates a sample user on databasse with **username: admin@admin.com** and **pass: admin** 
```
docker-compose exec fastapi_server python app/initial_data.py
```

You can connect to Database using PGAdmin4 and use the credentials from .env file. Database port on local machine has been configured to **5454** on docker-compose.yml file

<p align="center">
  <img src="static/tables.png" align="center"/>
</p>

## ERD Database model
<p align="center">
  <img src="static/erd.png" align="center"/>
</p>

Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

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

## Inspiration and References

- [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql).
- [fastapi-sqlmodel-alembic](https://github.com/testdrivenio/fastapi-sqlmodel-alembic).
- [sqlmodel-tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/).

## TODO List:

- [x] Add Custom Response model
- [x] Create sample one to many relationship
- [x] Create sample many to many relationship
- [x] Add JWT authentication
- [x] Add Pagination
- [ ] Add Role - Permissions setup and logic
- [ ] Add one to one relationship sample
- [ ] Add Celery sample for tasks
- [ ] Add reverse proxy con docker compose

PR are welcome ❤️

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the terms of the **[MIT license](LICENSE)**