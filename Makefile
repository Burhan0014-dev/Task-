.DEFAULT_GOAL := help

# Define targets and their commands
.PHONY: help
help: ## Display this help message
	@echo "Available targets:"
	@echo "  run           Run the Django project locally"
	@echo "  build         Build Docker containers"
	@echo "  up            Start Docker containers in the background"
	@echo "  down          Stop and remove Docker containers"
	@echo "  runserver     Run Django development server using Docker"
	@echo "  local         Run Django development server locally"

build:
    
	docker-compose build --no-cache --force-rm

up:
	docker-compose up -d

down:
	docker-compose down

runserver:
	docker-compose exec djangoapp python manage.py runserver 0.0.0.0:8000

local:
	python manage.py runserver

test:
	poetry run pytest --cov=task --cov-report=term --cov-report=html --cov-config=.coveragerc

