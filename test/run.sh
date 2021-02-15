#!/bin/bash

set -e

this_dir="$( cd "$(dirname "$0")" ; pwd -P )"

exists () {
  type "$1" >/dev/null 2>/dev/null
}

# If ccache is installed, use that to cache C++ compilation to speed up re-runs
if exists ccache; then
    export CC="ccache gcc"
fi

# Initialize venv
venv_bin=$this_dir/.venv/bin
python3 -m venv $this_dir/.venv

#tools
python=$venv_bin/python
pytest=$venv_bin/pytest
coverage=$venv_bin/coverage
pylint=$venv_bin/pylint
mypy=$venv_bin/mypy

# Install test dependencies
$python -m pip install -U setuptools wheel
$python -m pip install pytest pytest-cov coverage pylint mypy parameterized

# Install dut
export SYSTEMRDL_REQUIRE_BINARY_BUILD=1
cd $this_dir/../
$python $this_dir/../setup.py install
cd $this_dir

# Run unit tests while collecting coverage
$pytest --cov=systemrdl
export SYSTEMRDL_DISABLE_ACCELERATOR=1
$pytest --cov=systemrdl --cov-append

# Generate coverage report
$coverage html -i -d $this_dir/htmlcov

# Also run examples in order to make sure output is up-to-date
$python $this_dir/../examples/print_hierarchy.py $this_dir/../examples/atxmega_spi.rdl > $this_dir/../docs/examples/print_hierarchy_spi.stdout

$python $this_dir/../examples/export_json.py $this_dir/../examples/tiny.rdl
mv $this_dir/out.json $this_dir/../examples/tiny.json

# Run lint
$pylint --rcfile $this_dir/pylint.rc systemrdl | tee $this_dir/lint.rpt

# Run static type checking
$mypy $this_dir/../systemrdl
