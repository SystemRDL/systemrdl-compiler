#!/usr/bin/env python3

import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))

from src.rdl_compiler import RDLCompiler

rdlc = RDLCompiler()
root = rdlc.compile_file("test.rdl")
result = rdlc.elaborate("my_design")

