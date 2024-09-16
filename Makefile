export PYTHONPATH := $(shell pwd)

.PHONY: test
test: ## Test with Pybuilder
	pyb -X -c -v

.PHONY: runserver
runserver: ## Run Django app
	python3 src/manage.py runserver
