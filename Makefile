#!/usr/bin/make

include .env

define SERVERS_JSON
{
	"Servers": {
		"1": {
			"Name": "fastapi-alembic",
			"Group": "Servers",
			"Host": "$(DATABASE_HOST)",
			"Port": 5432,
			"MaintenanceDB": "postgres",
			"Username": "$(DATABASE_PASSWORD)",
			"SSLMode": "prefer",
			"PassFile": "/tmp/pgpassfile"
		}
	}
}
endef
export SERVERS_JSON

help:
	@echo "make"
	@echo "    install"
	@echo "        Install all packages of poetry project locally."
	@echo "    run-dev-build"
	@echo "        Run development docker compose and force build containers."
	@echo "    run-dev"
	@echo "        Run development docker compose."
	@echo "    stop-dev"
	@echo "        Stop development docker compose."
	@echo "    init-db"
	@echo "        Init database with sample data."	
	@echo "    add-dev-migration"
	@echo "        Add new database migration using alembic."
	@echo "    run-pgadmin"
	@echo "        Run pgadmin4."	
	@echo "    load-server-pgadmin"
	@echo "        Load server on pgadmin4."
	@echo "    clean-pgadmin"
	@echo "        Clean pgadmin4 data."

install:
	cd fastapi-alembic-sqlmodel-async && \
	poetry shell && \
	poetry install

run-dev-build:
	docker compose -f docker-compose-dev.yml up --build

run-dev:
	docker compose -f docker-compose-dev.yml up

stop-dev:
	docker compose -f docker-compose-dev.yml down

init-db:
	docker compose -f docker-compose-dev.yml exec fastapi_server python app/initial_data.py

add-dev-migration:
	docker compose -f docker-compose-dev.yml exec fastapi_server alembic revision --autogenerate && \
	docker compose -f docker-compose-dev.yml exec fastapi_server alembic upgrade head

run-pgadmin:
	echo "$$SERVERS_JSON" > ./pgadmin/servers.json && \
	docker volume create pgadmin_data && \
	docker compose -f pgadmin.yml up
	
load-server-pgadmin:
	docker exec -it pgadmin python /pgadmin4/setup.py --load-servers servers.json

clean-pgadmin:
	docker volume rm pgadmin_data