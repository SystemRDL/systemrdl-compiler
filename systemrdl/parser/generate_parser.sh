#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"

antlr4="java -Xmx500M -cp /usr/local/lib/antlr-4.7.2-complete.jar org.antlr.v4.Tool"
antlr4py3="$antlr4 -Dlanguage=Python3"

$antlr4py3 -visitor -no-listener SystemRDL.g4
