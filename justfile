install:
    poetry install

update:
    poetry update

local: install
    poetry run pre-commit install

lint: ruff format

lint-fix: ruff-fix format-fix

ruff:
    poetry run ruff check

ruff-fix:
    poetry run ruff check --fix

format:
    poetry run ruff format --diff

format-fix:
    poetry run ruff format

bandit:
    poetry run bandit -r fact_sorter -q

safety:
    poetry run safety scan

test:
    poetry run pytest

@test-cov:
    poetry run coverage run && poetry run coverage report
    poetry run coverage html && poetry run coverage xml --fail-under=95

build:
    poetry build
    pip install --upgrade -t package dist/fact_sorter-0.1.0-py3-none-any.whl
    rm -r dist
