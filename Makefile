# ########################
# VARIABLES
# #######################

LATEX_LANG ?= en
APP_PATH ?= ./infra/iac
VAR_FILE_PATH ?= ./env/prod

# ########################
# TARGET
# #######################

.PHONY: help
help:  ## help target to show available commands with information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all clean test run
all: clean test run ## Perform check clean test run at the same time

run: ## Run Django app
	python3 -m uvicorn src.portfolio.asgi:application --reload

clean:
	echo "clean"

.PHONY: sql-reset
sql-reset: ## Perform SQL reset
	echo "Deleting database..."
	rm -rf $(PWD)/src/db.sqlite3
	echo "Deleting migrations..."
	rm -rf $(PWD)/src/apps/common/migrations/00*.py
	rm -rf $(PWD)/src/apps/resume/migrations/00*.py
	rm -rf $(PWD)/src/apps/blogs/migrations/00*.py

.PHONY: migrate
migrate: ## Perform SQL migration
	python3 src/manage.py migrate common
	python3 src/manage.py migrate resume
	python3 src/manage.py migrate blogs

.PHONY: schema-update
schema-update: ## Update SQL schema & create an empty migration
	python3 src/manage.py makemigrations common
	python3 src/manage.py makemigrations common --empty --name common_migrate
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
	latexmk -pdf -pvc -interaction=nonstopmode -pdflatex="xelatex -interaction=nonstopmode '\def\lang{$(LATEX_LANG)}\input{main.tex}'" \
	main.tex || true && \
	zathura main.pdf

.PHONY: tf-init
tf-init: ## Initialize infa via Terraform
	terraform -chdir=$(APP_PATH) \
		init \
		-var-file="$(VAR_FILE_PATH)/terraform.tfvars" \
		-no-color

.PHONY: tf-validate
tf-validate: ## Validate infa via Terraform
	terraform -chdir=$(APP_PATH) \
		validate \
		-no-color

.PHONY: tf-plan
tf-plan: ## Plan infa via Terraform
	terraform -chdir=$(APP_PATH) \
		plan \
		-var-file="$(VAR_FILE_PATH)/terraform.tfvars" \
		-no-color

.PHONY: tf-apply
tf-apply: ## Apply infa via Terraform
	terraform -chdir=$(APP_PATH) \
		apply \
		-var-file="$(VAR_FILE_PATH)/terraform.tfvars" \
		-no-color \
		-auto-approve \
		-input=false

.PHONY: tf-destroy
tf-destroy: ## Apply infa via Terraform
	terraform -chdir=$(APP_PATH) \
		destroy \
		-var-file="$(VAR_FILE_PATH)/terraform.tfvars" \
		-no-color \
		-auto-approve \
		-input=false

.PHONY: encrypt-file
encrypt-file: ## Encrypt a file
	age -r $(AGE_KEY) $(FILE) > $(FILE).age

.PHONY: decrypt-file
decrypt-file: ## Decrypt a file
	age -d -i $(AGE_KEY) $(FILE) > $(FILE:.age=)

.PHONY: encrypt-files
encrypt-files: ## Encrypt a set of files, given a directory and an extension
	for file in $$(find $(DIR) -name "*.$(EXT)"); do \
		age -r $(AGE_KEY) $$file > $$file.age; \
	done

.PHONY: decrypt-files
decrypt-files: ## Decrypt a set of files, given a directory and an extension
	for file in $$(find $(DIR) -name "*.$(EXT).age"); do \
		age -d -i $(AGE_KEY) $$file > $${file%.age}; \
	done
