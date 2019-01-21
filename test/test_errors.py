
from .unittest_utils import RDLSourceTestCase
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
    
    def test_validation_error(self):
        self.assertRDLCompileError(
            ["rdl_testcases/err_validate.rdl"],
            None,
            r"Instance 'r2' at offset \+0x100:0x103 overlaps with 'r1' at offset \+0x100:0x103"
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
