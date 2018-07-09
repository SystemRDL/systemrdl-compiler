#!/usr/bin/env python3

import sys
import os

# Ignore this. Only needed for this example
this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))


from systemrdl import RDLCompiler, RDLListener, RDLWalker, RDLCompileError
from systemrdl.node import FieldNode

# Collect input files from the command line arguments
input_files = sys.argv[1:]


# Create an instance of the compiler
rdlc = RDLCompiler()


try:
    # Compile all the files provided
    for input_file in input_files:
        rdlc.compile_file(input_file)
    
    # Elaborate the design
    root = rdlc.elaborate()
except RDLCompileError:
    # A compilation error occurred. Exit with error code
    sys.exit(1)


# Define a listener that will print out the register model hierarchy
class MyModelPrintingListener(RDLListener):
    def __init__(self):
        self.indent = 0
        
    def enter_Component(self, node):
        if not isinstance(node, FieldNode):
            print("\t"*self.indent, node.get_path_segment())
            self.indent += 1
    
    def enter_Field(self, node):
        # Print some stuff about the field
        bit_range_str = "[%d:%d]" % (node.inst.high, node.inst.low)
        sw_access_str = "sw=%s" % node.get_property("sw").name
        print("\t"*self.indent, bit_range_str, node.get_path_segment(), sw_access_str)
    
    def exit_Component(self, node):
        if not isinstance(node, FieldNode):
            self.indent -= 1


# Traverse the register model!
walker = RDLWalker(unroll=True)
listener = MyModelPrintingListener()
walker.walk(root, listener)
