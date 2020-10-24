image_name := fastapi-simple-login
port := 5432

install:
	poetry install

test: install start-db
	poetry run pytest --cov=fastapi_simple_login test/


build-db-image:
	@docker image ls | grep ${image_name} \
	|| docker build -t ${image_name} -f db.dockerfile . > /dev/null


start-db: build-db-image
	@docker container ls | grep ${image_name} \
	|| docker run -d -p ${port}:5432 -v $(pwd)/pgdata:/var/lib/postgresql/data ${image_name}:latest > /dev/null
	@sleep 2
	@echo "==> Database (postgresql) is running on port ${port}"

stop-db:
	@docker kill $(shell docker ps | grep ${image_name} | cut -d ' ' -f1) > /dev/null
	@echo "==> Database (postgresql) on port ${port} has stopped"

.PHONY: test