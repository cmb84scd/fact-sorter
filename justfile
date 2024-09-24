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

@test:
    poetry run coverage run && poetry run coverage report
    poetry run coverage html && poetry run coverage xml --fail-under=95
