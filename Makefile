DOCKER_COMPOSE := docker-compose
DOCKER := docker
APP_NAME := books_app
.PHONY: up down build logs sort flake8 black linters

clean:
	find . -name '*.pyc' | xargs rm -rf
	find . -name '*__pycache__' | xargs rm -rf
	find . -name '*.cache' | xargs rm -rf
	rm -r .pytest_cache 2>/dev/null || true


up:
	$(DOCKER_COMPOSE) -f docker-compose-start.yml up --build -d
down:
	$(DOCKER_COMPOSE) -f docker-compose-start.yml down -v

build:
	$(DOCKER_COMPOSE) -f docker-compose-start.yml -t em-app-image:latest build

logs:
	$(DOCKER_COMPOSE) -f docker-compose-start.yml logs -f

black:
    $(DOCKER) exec $(APP_NAME) black .

sort:
   $(DOCKER) exec $(APP_NAME) isort .

flake8:
	$(DOCKER) exec $(APP_NAME) flake8 .

linters: sort black flake8