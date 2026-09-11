.PHONY: setup format format-check lint typecheck test test-unit test-contract check security clean

setup:
	uv sync --all-packages --all-groups
	uv run pre-commit install

format:
	uv run ruff format .
	uv run ruff check --fix .

format-check:
	uv run ruff format --check .

lint:
	uv run ruff check .

typecheck:
	uv run mypy

test:
	uv run pytest -m "not gpu"

test-unit:
	uv run pytest -m unit

test-contract:
	uv run pytest -m contract

check: format-check lint typecheck test

security:
	uv export --quiet --all-packages --all-groups --no-hashes --output-file /tmp/llmopt-requirements.txt
	uv run pip-audit --requirement /tmp/llmopt-requirements.txt

clean:
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .mypy_cache -o -name .ruff_cache \) -prune -exec rm -rf {} +
	rm -rf build dist htmlcov coverage.xml .coverage
