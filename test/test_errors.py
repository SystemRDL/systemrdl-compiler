
from unittest_utils import RDLSourceTestCase
from systemrdl import warnings

class TestErrors(RDLSourceTestCase):

    def test_syntax_error(self):
        self.assertRDLCompileError(
            ["rdl_testcases/err_syntax.rdl"],
            None,
            r"mismatched input '\}'"
        )
    
    def test_compile_error(self):
        self.assertRDLCompileError(
            ["rdl_testcases/err_compile.rdl"],
            None,
            r"Could not resolve hierarchical reference to 'badpath'"
        )
    
    def test_reg_overlap(self):
        self.assertRDLCompileError(
            ["rdl_testcases/err_validate.rdl"],
            "reg_overlap",
            r"Instance 'r2' at offset \+0x100:0x103 overlaps with 'r1' at offset \+0x100:0x103"
        )

    def test_reg_array_overlap(self):
        self.assertRDLCompileError(
            ["rdl_testcases/err_validate.rdl"],
            "reg_array_overlap",
            r"Instance array 'r_array' has address stride 0x1, but the element size is 0x4"
        )

    def test_regfile_array_overlap(self):
        self.assertRDLCompileError(
            ["rdl_testcases/err_validate.rdl"],
            "regfile_array_overlap",
            r"Instance array 'rf_array' has address stride 0x1, but the element size is 0x100"
        )


class TestUserErrors(RDLSourceTestCase):
    def setUp(self):
        super().setUp()
        self.compiler_error_flags = warnings.ALL

    def test_field_pack_user_error(self):

        self.assertRDLCompileError(
            ["rdl_testcases/field_packing.rdl"],
            "lsb_packing",
            r"Bit offset for field 'x' is not explicit"
        )
