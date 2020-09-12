import os
from unittest_utils import RDLSourceTestCase

class TestPreprocessor(RDLSourceTestCase):

    def test_preprocessor(self):
        root = self.compile(
            ["rdl_testcases/preprocessor.rdl"],
            "top"
        )

        reg1 = root.find_by_path("top.reg1")
        reg1_data0 = root.find_by_path("top.reg1.data0")
        reg1_data2 = root.find_by_path("top.reg1.data2")
        reg1_data4 = root.find_by_path("top.reg1.data4")

        self.assertEqual(len(list(reg1.fields())), 3)

        with self.subTest("reg1_data0"):
            self.assertEqual(reg1_data0.msb, 1)
            self.assertEqual(reg1_data0.lsb, 0)

        with self.subTest("reg1_data2"):
            self.assertEqual(reg1_data2.msb, 3)
            self.assertEqual(reg1_data2.lsb, 2)

        with self.subTest("reg1_data4"):
            self.assertEqual(reg1_data4.msb, 5)
            self.assertEqual(reg1_data4.lsb, 4)

    def test_src_ref_translation(self):
        root = self.compile(
            ["rdl_testcases/preprocessor.rdl"],
            "top"
        )

        with self.subTest("top def"):
            src_ref = root.find_by_path("top").inst.def_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor.rdl")
            self.assertEqual(src_ref.line, 25)
            self.assertEqual(src_ref.line_selection, (18, 18))

        with self.subTest("reg1 def"):
            src_ref = root.find_by_path("top.reg1").inst.def_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor.rdl")
            self.assertEqual(src_ref.line, 11)
            self.assertEqual(src_ref.line_selection, (10, 10))

        with self.subTest("reg1 inst"):
            src_ref = root.find_by_path("top.reg1").inst.inst_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor.rdl")
            self.assertEqual(src_ref.line, 26)
            self.assertEqual(src_ref.line_selection, (10, 13))

        with self.subTest("data0 def"):
            src_ref = root.find_by_path("top.reg1.data0").inst.def_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor_incl.rdl")
            self.assertEqual(src_ref.line, 4)
            self.assertEqual(src_ref.line_selection, (14, 15))

        with self.subTest("data0 inst"):
            src_ref = root.find_by_path("top.reg1.data0").inst.inst_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor.rdl")
            self.assertEqual(src_ref.line, 13)
            self.assertEqual(src_ref.line_selection, (12, 22))

        with self.subTest("reg2 def"):
            src_ref = root.find_by_path("top.reg2").inst.def_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor_incl2.rdl")
            self.assertEqual(src_ref.line, 2)
            self.assertEqual(src_ref.line_selection, (11, 11))

        with self.subTest("reg2 inst"):
            src_ref = root.find_by_path("top.reg2").inst.inst_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor.rdl")
            self.assertEqual(src_ref.line, 27)
            self.assertEqual(src_ref.line_selection, (11, 14))

        with self.subTest("reg3 inst"):
            src_ref = root.find_by_path("top.reg3").inst.inst_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor.rdl")
            self.assertEqual(src_ref.line, 28)
            self.assertEqual(src_ref.line_selection, (4, 22))

        with self.subTest("x def"):
            src_ref = root.find_by_path("top.reg2.x").inst.def_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor_incl.rdl")
            self.assertEqual(src_ref.line, 4)
            self.assertEqual(src_ref.line_selection, (14, 15))

        with self.subTest("x inst"):
            src_ref = root.find_by_path("top.reg2.x").inst.inst_src_ref

            self.assertEqual(os.path.basename(src_ref.path), "preprocessor_incl2.rdl")
            self.assertEqual(src_ref.line, 3)
            self.assertEqual(src_ref.line_selection, (12, 12))

        with self.subTest("conditional1"):
            self.assertIsNone(root.find_by_path("top.foo1"))
            self.assertIsNone(root.find_by_path("top.bar1"))
            self.assertIsNotNone(root.find_by_path("top.else1"))
            self.assertIsNone(root.find_by_path("top.macro_foo1"))
            self.assertIsNone(root.find_by_path("top.macro_bar1"))
            self.assertIsNotNone(root.find_by_path("top.macro_else1"))

        with self.subTest("conditional2"):
            self.assertIsNotNone(root.find_by_path("top.foo2"))
            self.assertIsNone(root.find_by_path("top.bar2"))
            self.assertIsNone(root.find_by_path("top.else2"))

        with self.subTest("conditional3"):
            self.assertIsNotNone(root.find_by_path("top.foo3"))
            self.assertIsNone(root.find_by_path("top.bar3"))
            self.assertIsNone(root.find_by_path("top.else3"))
            self.assertIsNone(root.find_by_path("top.xxx3"))
            self.assertIsNone(root.find_by_path("top.yyy3"))
            self.assertIsNone(root.find_by_path("top.xyelse3"))

        with self.subTest("conditional4"):
            self.assertIsNone(root.find_by_path("top.foo4"))
            self.assertIsNotNone(root.find_by_path("top.bar4"))
            self.assertIsNone(root.find_by_path("top.else4"))
            self.assertIsNone(root.find_by_path("top.xxx4"))
            self.assertIsNotNone(root.find_by_path("top.yyy4"))
            self.assertIsNone(root.find_by_path("top.xyelse4"))

        with self.subTest("Misc maros"):
            self.assertIsNotNone(root.find_by_path("top.abcd1234"))

            desc = root.find_by_path("top").get_property("desc")
            self.assertEqual(desc, "left side: \"right side\"")

            name = root.find_by_path("top").get_property("name")
            self.assertEqual(name, "b + 1 + 42 + a")
