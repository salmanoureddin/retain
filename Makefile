.PHONY: install run test lint format check

install:
	python -m pip install -e ".[dev]"

run:
	uvicorn retain.main:app --reload

test:
	pytest --cov=retain --cov-report=term-missing

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

check: lint test
