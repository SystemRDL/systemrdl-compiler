from unittest_utils import RDLSourceTestCase
import systemrdl.rdltypes as rdlt
from systemrdl import warnings, RDLCompiler, RDLCompileError


class TestInterleavedArrays(RDLSourceTestCase):

    def test_interleaved_arrays(self):
        top = self.compile(
            ["rdl_src/interleaved_arrays.rdl"],
            "interleaved_arrays_test"
        ).top
        self.assertEqual(top.type_name, "interleaved_arrays_test")
        
    def test_interleaved_arrays_2(self):
        top = self.compile(
            ["rdl_src/interleaved_arrays.rdl"],
            "interleaved_arrays_test_2"
        ).top
        self.assertEqual(top.type_name, "interleaved_arrays_test_2")