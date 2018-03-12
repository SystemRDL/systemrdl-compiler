#!/bin/bash
cd ../
pylint3 --rcfile test/pylint.rc systemrdl --ignore parser | tee test/lint.rpt
