PYTEST=poetry run pytest -vrf

install_dev:
	poetry install

install:
	poetry install --no-dev

lint:
	poetry run black -S --check --diff .
	poetry run isort --check-only --diff .
	poetry run flake8 .
	poetry run mypy . --ignore-missing-imports

test: lint
	$(PYTEST)

test_cov:
	# Run tests, and prepare coverage report
	$(PYTEST) --cov ds_packages --cov v12 --cov baml --cov-report=html:htmlcov

test_with_warnings:
	# Run tests, and show warnings
	$(PYTEST) -W all
