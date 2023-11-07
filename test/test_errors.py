
from unittest_utils import RDLSourceTestCase
from systemrdl import warnings

class TestErrors(RDLSourceTestCase):

    def test_syntax_error(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_syntax.rdl"],
            None,
            r"mismatched input '\}'"
        )

    def test_compile_error(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_compile.rdl"],
            None,
            r"Could not resolve hierarchical reference to 'badpath'"
        )

    def test_reg_overlap(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_validate.rdl"],
            "reg_overlap",
            r"Instance 'r2' at offset \+0x100:0x103 overlaps with 'r1' at offset \+0x100:0x103"
        )

    def test_reg_array_overlap(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_validate.rdl"],
            "reg_array_overlap",
            r"Instance array 'r_array' has address stride 0x1, but the element size is 0x4"
        )

    def test_regfile_array_overlap(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_validate.rdl"],
            "regfile_array_overlap",
            r"Instance array 'rf_array' has address stride 0x1, but the element size is 0x100"
        )

    def test_bad_addr_allocators(self):
        with self.subTest("addr"):
            self.assertRDLCompileError(
                ["rdl_err_src/err_allocators1.rdl"],
                None,
                r"Unexpected address allocation operator for non-addressable instance"
            )

        with self.subTest("stride"):
            self.assertRDLCompileError(
                ["rdl_err_src/err_allocators2.rdl"],
                None,
                r"Unexpected address allocation operator for non-addressable instance"
            )

        with self.subTest("align"):
            self.assertRDLCompileError(
                ["rdl_err_src/err_allocators3.rdl"],
                None,
                r"Unexpected address allocation operator for non-addressable instance"
            )

    def test_bad_mem_child(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_mem_defs.rdl"],
            None,
            r"Definitions of 'addrmap' components not allowed inside a mem definition"
        )

    def test_incomplete_struct(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_incomplete_struct.rdl"],
            None,
            r"Incomplete struct literal 'struct_t'. The following members are undefined: b"
        )


class TestUserErrors(RDLSourceTestCase):
    def setUp(self):
        super().setUp()
        self.compiler_error_flags = warnings.ALL

    def test_field_pack_user_error(self):

        self.assertRDLCompileError(
            ["rdl_src/field_packing.rdl"],
            "lsb_packing",
            r"Bit offset for field 'x' is not explicit"
        )
