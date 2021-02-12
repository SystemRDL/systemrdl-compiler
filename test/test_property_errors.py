
from unittest_utils import RDLSourceTestCase
from systemrdl import warnings

class TestErrors(RDLSourceTestCase):

    def test_singlepulse_errors(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_singlepulse.rdl"], None,
            r"Field 'bad1' marked as 'singlepulse' shall have width of 1"
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_singlepulse.rdl"], None,
            r"Field 'bad1' marked as 'singlepulse' shall have a reset value of 0"
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_singlepulse.rdl"], None,
            r"Field 'bad1' marked as 'singlepulse' shall be writable by software"
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_singlepulse.rdl"], None,
            r"Field 'bad2' marked as 'singlepulse' has conflicting 'onwrite' value of 'wclr'"
        )

    def test_we_wel_errors(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_we_wel.rdl"], None,
            r"Field 'bad1' sets property 'we', but the field's 'hw' property indicates is not writable by hardware"
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_we_wel.rdl"], None,
            r"Use of 'we' property on field 'bad1' that does not implement storage does not make sense"
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_we_wel.rdl"], None,
            r"Field 'bad2' sets property 'wel', but the field's 'hw' property indicates is not writable by hardware"
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_we_wel.rdl"], None,
            r"Use of 'wel' property on field 'bad2' that does not implement storage does not make sense"
        )
