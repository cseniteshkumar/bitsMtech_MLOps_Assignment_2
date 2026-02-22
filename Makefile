.help:
	@echo "MLOps CI/CD Helper Commands"
	@echo "============================"
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install all dependencies"
	@echo "  make dev-install   - Install with dev tools (testing, linting)"
	@echo "  make run           - Run the FastAPI application"
	@echo "  make test          - Run all tests"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make lint          - Run all linting checks"
	@echo "  make format        - Format code with black and isort"
	@echo "  make format-check  - Check formatting without changes"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run container with docker-compose"
	@echo "  make docker-stop   - Stop containers"
	@echo "  make docker-logs   - View container logs"
	@echo ""
	@echo "CI/CD:"
	@echo "  make local-ci      - Run local CI tests (like GitHub Actions)"
	@echo "  make clean         - Remove temporary files and caches"
	@echo "  make venv          - Create Python virtual environment"
	@echo ""

.PHONY: help venv install dev-install run test test-cov lint format format-check docker-build docker-run docker-stop docker-logs local-ci clean

help: .help

venv:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip

install:
	pip install -r requirements_fastapi.txt

dev-install:
	pip install -r requirements_fastapi.txt
	pip install pytest pytest-cov pytest-asyncio
	pip install flake8 black isort pylint
	pip install bandit safety pip-audit
	pip install locust

run:
	python -m app.main

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	@echo "Running flake8..."
	flake8 app/ tests/ --max-line-length=127 --statistics || true
	@echo ""
	@echo "Running pylint..."
	pylint app/ --disable=all --enable=E,F --fail-under=9 || true

format:
	@echo "Formatting with black..."
	black app/ tests/
	@echo "Sorting imports with isort..."
	isort app/ tests/

format-check:
	@echo "Checking code formatting..."
	black --check app/ tests/ --diff
	@echo ""
	@echo "Checking import ordering..."
	isort --check-only app/ tests/ --diff

docker-build:
	docker build -t mlops-classifier:latest .

docker-run:
	docker-compose up --build

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f api

local-ci:
	@echo "Running local CI tests..."
	./run-local-ci-tests.sh

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/ build/ *.egg-info/
	rm -rf .venv venv/

.PHONY: .help
