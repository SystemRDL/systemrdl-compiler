#!/usr/bin/env python3

import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))

from src.rdl_compiler import RDLCompiler
from src.model.walker import RDLListener, RDLUnrollWalker

rdlc = RDLCompiler()
root = rdlc.compile_file("test.rdl")
result = rdlc.elaborate("my_design")

class hier_printer(RDLListener):
    def enter_Component(self, node):
        pass
        print(node.get_path())

RDLUnrollWalker().walk(hier_printer(), result)

testme = result.get_property("testme")
print("testme =", testme.get_path())
