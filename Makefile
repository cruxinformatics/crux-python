# -*- mode: make; tab-width: 4; indent-tabs-mode: t -*-
# vim: ft=make noexpandtab tabstop=4 shiftwidth=4 softtabstop=4

.DEFAULT_GOAL := help

# This needs to be the first target
.PHONY: help
help: ## Print this help message
	@echo 'Usage: make <command>'
	@echo
	@echo 'Commands:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / \
		{printf "    \033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: lint
lint: ## Run lint tests
	nox -s lint
	nox -s type_check

.PHONY: unit
unit: ## Run unit tests
	nox -s unit

.PHONY: integration
integration: ## Run integration tests
	nox -s integration

.PHONY: format_check
format_check: ## Check formatting of code without changing it
	nox -s format_check

.PHONY: format
format: ## Format code
	black .

.PHONY: test
test: ## Run all tests
	nox

.PHONY: lock
lock: ## Generate Pipfile.lock and requirements.txt
	pipenv lock
	pipenv lock --requirements > requirements.txt
	pipenv lock --dev --requirements > requirements-dev.txt

.PHONY: package
package: ## Package for distribution
	rm -rf dist && \
	python setup.py bdist_wheel

.PHONY: docs
docs: ## Generate sphinx HTML documentation
	cd docs && \
	sphinx-apidoc -o ./ ../crux && \
	make html
