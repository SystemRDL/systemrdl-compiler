
from .unittest_utils import RDLSourceTestCase

class TestEnums(RDLSourceTestCase):
    
    def test_enums(self):
        top = self.compile(
            ["rdl_testcases/enums.rdl"],
            "enum_test1"
        )
        
        f_default = top.find_by_path("enum_test1.reg1.f_default")
        f_zero = top.find_by_path("enum_test1.reg1.f_zero")
        f_one = top.find_by_path("enum_test1.reg1.f_one")
        f_three = top.find_by_path("enum_test1.reg1.f_three")
        f_four = top.find_by_path("enum_test1.reg1.f_four")
        f_five = top.find_by_path("enum_test1.reg1.f_five")
        self.assertEqual(f_default.get_property("reset"), 5)
        self.assertEqual(f_zero.get_property("reset"), 1)
        self.assertEqual(f_one.get_property("reset"), 2)
        self.assertEqual(f_three.get_property("reset"), 4)
        self.assertEqual(f_four.get_property("reset"), 5)
        self.assertEqual(f_five.get_property("reset"), 6)
        
        self.assertEqual(f_default.get_property("encode").five.rdl_name, "five's name")
        self.assertEqual(f_default.get_property("encode").five.rdl_desc, "this is five")
        