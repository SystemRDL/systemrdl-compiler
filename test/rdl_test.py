#!/usr/bin/env python3

import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))

from systemrdl import RDLCompiler, RDLListener, RDLUnrollWalker

rdlc = RDLCompiler()
rdlc.compile_file("test.rdl")
top = rdlc.elaborate("my_design")

class hier_printer(RDLListener):
    def enter_Component(self, node):
        pass
        print(node.get_path())

RDLUnrollWalker().walk(hier_printer(), top)

testme = top.get_property("testme")
print("testme =", testme.get_path())

f = top.find_by_path("reg_b.asdf")
if(f):
    print(f.get_path())

