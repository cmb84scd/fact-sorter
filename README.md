# Fact Sorter

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![security: safety](https://img.shields.io/badge/security-safety-blue)](https://github.com/pyupio/safety)
[![Pipeline CI](https://github.com/cmb84scd/fact-sorter/actions/workflows/pipeline.yml/badge.svg)](https://github.com/cmb84scd/fact-sorter/actions?query=branch:main)
![Code Coverage](https://img.shields.io/badge/Code%20Coverage-100%25-success?style=flat)

- [Overview](#overview)
- [Setup](#setup)
  - [Python](#python)
  - [Poetry](#poetry)
  - [AWS CDK](#aws-cdk)
  - [Just](#just)
  - [Project](#project)
- [Commands](#commands)
- [Architecture](#architecture)

## Overview

A project to sort facts using AWS lambdas and an event bus. Created as part of my learning to help me better understand how to use event buses.

## Setup

To use this project, you will need to have the following installed.

### Python

This project uses Python version 3.12. It is advised to use [pyenv](https://github.com/pyenv/pyenv) to install Python using:

```bash
pyenv install
```

### Poetry

This project uses poetry version 1.8.3. To install poetry, follow the instructions [here](https://python-poetry.org/docs/) or to update it if you already have it installed run:

```bash
poetry self update
```

### AWS CDK

This project uses the AWS CDK to define the cloud infrastructure in code. To install it you can follow the instructions [here](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html).

### Just

This project uses just to run the lint, test, etc commands. To use just you will need to install it but if you'd prefer not to, you can copy the commands from the `justfile` and paste them directly into your terminal to run them. To install just, follow the instructions [here](https://just.systems/man/en/).

### Project

Having installed the above, you can now clone the repository and install the dependencies, along with the pre-commit hook:

```bash
git clone git@github.com:cmb84scd/fact-sorter.git
cd fact-sorter
just local
```

## Commands

All commands are defined in the `justfile` and are run as `just {command}` where `{command}` is one of:

| Name     | Description                            |
| ----     | -------------------------------------- |
| build    | Builds the project                     |
| test     | Runs all the unit tests                |
| test-cov | Runs all the unit tests with coverage  |
| lint     | Runs all the linting checks            |
| lint-fix | Automatically fixes any linting issues |

I haven't listed all the commands here, but you can see them all by looking in the `justfile`.

Please note, before running the tests ensure that node is activated as it is needed by the CDK tests and that you have built the project. Also, if running `cdk synth`, you will need to add a `.env` file and put the following in it, replacing the values with your details:

```bash
AWS_ACCOUNT_ID='your-account-id'
AWS_REGION='your-aws-region'
```

## Architecture

Find an [in depth view of the architecture here](docs/ARCHITECTURE.md)
