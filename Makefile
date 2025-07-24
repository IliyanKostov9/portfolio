PROJECT_NAME ?= django_project
APP_NAME ?= django_app

.PHONY: all clean test run
all: clean test run

run: ## Run Django app
	python3 src/manage.py runserver

test: ## Test Django app
	echo "test"

clean:
	echo "clean"

.PHONY: create-project
	create-app: ## Create project
	python3 src/manage.py startproject $(PROJECT_NAME)

.PHONY: create-app
create-app: ## Create app
	mkdir src/apps/$(APP_NAME)
	python3 src/manage.py startapp $(APP_NAME) src/apps/$(APP_NAME)
	echo "$(APP_NAME) is created!"

.PHONY: type-inference
type-inference:
	pyre infer -i

.PHONY: gen-models
gen-models:
	python3 src/manage.py makemigrations landing_page

.PHONY: get-sql
get-sql:
	python3 src/manage.py sqlmigrate landing_page 0001


.PHONY: sync
sync:
	python3 src/manage.py migrate
