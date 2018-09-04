
from .unittest_utils import RDLSourceTestCase

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
            self.assertEqual(reg1_data0.inst.msb, 1)
            self.assertEqual(reg1_data0.inst.lsb, 0)
        
        with self.subTest("reg1_data2"):
            self.assertEqual(reg1_data2.inst.msb, 3)
            self.assertEqual(reg1_data2.inst.lsb, 2)
        
        with self.subTest("reg1_data4"):
            self.assertEqual(reg1_data4.inst.msb, 5)
            self.assertEqual(reg1_data4.inst.lsb, 4)
