MESSAGE = "auto"


all: help

test: ## Run project tests
	@echo "Run project tests"

collect-requirements: ## Collect python requirements for the project
	@echo "Collect python requirements for the project"
	pip freeze > requirements.txt

install-requirements: ## Install python requirements for the project
	@echo "Install python requirements for the project"
	pip install -r requirements.txt

migrate: ## Generate new migration by changes between schema and db
	@echo "Generate new migration by changes between schema and db"
	python db/migrations/ revision --autogenerate -m $(MESSAGE)

upgrade: ## Upgrade db up to 1 migration
	@echo "Upgrade db up to 1 migration"
	python db/migrations/ upgrade +1

upgrade-all: ## Upgrade db up to date
	@echo "Upgrade db up to date"
	python db/migrations/ upgrade head

downgrade: ## Downgrade db down to 1 migration
	@echo "Downgrade db down to 1 migration"
	python db/migrations/ downgrade -1

downgrade-all: ## Downgrade db to base state
	@echo "Downgrade db to base state"
	python db/migrations/ downgrade base

run: ## Run application
	@echo "Run application"
	python main.py

upload: ## Upload data from source to database
	@echo "Upload data from source to database"
	python upload.py --source=$(SOURCE)

linters: ## Run linters
	@echo "Run linters"
	black . --diff
	flake8 .

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: help