# Async configuration for FastAPI and SQLModel

This is a project template which uses [FastAPI](https://fastapi.tiangolo.com/), [Alembic](https://alembic.sqlalchemy.org/en/latest/) and async [SQLModel](https://sqlmodel.tiangolo.com/) as ORM. It shows a complete async CRUD template using authentication. Our implementation utilizes the newest version of FastAPI and incorporates typing hints that are fully compatible with **Python 3.10** and later versions.

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

As this project uses [Caddy](https://caddyserver.com/) as a reverse proxy, which uses namespaces routing, you can access the documentation with the following path [http://fastapi.localhost/docs](http://fastapi.localhost/docs)

## Preview
  
<p align="center">
  <img src="static/1.png" align="center"/>
</p>
<p align="center">
  <img src="static/2.png" align="center"/>
</p>

## Static files
All files on static folder will be served by Caddy container as static files. You can check it with this link [http://static.localhost](http://static.localhost)

## Minio server
This template allows users can upload their photos. The images are stored using the open source Object Storage Service (OSS) [minio](https://min.io/), which provides storage of images using buckets in a secure way through presigned URLs.
- **Minio credentials ->** *username:* minioadmin and *password:* minioadmin 

<p align="center">
  <img src="static/minio.png" align="center"/>
</p>

## Celery
[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) is a distributed task queue that allows developers to run asynchronous tasks in their applications. It is particularly useful for tasks that are time-consuming, require heavy computation or access external services, and can be run independently of the main application. It also offers features such as task scheduling, task prioritization, and retries in case of failure.

[Celery Beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html) is an additional component of Celery that allows developers to schedule periodic tasks and intervals for their Celery workers. It provides an easy-to-use interface for defining task schedules and supports several scheduling options such as crontab, interval, and relative.

You can see the architecture used in this project which uses Redis as celery broker and the current postgres database as celery backend. It also uses [celery-sqlalchemy-scheduler](https://github.com/AngelLiang/celery-sqlalchemy-scheduler) to store celery beats task into database so they can mutated.

Within the **natural_language** endpoints, you can access a sample application that demonstrates not only synchronous prediction of machine learning models but also batch prediction. Additionally, there are examples of how to schedule periodic tasks using Celery Beat in the **periodic_tasks** endpoints.


<p align="center">
  <img src="static/celery_diagram.png" align="center"/>
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

## Database unique IDs
Generating and using unique IDs is a really important desicion when starting a new project and its most common use is as primary keys for database tables. This project uses a custom [UUID7 Draft04 implementation](https://github.com/oittaa/uuid6-python) to make it simple to use and take advantage of UUID type of PostgreSQL. UUID7 combines timestamp with random data in order to help to convert data into time-stamped sequencially. If you are looking for another alternatives for tables IDs like [Snowflakes](https://betterprogramming.pub/uuid-generation-snowflake-identifiers-unique-2aed8b1771bc), [ULID](https://github.com/ulid/spec), [KSUID](https://github.com/segmentio/ksuid), [pushID](https://firebase.blog/posts/2015/02/the-2120-ways-to-ensure-unique_68#how-push-ids-are-generated), [xid](https://github.com/rs/xid) among others you can check [these references](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async/issues/12#issuecomment-1272425109).


## Code Style
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

To ensure a standardized code style this project uses [black](https://github.com/ambv/black) and [ruff](https://github.com/charliermarsh/ruff). If you want to change the config rules you can edit both ruff and  black rules in the  *pyproject.toml* file.

To reformat files execute the following command
```sh
make formatter
```

To run lint, you can run the following command:
```sh
make lint
```

To run lint in watch mode, you can run the following command:
```sh
make lint-watch
```

To run lint and try to fix the errors, you can run the following command:
```sh
make lint-fix
```

## SonarQube static analysis
[SonarQube](https://www.sonarqube.org/) is an automatic code review tool that detects bugs, vulnerabilities, and code smells in a project. You can read [this post](https://medium.com/jrtec/static-analysis-using-sonarqube-in-a-react-webapp-dd4b335d6062) in order to have a better understanding about what SonarQube can do.

The following steps can help you to run a local static code analysis

1. Start SonarQube container
```sh
make run-sonarqube
```

The above code starts SonarQube at [localhost:9000](http://localhost:9000/). You can login using this **credentials ->** *username:* admin and *password:* admin, after that it should requiere you change your password.

2. Add new project
<p align="center">
  <img src="static/sonarqube1.png" align="center"/>
</p>

<p align="center">
  <img src="static/sonarqube2.png" align="center"/>
</p>

<p align="center">
  <img src="static/sonarqube4.png" align="center"/>
</p>

5. Copy **projectKey** and **login** and replace on *backend/sonar-project.properties* file.
<p align="center">
  <img src="static/sonarqube5.png" align="center"/>
</p>

*backend/sonar-project.properties* file
```sh
# Organization and project keys are displayed in the right sidebar of the project homepage
sonar.organization=my_organization
sonar.projectKey=fastapi-alembic-sqlmodel-async
sonar.host.url=http://host.docker.internal:9000
sonar.login=157cc42f5b2702f470af3466610eebf38551fdd7

# --- optional properties ---

# defaults to project key
sonar.projectName=fastapi-alembic-sqlmodel-async
# defaults to 'not provided'
sonar.projectVersion=1.0

# Path is relative to the sonar-project.properties file. Defaults to .
sonar.sources=app

# Encoding of the source code. Default is default system encoding
sonar.sourceEncoding=UTF-8
```

6. Run the following command to execute a new code scan
```sh
make run-sonar-scanner
```
<p align="center">
  <img src="static/sonarqube6.png" align="center"/>
</p>

When the build is successful, you can see the SonarQube screen automatically refreshed with the analysis. If you want to export a report, you can check this [this post](https://medium.com/jrtec/static-analysis-using-sonarqube-in-a-react-webapp-dd4b335d6062).

## Inspiration and References

- [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql).
- [fastapi-sqlmodel-alembic](https://github.com/testdrivenio/fastapi-sqlmodel-alembic).
- [sqlmodel-tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/).
- [asyncer-tutorial](https://asyncer.tiangolo.com/tutorial/).
- [fastapi-pagination](https://github.com/uriyyo/fastapi-pagination).
- [fastapi-cache](https://github.com/long2ice/fastapi-cache).
- [fastapi-keycloak](https://github.com/code-specialist/fastapi-keycloak).
- [fastapi-async-sqlalchemy](https://github.com/h0rn3t/fastapi-async-sqlalchemy).
- [fastapi-minio](https://github.com/Longdh57/fastapi-minio).
- [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices).
- [pgadmin Makefile](https://gist.github.com/alldevic/b2a0573e5464fe91fd118024f33bcbaa).
- [Styling and makefiles](https://github.com/RasaHQ/rasa).
- [awesome-fastapi](https://github.com/mjhea0/awesome-fastapi).
- [Serving ML Models in Production with FastAPI and Celery](https://towardsdatascience.com/deploying-ml-models-in-production-with-fastapi-and-celery-7063e539a5db)
- [Database detup](https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-7-sqlalchemy-database-setup/)

## TODO List:

- [x] Add Custom Response model
- [x] Create sample one to many relationship
- [x] Create sample many to many relationship
- [x] Add JWT authentication
- [x] Add Pagination
- [x] Add User birthday field with timezone
- [x] Add static server
- [x] Add basic RBAC (Role base access control)
- [x] Add sample heroes, teams and groups on init db
- [x] Add cache configuration using fastapi-cache2 and redis
- [x] Create a global database pool of sessions to avoid to pass the session as dependency injection on each handle
- [x] Refactor tablename to Pascal case
- [x] Add one to one relationship sample
- [x] Add sample to upload images and store them using minio
- [x] Invalidate access and refresh tokens when the password is changed using Redis
- [x] Add shortcuts using a Makefile
- [x] Add sample async, sync and concurrent functions using asyncer
- [x] Add Black formatter and flake8 lint (Rasa as reference)
- [x] Add static code analysis using SonarQube
- [x] Function return type annotations to declare the response_model (fastapi > 0.89.0)
- [x] Add export report api in csv/xlsx files using StreamingResponse
- [x] Add production deployment orchestation using terraform + Elastic Beanstalk - AWS
- [x] Add Github actions automation for deploy on Elastic Beanstalk - AWS
- [x] Database query optimization. Many-Many use "selectin" and One-One and One-Many use "joined" [issue](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async/issues/20)
- [x] Add Enum sample column
- [x] Add docstrings
- [x] Install pg_trgm by code and add a query for smart search of users by name
- [x] Upgrade typing (Compatible just with python > 3.10)
- [x] Add sample transformers NLP models and use them globally
- [x] Add Celery samples for tasks, and schedule tasks
- [x] Migrate from traefik reverse proxy to Caddy reverse proxy for automatic ssl
- [ ] Add a nextjs sample frontend
- [ ] Add testing
- [ ] Add jsonb field on table sample
- [ ] Make that celery-sqlalchemy-scheduler works async
- [ ] Add AuthZ using oso
- [ ] Add SSL to reverse proxy on prod
- [ ] Add instructions on doc for production deployment using github actions and dockerhub (CI/CD)

- [ ] Convert repo into template using cookiecutter


PR are welcome ❤️

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the terms of the **[MIT license](LICENSE)**
