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
    poetry run bandit -r eventbus_learning -q

safety:
    poetry run safety scan

test:
    @poetry run pytest \
        --cov-report term:skip-covered \
        --cov-report html:reports \
        --cov-report xml:reports/coverage.xml \
        --junitxml=reports/unit_test_report.xml \
        --cov-fail-under=95 \
        --cov=eventbus_learning tests/unit_tests -ra -s
