run-tests:
	docker-compose -f infra/docker-compose.yml up -d psql_test
	pytest tests -p no:warnings
	docker-compose -f infra/docker-compose.yml stop psql_test

run-build:
	docker-compose -f infra/docker-compose.yml build

run-database:
	docker-compose -f infra/docker-compose.yml up -d pgbouncer

run-database-test:
	docker-compose -f infra/docker-compose.yml up -d psql_test

run-server:
	docker-compose -f infra/docker-compose.yml up nomades

run-dev-server:
	docker-compose -f infra/docker-compose.yml up -d pgbouncer
	python main.py

down-server:
	docker-compose -f infra/docker-compose.yml down

down-app:
	docker compose -f infra/docker-compose.yml down nomades

down-pgbouncer:
	docker-compose -f infra/docker-compose.yml down pgbouncer
