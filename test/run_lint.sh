#!/bin/bash
cd ../
pylint3 --rcfile test/pylint.rc src --ignore parser | tee test/lint.rpt
