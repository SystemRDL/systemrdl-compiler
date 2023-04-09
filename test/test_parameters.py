
from unittest_utils import RDLSourceTestCase
import systemrdl.rdltypes as rdlt
from systemrdl import RDLCompiler

class TestParameters(RDLSourceTestCase):

    def test_spec_examples(self):
        root = self.compile(
            ["rdl_src/parameters.rdl"],
            "myAmap"
        )

        reg32  = root.find_by_path("myAmap.reg32")
        reg32a = root.find_by_path("myAmap.reg32_arr")
        reg16  = root.find_by_path("myAmap.reg16")
        reg8   = root.find_by_path("myAmap.reg8")
        mem32  = root.find_by_path("myAmap.mem32")
        mem64  = root.find_by_path("myAmap.mem64")

        with self.subTest("reg32"):
            self.assertEqual(reg32.get_property('regwidth'), 32)
            self.assertEqual(reg32.get_property('shared'), True)
            data = reg32.get_child_by_name("data")
            self.assertEqual(data.width, 31)
            self.assertEqual(data.high, 30)
            self.assertEqual(data.low, 0)

        with self.subTest("reg32a"):
            self.assertEqual(reg32a.get_property('regwidth'), 32)
            self.assertEqual(reg32a.get_property('shared'), True)
            data = reg32a.get_child_by_name("data")
            self.assertEqual(data.width, 31)
            self.assertEqual(data.high, 30)
            self.assertEqual(data.low, 0)

        with self.subTest("reg16"):
            self.assertEqual(reg16.get_property('regwidth'), 16)
            self.assertEqual(reg16.get_property('shared'), True)
            data = reg16.get_child_by_name("data")
            self.assertEqual(data.width, 15)
            self.assertEqual(data.high, 14)
            self.assertEqual(data.low, 0)

        with self.subTest("reg8"):
            self.assertEqual(reg8.get_property('regwidth'), 8)
            self.assertEqual(reg8.get_property('shared'), False)
            data = reg8.get_child_by_name("data")
            self.assertEqual(data.width, 7)
            self.assertEqual(data.high, 6)
            self.assertEqual(data.low, 0)

        with self.subTest("mem32"):
            self.assertEqual(mem32.get_property('mementries'), 4096)
            self.assertEqual(mem32.get_property('memwidth'), 32)

        with self.subTest("mem64"):
            self.assertEqual(mem64.get_property('mementries'), 4096)
            self.assertEqual(mem64.get_property('memwidth'), 64)


    def test_more(self):
        root = self.compile(
            ["rdl_src/parameters.rdl"],
            "amap2"
        )

        reg1 = root.find_by_path("amap2.reg1")
        reg2 = root.find_by_path("amap2.reg2")
        reg3 = root.find_by_path("amap2.reg3")

        with self.subTest("reg1"):
            self.assertEqual(reg1.inst.type_name, "param_reg")
            self.assertEqual(reg1.get_property('name'), "myname")
            self.assertEqual(reg1.get_property('shared'), False)
            data = reg1.get_child_by_name("data")
            self.assertEqual(data.get_property('hdl_path_slice'), ["dat"])

        with self.subTest("reg2"):
            self.assertEqual(reg2.inst.type_name, "param_reg")
            self.assertEqual(reg2.get_property('name'), "myname")
            self.assertEqual(reg2.get_property('shared'), False)
            data = reg2.get_child_by_name("data")
            self.assertEqual(data.get_property('hdl_path_slice'), ["dat"])

        with self.subTest("reg3"):
            self.assertEqual(reg3.inst.type_name, "param_reg_NAME_a36638b4_SHARED_t_FIELD_SLICES_184d423e")
            self.assertEqual(reg3.get_property('name'), "othername")
            self.assertEqual(reg3.get_property('shared'), True)
            data = reg3.get_child_by_name("data")
            self.assertEqual(data.get_property('hdl_path_slice'), ["foo"])


    def test_nested(self):
        root = self.compile(
            ["rdl_src/parameters.rdl"],
            "nested"
        )
        f1 = root.find_by_path("nested.rf_inst.r_inst1.f")
        f2 = root.find_by_path("nested.rf_inst.r_inst2.f")
        f3 = root.find_by_path("nested.r1_inst.f")

        with self.subTest("f1"):
            self.assertEqual(f1.width, 4)

        with self.subTest("f2"):
            self.assertEqual(f2.width, 4)

        with self.subTest("f3"):
            self.assertEqual(f3.width, 5)


    def test_elab_defaults(self):
        root = self.compile(
            ["rdl_src/parameters.rdl"],
            "elab_params",
            parameters={}
        )

        f1 = root.find_by_path("elab_params.r1.f")
        f2 = root.find_by_path("elab_params.r2.f")
        f3 = root.find_by_path("elab_params.r3.f")

        self.assertEqual(f1.width, 1)
        self.assertEqual(f2.width, 2)
        self.assertEqual(f3.width, 3)
        self.assertEqual(f1.get_property('onwrite'), rdlt.OnWriteType.woset)
        self.assertEqual(f2.get_property('donttest'), True)
        self.assertEqual(f3.get_property('name'), "default")


    def test_elab_override(self):
        root = self.compile(
            ["rdl_src/parameters.rdl"],
            "elab_params",
            parameters={
                "STR":"python!",
                "INT": 5,
                "INTARR": [6,7],
                "ONWR": rdlt.OnWriteType.woclr,
                "BOOL": False
            }
        )

        f1 = root.find_by_path("elab_params.r1.f")
        f2 = root.find_by_path("elab_params.r2.f")
        f3 = root.find_by_path("elab_params.r3.f")

        self.assertEqual(f1.width, 5)
        self.assertEqual(f2.width, 6)
        self.assertEqual(f3.width, 7)
        self.assertEqual(f1.get_property('onwrite'), rdlt.OnWriteType.woclr)
        self.assertEqual(f2.get_property('donttest'), False)
        self.assertEqual(f3.get_property('name'), "python!")

    def test_elab_override_via_eval(self):
        rdlc = RDLCompiler()
        root = self.compile(
            ["rdl_src/parameters.rdl"],
            "elab_params",
            parameters={
                "STR": rdlc.eval('"python!"'),
                "INT":  rdlc.eval('5'),
                "INTARR":  rdlc.eval("'{6,7}"),
                "ONWR":  rdlc.eval('woclr'),
                "BOOL":  rdlc.eval('100/2 - 50')
            }
        )

        f1 = root.find_by_path("elab_params.r1.f")
        f2 = root.find_by_path("elab_params.r2.f")
        f3 = root.find_by_path("elab_params.r3.f")

        self.assertEqual(f1.width, 5)
        self.assertEqual(f2.width, 6)
        self.assertEqual(f3.width, 7)
        self.assertEqual(f1.get_property('onwrite'), rdlt.OnWriteType.woclr)
        self.assertEqual(f2.get_property('donttest'), False)
        self.assertEqual(f3.get_property('name'), "python!")

    def test_param_scope(self):
        root = self.compile(
            ["rdl_src/parameters.rdl"],
            "param_scope"
        )
        ffX = root.find_by_path("param_scope.rfX.rf3.rf2.rr.ff")
        ffY = root.find_by_path("param_scope.rfY.rf3.rf2.rr.ff")
        ffZ = root.find_by_path("param_scope.rfZ.rf3.rf2.rr.ff")

        self.assertEqual(ffX.width, 2)
        self.assertEqual(ffY.width, 3)
        self.assertEqual(ffZ.width, 1)

    def test_err_ref_in_parameter(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_ref_in_parameter.rdl"],
            "parameters1",
            r"Parameter 'PARAM' contains a reference. SystemRDL does not allow component references inside parameter values."
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_ref_in_parameter.rdl"],
            "parameters2",
            r"Parameter 'PARAM' contains a reference. SystemRDL does not allow component references inside parameter values."
        )
