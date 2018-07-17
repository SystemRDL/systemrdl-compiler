#!/bin/bash

set -e

this_dir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $this_dir/../


# Run unit tests while collecting coverage
coverage3 run $this_dir/../setup.py test
coverage3 html -d $this_dir/htmlcov

# Also run examples in order to make sure output is up-to-date
$this_dir/../examples/print_hierarchy.py $this_dir/../examples/atxmega_spi.rdl > $this_dir/../docs/print_hierarchy_spi.stdout

# Run lint
pylint --rcfile $this_dir/pylint.rc systemrdl | tee $this_dir/lint.rpt
