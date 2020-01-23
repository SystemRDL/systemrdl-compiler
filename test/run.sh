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

# Install test dependencies
$python -m pip install pytest pytest-cov coverage pylint

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
$coverage html -d $this_dir/htmlcov

# Also run examples in order to make sure output is up-to-date
$python $this_dir/../examples/print_hierarchy.py $this_dir/../examples/atxmega_spi.rdl > $this_dir/../docs/print_hierarchy_spi.stdout

# Run lint
$pylint --rcfile $this_dir/pylint.rc systemrdl | tee $this_dir/lint.rpt
