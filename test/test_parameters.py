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


    def test_param_types(self):
        root = self.compile(
            ["rdl_src/param_types.rdl"],
            "param_types"
        )

        reg1 = root.find_by_path("param_types.reg1")
        reg2 = root.find_by_path("param_types.reg2")
        reg3 = root.find_by_path("param_types.reg3")

        with self.subTest("reg1"):
            self.assertEqual(reg1.type_name, "param_reg")
            self.assertEqual(reg1.get_property('name'), "myname")
            self.assertEqual(reg1.get_property('shared'), False)
            data = reg1.get_child_by_name("data")
            self.assertEqual(data.get_property('hdl_path_slice'), ["dat"])

        with self.subTest("reg2"):
            self.assertEqual(reg2.type_name, "param_reg")
            self.assertEqual(reg2.get_property('name'), "myname")
            self.assertEqual(reg2.get_property('shared'), False)
            data = reg2.get_child_by_name("data")
            self.assertEqual(data.get_property('hdl_path_slice'), ["dat"])

        with self.subTest("reg3"):
            self.assertEqual(reg3.type_name, "param_reg_NAME_a36638b4_SHARED_t_FIELD_SLICES_184d423e")
            self.assertEqual(reg3.get_property('name'), "othername")
            self.assertEqual(reg3.get_property('shared'), True)
            data = reg3.get_child_by_name("data")
            self.assertEqual(data.get_property('hdl_path_slice'), ["foo"])


    def test_nested(self):
        root = self.compile(
            ["rdl_src/nested_params.rdl"],
            "nested_params"
        )
        f1 = root.find_by_path("nested_params.rf_inst.r_inst1.f")
        f2 = root.find_by_path("nested_params.rf_inst.r_inst2.f")
        f3 = root.find_by_path("nested_params.r1_inst.f")

        with self.subTest("f1"):
            self.assertEqual(f1.width, 4)

        with self.subTest("f2"):
            self.assertEqual(f2.width, 4)

        with self.subTest("f3"):
            self.assertEqual(f3.width, 5)


    def test_elab_defaults(self):
        root = self.compile(
            ["rdl_src/elab_params.rdl"],
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
            ["rdl_src/elab_params.rdl"],
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
            ["rdl_src/elab_params.rdl"],
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
            ["rdl_src/param_scope.rdl"],
            "param_scope"
        )
        ffX = root.find_by_path("param_scope.rfX.rf3.rf2.rr.ff")
        ffY = root.find_by_path("param_scope.rfY.rf3.rf2.rr.ff")
        ffZ = root.find_by_path("param_scope.rfZ.rf3.rf2.rr.ff")

        self.assertEqual(ffX.width, 2)
        self.assertEqual(ffY.width, 3)
        self.assertEqual(ffZ.width, 1)

    def test_param_dpa_scopes(self):
        root = self.compile(
            ["rdl_src/param_dpa_scopes.rdl"],
            "param_dpa_scopes"
        )
        top = root.top
        d = top.find_by_path("reg_default")
        df = top.find_by_path("reg_default.f")
        o1 = top.find_by_path("reg_override1")
        o1f = top.find_by_path("reg_override1.f")
        o2 = top.find_by_path("reg_override2")
        o2f = top.find_by_path("reg_override2.f")

        self.assertEqual(d.get_property("desc"), "reg default")
        self.assertEqual(df.get_property("desc"), "reg default")
        self.assertEqual(o1.get_property("desc"), "top default")
        self.assertEqual(o1f.get_property("desc"), "top default")
        self.assertEqual(o2.get_property("desc"), "from inst")
        self.assertEqual(o2f.get_property("desc"), "from inst")

        self.assertEqual(d.get_property("name"), "dpa1")
        self.assertEqual(df.get_property("name"), "dpa2")
        self.assertEqual(o1.get_property("name"), "top default")
        self.assertEqual(o1f.get_property("name"), "top default")
        self.assertEqual(o2.get_property("name"), "top default")
        self.assertEqual(o2f.get_property("name"), "top default")


    def test_param_dpa_scopes2(self):
        root = self.compile(
            ["rdl_src/nested_params_dpa.rdl"]
        )

        value_map = {
            "top": (1000, 2000, 3000),
            "top.rf1": (100, 200, 300),
            "top.rf1.r1": (10, 20, 30),
            "top.rf1.r1.f1": (1, 2, 3),
            "top.rf1.r1.f2": (10, 4, 5),
            "top.rf1.r1.f3": (1, 2, 3),
            "top.rf1.r2": (100, 40, 50),
            "top.rf1.r2.f1": (1, 2, 3),
            "top.rf1.r2.f2": (10, 200, 5),
            "top.rf1.r2.f3": (1, 2, 3),
            "top.rf1.r3": (10, 20, 30),
            "top.rf1.r3.f1": (1, 2, 3),
            "top.rf1.r3.f2": (10, 4, 5),
            "top.rf1.r3.f3": (1, 2, 3),
            "top.rf2": (1000, 400, 500),
            "top.rf2.r1": (10, 20, 30),
            "top.rf2.r1.f1": (1, 2, 3),
            "top.rf2.r1.f2": (10, 4, 5),
            "top.rf2.r1.f3": (1, 2, 3),
            "top.rf2.r2": (100, 2000, 50),
            "top.rf2.r2.f1": (1, 2, 3),
            "top.rf2.r2.f2": (10, 400, 3000),
            "top.rf2.r2.f3": (1, 2, 3),
            "top.rf2.r3": (10, 20, 30),
            "top.rf2.r3.f1": (1, 2, 3),
            "top.rf2.r3.f2": (10, 4, 5),
            "top.rf2.r3.f3": (1, 2, 3),
            "top.rf3": (100, 200, 300),
            "top.rf3.r1": (10, 20, 30),
            "top.rf3.r1.f1": (1, 2, 3),
            "top.rf3.r1.f2": (10, 4, 5),
            "top.rf3.r1.f3": (1, 2, 3),
            "top.rf3.r2": (100, 40, 50),
            "top.rf3.r2.f1": (1, 2, 3),
            "top.rf3.r2.f2": (10, 200, 5),
            "top.rf3.r2.f3": (1, 2, 3),
            "top.rf3.r3": (10, 20, 30),
            "top.rf3.r3.f1": (1, 2, 3),
            "top.rf3.r3.f2": (10, 4, 5),
            "top.rf3.r3.f3": (1, 2, 3),
        }

        for node in root.descendants():
            udp_values = value_map[node.get_path()]
            self.assertEqual(node.get_property("udp1"), udp_values[0])
            self.assertEqual(node.get_property("udp2"), udp_values[1])
            self.assertEqual(node.get_property("udp3"), udp_values[2])

    def test_param_expressions(self):
        root = self.compile(
            ["rdl_src/param_expressions.rdl"]
        )

        def checkme(r, X):
            self.assertEqual(r.get_property("udp1"), X * 2 + 10 - 2)
            self.assertEqual(r.get_property("udp2"), 1 << X)
            self.assertEqual(r.get_property("udp3"), 2 ** X)
            self.assertEqual(r.get_property("udp4"), int("0x" + "A" * X, 0))
            self.assertEqual(r.get_property("udp5"), 0xFFFFFFFF & ((1 << X) - 1))

        r1 = root.find_by_path("top.r1")
        checkme(r1, 8)

        r2 = root.find_by_path("top.r2")
        checkme(r2, 4)

        r3 = root.find_by_path("top.r3")
        checkme(r3, 8)

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

    def test_struct_param(self):
        root = self.compile(
            ["rdl_src/parameters.rdl"],
            "struct_param"
        )
        spr = root.find_by_path("struct_param.spr")
        self.assertEqual(spr.inst.type_name, "struct_param_reg_STRUCT_3_5d946c5b_STRUCT_4_55dee485")

    def test_ispresent(self):
        root = self.compile(['rdl_src/parameterized_ispresent.rdl'], 'top')

        reg = root.find_by_path('top.f_b_present')
        children = list(reg.children())
        self.assertEqual(len(children), 2)
        reg_x = children[0]
        self.assertEqual(reg_x.inst_name, 'reg_x')
        self.assertEqual(reg_x.get_child_by_name('f').get_property('reset'), 1)
        self.assertEqual(children[1].inst_name, 'reg_b')

        reg = root.find_by_path('top.f_a_present')
        children = list(reg.children())
        self.assertEqual(len(children), 2)
        reg_x = children[0]
        self.assertEqual(reg_x.inst_name, 'reg_x')
        self.assertEqual(reg_x.get_child_by_name('f').get_property('reset'), 3)
        self.assertEqual(children[1].inst_name, 'reg_a')

        reg = root.find_by_path('top.f_both_present')
        children = list(reg.children())
        self.assertEqual(children[0].inst_name, 'reg_x')
        self.assertEqual(children[1].inst_name, 'reg_a')
        self.assertEqual(children[2].inst_name, 'reg_b')

        reg = root.find_by_path('top.f_none_present')
        children = list(reg.children())
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].inst_name, 'reg_x')

    def test_nested_types(self):
        root = self.compile(['rdl_src/parameterized_nested_types.rdl'], 'top')

        regs = list(root.find_by_path('top.default_a.b.some_reg').unrolled())
        self.assertEqual(len(regs), 1)
        reg = regs[0]
        fields = list(reg.fields())
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].inst_name, 'nested_field')

        regs = list(root.find_by_path('top.non_default_a.b.some_reg').unrolled())
        self.assertEqual(len(regs), 2)
        reg = regs[0]
        fields = list(reg.fields())
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].inst_name, 'nested_field')
        reg = regs[1]
        fields = list(reg.fields())
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].inst_name, 'nested_field')

        regs = list(root.find_by_path('top.c.b.some_reg').unrolled())
        self.assertEqual(len(regs), 1)
        reg = regs[0]
        fields = list(reg.fields())
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0].inst_name, 'nested_field')

    def test_expr_reg(self):
        root = self.compile(['rdl_src/parameterized_expr_reg.rdl'], 'top')

        field = root.find_by_path('top.r_default.f');
        self.assertEqual(field.get_property('reset'), 0x1f);

        field = root.find_by_path('top.r_four.f');
        self.assertEqual(field.get_property('reset'), 0xf);

        field = root.find_by_path('top.r_six.f');
        self.assertEqual(field.get_property('reset'), 0x3f);

    def test_expr_regfile(self):
        root = self.compile(['rdl_src/parameterized_expr_regfile.rdl'], 'top')

        field = root.find_by_path('top.rf_default.reg_x.f');
        self.assertEqual(field.get_property('reset'), 0x1f);

        field = root.find_by_path('top.rf_four.reg_x.f');
        self.assertEqual(field.get_property('reset'), 0xf);

        field = root.find_by_path('top.rf_six.reg_x.f');
        self.assertEqual(field.get_property('reset'), 0x3f);

        # y not present.
        self.assertEqual(len(root.find_by_path('top.rf_default').registers()), 1)

        # y not present.
        self.assertEqual(len(root.find_by_path('top.rf_four').registers()), 1)

        # y present.
        self.assertEqual(len(root.find_by_path('top.rf_six').registers()), 2)

    def test_expr_nested_regfile(self):
        root = self.compile(['rdl_src/parameterized_expr_nested_regfile.rdl'], 'top')

        field = root.find_by_path('top.rf_default.rf_inner.reg_x.f');
        self.assertEqual(field.get_property('reset'), 0x3ff);  # 10 bits.

        field = root.find_by_path('top.rf_nine.rf_inner.reg_x.f');
        self.assertEqual(field.get_property('reset'), 0x1ff);  # 9 bits.

        field = root.find_by_path('top.rf_eleven.rf_inner.reg_x.f');
        self.assertEqual(field.get_property('reset'), 0x7ff);  # 11 bits.

        field = root.find_by_path('top.top_rf_default.rf_inner.reg_x.f');
        self.assertEqual(field.get_property('reset'), 0x3fff);  # 14 bits.

        field = root.find_by_path('top.top_rf_thirteen.rf_inner.reg_x.f');
        self.assertEqual(field.get_property('reset'), 0x1fff);  # 13 bits.

        field = root.find_by_path('top.top_rf_fifteen.rf_inner.reg_x.f');
        self.assertEqual(field.get_property('reset'), 0x7fff);  # 15 bits.
