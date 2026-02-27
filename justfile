# https://just.systems

default:
    @just --list

# run pytest in tests/ directory
test *args="tests/":
    uv run pytest --log-cli-level=INFO {{args}}

# format using ruff
format:
    uv run ruff format

# lint using ruff
lint:
    uv run ruff check

# build the project
build:
    rm dist/*
    uv build

# bump up the project version
release BUMP="":
    uv version --bump {{BUMP}}

# publish the project to pypi. Ensure that API token is set in $HOME/.pypirc
publish: build
    uv publish -u __token__
