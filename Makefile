PYTEST=uv run pytest

install_dev:
	uv sync

install:
	uv sync --no-dev

lint:
	uv run ruff check

test: lint
	$(PYTEST)

test_cov:
	# Run tests and prepare coverage report
	$(PYTEST) --cov=./ --cov-report=xml

test_with_warnings:
	# Run tests and show warnings
	$(PYTEST) -W all
