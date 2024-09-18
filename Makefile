PROJECT_NAME ?= django_project
APP_NAME ?= django_app

# export PYTHONPATH := $(shell pwd):$(shell pwd)/src/apps

.PHONY: nix-setup
nix-setup: ## Setup project with Nix
	echo "use nix" >> .envrc
	direnv allow

.PHONY: create-project
	create-app: ## Create project
	python3 src/manage.py startproject $(PROJECT_NAME)

.PHONY: create-app
create-app: ## Create app
	mkdir src/apps/$(APP_NAME)
	python3 src/manage.py startapp $(APP_NAME) src/apps/$(APP_NAME)
	echo "$(APP_NAME) is created!"

.PHONY: test
test: ## Test with Pybuilder
	pyb -X -c -v

.PHONY: runserver
runserver: ## Run Django app
	python3 src/manage.py runserver
