##########################
# TARGET
# #######################

.PHONY: help
help:  ## help target to show available commands with information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all check clean test run
all: check clean test run ## Perform check clean test run at the same time

run: ## Run Django app
	python3 -m uvicorn src.portfolio.asgi:application --reload

test: ## Test Django app
	python3 -Wa ./src/manage.py test apps.resume.tests -v 3
	python3 -Wa ./src/manage.py test apps.blogs.tests -v 3

clean:
	echo "clean"

.PHONY: check
check: ## Check the django templates
	python3 src/manage.py check --deploy

.PHONY: migrate-check
migrate-check: ## Check if the migrations are compatible
	  python3 src/manage.py lintmigrations

.PHONY: sql-reset
sql-reset: ## Perform SQL reset
	echo "Deleting database..."
	rm -rf $(PWD)/src/db.sqlite3
	echo "Deleting migrations..."
	rm -rf $(PWD)/src/apps/resume/migrations/00*.py
	rm -rf $(PWD)/src/apps/blogs/migrations/00*.py

.PHONY: migrate
migrate: ## Perform SQL migration
	python3 src/manage.py migrate resume
	python3 src/manage.py migrate blogs

.PHONY: schema-update
schema-update: ## Update SQL schema & create an empty migration
	python3 src/manage.py makemigrations resume
	python3 src/manage.py makemigrations resume --empty --name resume_migrate
	python3 src/manage.py makemigrations blogs
	python3 src/manage.py makemigrations blogs --empty --name blogs_migrate
	echo "Now copy the following code to the new empty migrated python file like"
	echo " \
		from . import init, init_reverse \
		operations = [ \
			migrations.RunPython(init, init_reverse), \
		] \
	"

.PHONY: show-migrate
show-migrate: ## Perform SQL migration
	python3 src/manage.py showmigrations


.PHONY: generate-secretkey
generate-secretkey: ## Generate a secret key
	python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

.PHONY: translate
translate: ## Translate text into the 4 languages
	django-admin makemessages -l en
	django-admin makemessages -l bg
	django-admin makemessages -l fr
	django-admin makemessages -l ge
	django-admin compilemessages

.PHONY: tr-compile
tr-compile: ## Complie the translated .po files
	django-admin compilemessages

.PHONY: latex-compile
latex-compile:
	cd docs && \
	latexmk -C main.tex && \
	latexmk -pdf -pvc -interaction=nonstopmode -pv main.tex || true && \
	zathura main.pdf


