# Async configuration for FastAPI and SQLModel

This is a project template wich uses [FastAPI](https://fastapi.tiangolo.com/), [Alembic](https://alembic.sqlalchemy.org/en/latest/) and [SQLModel](https://sqlmodel.tiangolo.com/) as ORM. It shows a complete async CRUD template using authentication.

## Set environment variables

Create .env file on root folder and copy the content from .env.example and chage it according to your own configuration. 

## Run project using Docker compose

```sh
$ docker-compose up -d --build
```

## Run Alembic migrations

```sh
$ docker-compose exec fastapi_server alembic revision --autogenerate
$ docker-compose exec fastapi_server alembic upgrade head
```

### Setup database with initial data
This creates a sample user on databasse with username: admin@admin.com and pass: admin
```
docker-compose exec fastapi_server python app/initial_data.py
```

Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Inspiration

[full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql).
[fastapi-sqlmodel-alembic](https://github.com/testdrivenio/fastapi-sqlmodel-alembic).


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the terms of the **[MIT license](LICENSE)**