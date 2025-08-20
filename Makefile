PROJECT_NAME ?= django_project
APP_NAME ?= django_app

.PHONY: help
help:  ## help target to show available commands with information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all check clean test run
all: check clean test run ## Perform check clean test run at the same time

run: ## Run Django app
	python3 -m uvicorn src.portfolio.asgi:application --reload

test: ## Test Django app
	python3 ./src/manage.py test apps.landing_page.tests -v 3

clean:
	echo "clean"

.PHONY: check
check: ## Check the django templates
	python3 src/manage.py check --deploy

.PHONY: type-inference
type-inference: ## Perform static type check with Pyre
	pyre infer -i

.PHONY: schema-update
schema-update: ## Update SQL schema & create an empty migration
	python3 src/manage.py makemigrations landing_page
	python3 src/manage.py makemigrations landing_page --empty
	echo "Now copy the following code to the new empty migrated python file like"
	echo " \
		from . import init, init_reverse \
		operations = [ \
			migrations.RunPython(init, init_reverse), \
		] \
	"

.PHONY: sql-init-test
sql-init-test: ## Perform SQL migration
	python3 src/manage.py migrate landing_page

.PHONY: show-migrate
show-migrate: ## Perform SQL migration
	python3 src/manage.py showmigrations


.PHONY: sql-reset
sql-reset: ## Perform SQL reset
	echo "Deleting database..."
	rm -rf $(MAKE)/src/db.sqlite3
	echo "Deleting migrations..."
	rm -rf $(MAKE)/src/apps/landing_page/migrations/00*.py


.PHONY: generate-secretkey
generate-secretkey: ## Generate a secret key
	python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
