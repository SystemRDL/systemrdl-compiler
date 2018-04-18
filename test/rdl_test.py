#!/usr/bin/env python3

import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))

from systemrdl import RDLCompiler, RDLListener, RDLWalker

rdlc = RDLCompiler()
rdlc.compile_file("test.rdl")
top = rdlc.elaborate("my_design")

class hier_printer(RDLListener):
    def enter_Component(self, node):
        print(node.get_path(), node.inst.type_name)

RDLWalker(unroll=True).walk(top, hier_printer())

f = top.find_by_path("reg_b.asdf")
if(f):
    print(f.get_path())

