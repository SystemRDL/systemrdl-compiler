
from .unittest_utils import RDLSourceTestCase

class TestParameters(RDLSourceTestCase):
    
    def test_spec_examples(self):
        root = self.compile(
            ["rdl_testcases/parameters.rdl"],
            "myAmap"
        )
        
        reg32  = root.find_by_path("myAmap.reg32")
        reg32a = root.find_by_path("myAmap.reg32_arr")
        reg16  = root.find_by_path("myAmap.reg16")
        reg8   = root.find_by_path("myAmap.reg8")
        mem32  = root.find_by_path("myAmap.mem32")
        mem64  = root.find_by_path("myAmap.mem64")
        
        with self.subTest("reg32"):
            self.assertEqual(reg32.get_property("regwidth"), 32)
            self.assertEqual(reg32.get_property("shared"), True)
            data = reg32.get_child_by_name("data")
            self.assertEqual(data.inst.width, 31)
            self.assertEqual(data.inst.high, 30)
            self.assertEqual(data.inst.low, 0)
        
        with self.subTest("reg32a"):
            self.assertEqual(reg32a.get_property("regwidth"), 32)
            self.assertEqual(reg32a.get_property("shared"), True)
            data = reg32a.get_child_by_name("data")
            self.assertEqual(data.inst.width, 31)
            self.assertEqual(data.inst.high, 30)
            self.assertEqual(data.inst.low, 0)
        
        with self.subTest("reg16"):
            self.assertEqual(reg16.get_property("regwidth"), 16)
            self.assertEqual(reg16.get_property("shared"), True)
            data = reg16.get_child_by_name("data")
            self.assertEqual(data.inst.width, 15)
            self.assertEqual(data.inst.high, 14)
            self.assertEqual(data.inst.low, 0)
        
        with self.subTest("reg8"):
            self.assertEqual(reg8.get_property("regwidth"), 8)
            self.assertEqual(reg8.get_property("shared"), False)
            data = reg8.get_child_by_name("data")
            self.assertEqual(data.inst.width, 7)
            self.assertEqual(data.inst.high, 6)
            self.assertEqual(data.inst.low, 0)
        
        with self.subTest("mem32"):
            self.assertEqual(mem32.get_property("mementries"), 4096)
            self.assertEqual(mem32.get_property("memwidth"), 32)
        
        with self.subTest("mem64"):
            self.assertEqual(mem64.get_property("mementries"), 4096)
            self.assertEqual(mem64.get_property("memwidth"), 64)
    
    def test_more(self):
        root = self.compile(
            ["rdl_testcases/parameters.rdl"],
            "amap2"
        )
        
        reg1 = root.find_by_path("amap2.reg1")
        reg2 = root.find_by_path("amap2.reg2")
        reg3 = root.find_by_path("amap2.reg3")
        
        with self.subTest("reg1"):
            self.assertEqual(reg1.inst.type_name, "param_reg")
            self.assertEqual(reg1.get_property("name"), "myname")
            self.assertEqual(reg1.get_property("shared"), False)
            data = reg1.get_child_by_name("data")
            self.assertEqual(data.get_property("hdl_path_slice"), ["dat"])
        
        with self.subTest("reg2"):
            self.assertEqual(reg2.inst.type_name, "param_reg")
            self.assertEqual(reg2.get_property("name"), "myname")
            self.assertEqual(reg2.get_property("shared"), False)
            data = reg2.get_child_by_name("data")
            self.assertEqual(data.get_property("hdl_path_slice"), ["dat"])
        
        with self.subTest("reg3"):
            self.assertEqual(reg3.inst.type_name, "param_reg_NAME_a36638b4_SHARED_t_FIELD_SLICES_184d423e")
            self.assertEqual(reg3.get_property("name"), "othername")
            self.assertEqual(reg3.get_property("shared"), True)
            data = reg3.get_child_by_name("data")
            self.assertEqual(data.get_property("hdl_path_slice"), ["foo"])
