install:
    poetry install

update:
    poetry update

local: install
    poetry run pre-commit install

lint: ruff format cfn-lint

lint-fix: ruff-fix format-fix

ruff:
    poetry run ruff check

ruff-fix:
    poetry run ruff check --fix

format:
    poetry run ruff format --diff

format-fix:
    poetry run ruff format

cfn-lint:
    poetry run cfn-lint template.yaml

bandit:
    poetry run bandit -r eventbus_learning -q

safety:
    poetry run safety scan

test:
    @poetry run coverage run --omit='tests/**' -m pytest tests/unit_tests
    @poetry run coverage report -m --skip-covered && poetry run coverage html -d reports
    @poetry run coverage xml -o reports/coverage.xml --fail-under=95
