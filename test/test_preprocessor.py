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

        with self.subTest("reg1 def"):
            src_ref = root.find_by_path("top.reg1").inst.def_src_ref
            src_ref.derive_coordinates()
            
            self.assertEqual(os.path.basename(src_ref.filename), "preprocessor.rdl")
            self.assertEqual(src_ref.start_line, 4)
            self.assertEqual(src_ref.start_col, 10)
            self.assertEqual(src_ref.end_line, 8)
            self.assertEqual(src_ref.end_col, 0)

        with self.subTest("reg1 inst"):
            src_ref = root.find_by_path("top.reg1").inst.inst_src_ref
            src_ref.derive_coordinates()
            
            self.assertEqual(os.path.basename(src_ref.filename), "preprocessor.rdl")
            self.assertEqual(src_ref.start_line, 18)
            self.assertEqual(src_ref.start_col, 10)
            self.assertEqual(src_ref.end_line, 18)
            self.assertEqual(src_ref.end_col, 13)

        with self.subTest("data0 def"):
            src_ref = root.find_by_path("top.reg1.data0").inst.def_src_ref
            src_ref.derive_coordinates()
            
            self.assertEqual(os.path.basename(src_ref.filename), "preprocessor_incl.rdl")
            self.assertEqual(src_ref.start_line, 4)
            self.assertEqual(src_ref.start_col, 14)
            self.assertEqual(src_ref.end_line, 4)
            self.assertEqual(src_ref.end_col, 15)
        
        with self.subTest("data0 inst"):
            src_ref = root.find_by_path("top.reg1.data0").inst.inst_src_ref
            src_ref.derive_coordinates()
            
            self.assertEqual(os.path.basename(src_ref.filename), "preprocessor.rdl")
            self.assertEqual(src_ref.start_line, 6)
            self.assertEqual(src_ref.start_col, 12)
            self.assertEqual(src_ref.end_line, 6)
            self.assertEqual(src_ref.end_col, 22)
        
        with self.subTest("reg2 def"):
            src_ref = root.find_by_path("top.reg2").inst.def_src_ref
            src_ref.derive_coordinates()
            
            self.assertEqual(os.path.basename(src_ref.filename), "preprocessor_incl2.rdl")
            self.assertEqual(src_ref.start_line, 2)
            self.assertEqual(src_ref.start_col, 11)
            self.assertEqual(src_ref.end_line, 4)
            self.assertEqual(src_ref.end_col, 0)

        with self.subTest("reg2 inst"):
            src_ref = root.find_by_path("top.reg2").inst.inst_src_ref
            src_ref.derive_coordinates()
            
            self.assertEqual(os.path.basename(src_ref.filename), "preprocessor.rdl")
            self.assertEqual(src_ref.start_line, 19)
            self.assertEqual(src_ref.start_col, 11)
            self.assertEqual(src_ref.end_line, 19)
            self.assertEqual(src_ref.end_col, 14)
        
        with self.subTest("x def"):
            src_ref = root.find_by_path("top.reg2.x").inst.def_src_ref
            src_ref.derive_coordinates()

            self.assertEqual(os.path.basename(src_ref.filename), "preprocessor_incl.rdl")
            self.assertEqual(src_ref.start_line, 4)
            self.assertEqual(src_ref.start_col, 14)
            self.assertEqual(src_ref.end_line, 4)
            self.assertEqual(src_ref.end_col, 15)

        with self.subTest("x inst"):
            src_ref = root.find_by_path("top.reg2.x").inst.inst_src_ref
            src_ref.derive_coordinates()
            
            self.assertEqual(os.path.basename(src_ref.filename), "preprocessor_incl2.rdl")
            self.assertEqual(src_ref.start_line, 3)
            self.assertEqual(src_ref.start_col, 12)
            self.assertEqual(src_ref.end_line, 3)
            self.assertEqual(src_ref.end_col, 12)
