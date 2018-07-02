#!/bin/bash

rm -rf dist

python3 setup.py sdist
twine upload --repository-url https://pypi.org/legacy/ dist/*
