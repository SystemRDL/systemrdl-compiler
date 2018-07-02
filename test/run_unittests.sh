#!/bin/bash

#python3 -m unittest discover

coverage3 run rdl_unittest.py
coverage3 html

# Also run examples in order to make sure output is up-to-date
../examples/print_hierarchy.py ../examples/atxmega_spi.rdl > ../docs/print_hierarchy_spi.stdout
