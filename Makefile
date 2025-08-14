PROJECT_NAME ?= django_project
APP_NAME ?= django_app

.PHONY: all check clean test run
all: check clean test run

run: ## Run Django app
	python3 src/manage.py runserver

test: ## Test Django app
	echo "test"

clean:
	echo "clean"

.PHONY: check
check: ## Check the django templates
	python3 src/manage.py check --deploy

.PHONY: type-inference
type-inference:
	pyre infer -i

.PHONY: schema-update
schema-update:
	python3 src/manage.py makemigrations landing_page

.PHONY: sql-init-test
sql-init-test:
	python src/manage.py migrate landing_page 0003_initial
	python src/manage.py migrate landing_page
