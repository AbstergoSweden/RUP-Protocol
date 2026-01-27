.PHONY: validate validate-python validate-node test test-python test-node lint lint-python lint-js lint-docs format format-python

validate: validate-python validate-node

validate-python:
	./.venv/bin/python validators/validate_rup.py protocol rup-protocol.yaml
	./.venv/bin/python validators/validate_rup.py all ./examples

validate-node:
	node validators/validate_rup.js protocol rup-protocol.yaml
	node validators/validate_rup.js all ./examples

test: test-python test-node

test-python:
	./.venv/bin/pytest

test-node:
	npm test

lint: lint-python lint-js lint-docs

lint-python:
	./.venv/bin/python -m ruff check .

lint-js:
	npm run lint:js

lint-docs:
	./.venv/bin/python tools/lint_docs.py

format: format-python

format-python:
	./.venv/bin/python -m ruff format .
