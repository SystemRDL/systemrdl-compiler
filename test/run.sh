#!/bin/bash

# Usage (from anywhere):
#   test/run.sh

set -e

cd "$(dirname "$0")/.."

# Fail loudly if the C++ accelerator can't be built
export SYSTEMRDL_REQUIRE_BINARY_BUILD=1

# Run twice. with/without C++ accelerator
uv run --directory test pytest --cov=systemrdl
SYSTEMRDL_DISABLE_ACCELERATOR=1 uv run --directory test pytest

# Generate coverage report
uv run --directory test coverage html -i -d htmlcov

# Also run examples in order to make sure output is up-to-date
uv run examples/print_hierarchy.py examples/atxmega_spi.rdl > docs/examples/print_hierarchy_spi.stdout
uv run --directory examples export_json.py tiny.rdl
mv examples/out.json examples/tiny.json

# Run lint
uv run pylint --rcfile test/pylint.rc -j 0 src/systemrdl

# Run static type checking
uv run mypy --config-file test/mypy.ini src/systemrdl
