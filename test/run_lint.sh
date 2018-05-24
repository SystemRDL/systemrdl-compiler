#!/bin/bash
cd ../
pylint3 --rcfile test/pylint.rc systemrdl | tee test/lint.rpt
