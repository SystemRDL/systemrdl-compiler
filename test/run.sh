#!/bin/bash

set -e

cd "$(dirname "$0")"

exists () {
    type "$1" >/dev/null 2>/dev/null
}

# If ccache is installed, use that to cache C++ compilation to speed up re-runs
if exists ccache; then
    export CC="ccache gcc"
    export CXX="ccache g++"
fi

# Initialize venv
python3 -m venv .venv
source .venv/bin/activate

# Install
export SYSTEMRDL_REQUIRE_BINARY_BUILD=1
python -m pip install -U ..
python -m pip install -r requirements.txt pytest-parallel

# Run unit tests while collecting coverage
pytest --cov=systemrdl
export SYSTEMRDL_DISABLE_ACCELERATOR=1
pytest

# Generate coverage report
coverage html -i -d htmlcov

# Also run examples in order to make sure output is up-to-date
../examples/print_hierarchy.py ../examples/atxmega_spi.rdl > ../docs/examples/print_hierarchy_spi.stdout
../examples/export_json.py ../examples/tiny.rdl
mv out.json ../examples/tiny.json

# Run lint
pylint --rcfile pylint.rc -j 0 systemrdl

# Run static type checking
mypy ../src/systemrdl
