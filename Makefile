.PHONY: setup doctor dev-up dev-down format format-check lint typecheck test test-unit test-contract test-integration test-e2e test-gpu-smoke check build security clean

setup:
	uv sync --all-packages --all-groups
	uv run pre-commit install

doctor:
	./scripts/doctor.sh

dev-up:
	@echo "dev-up is unavailable in this milestone; no local service runtime exists."
	@false

dev-down:
	@echo "dev-down is unavailable in this milestone; no local service runtime exists."
	@false

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
	uv run pytest -m "not gpu and not performance and not slow"

test-unit:
	uv run pytest -m unit

test-contract:
	uv run pytest -m contract

test-integration:
	uv run pytest -m integration

test-e2e:
	@echo "test-e2e is unavailable in this milestone; no end-to-end runtime exists."
	@false

test-gpu-smoke:
	uv run pytest -m "gpu and smoke"

check:
	./scripts/check.sh

build:
	uv build --all-packages

security:
	uv export --quiet --all-packages --all-groups --no-hashes --output-file /tmp/llmopt-requirements.txt
	uv run pip-audit --requirement /tmp/llmopt-requirements.txt

clean:
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .mypy_cache -o -name .ruff_cache \) -prune -exec rm -rf {} +
	rm -rf build dist htmlcov coverage.xml .coverage
