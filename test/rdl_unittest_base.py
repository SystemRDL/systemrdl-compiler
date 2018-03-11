import unittest
import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))

from src.rdl_compiler import RDLCompiler

class RDLSourceTestCase(unittest.TestCase):
    """
    Base class for SystemRDL unittest TestCase
    Implements mechanisms and tests common to interpreting an RDL testcase file
    """
    def compile(self, files, top_name):
        rdlc = RDLCompiler()
        for file in files:
            rdlc.compile_file(os.path.join(this_dir, file))
        return(rdlc.elaborate(top_name))
    