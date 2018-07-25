
from .unittest_utils import RDLSourceTestCase
import systemrdl.rdltypes as rdlt

class TestStructs(RDLSourceTestCase):
    
    def test_structs(self):
        root = self.compile(
            ["rdl_testcases/structs.rdl"],
            "struct_test"
        )
        
        with self.subTest("6.3.2.2.1"):
            amap = root.find_by_path("struct_test")
            p01 = amap.get_property("p01")
            p02 = amap.get_property("p02")
            p03 = amap.get_property("p03")
            
            self.assertEqual(type(p01).__name__, "base_struct")
            self.assertEqual(set(p01._values.keys()), set(["foo"]))
            self.assertEqual(p01.foo, 1)
            
            self.assertEqual(type(p02).__name__, "derived_struct")
            self.assertEqual(set(p02._values.keys()), set(["foo", "bar"]))
            self.assertEqual(p02.foo, 0)
            self.assertEqual(p02.bar, 1234)
            
            self.assertEqual(type(p03).__name__, "final_struct")
            self.assertEqual(set(p03._values.keys()), set(["foo", "bar", "baz"]))
            self.assertEqual(p03.foo, 1)
            self.assertEqual(p03.bar, 5678)
            self.assertEqual(p03.baz, "abcde")
        
        with self.subTest("ex1"):
            f1p1 = root.find_by_path("struct_test.ex1_reg.ex1_field1").get_property("p1")
            self.assertEqual(type(f1p1).__name__, "struct1")
            self.assertEqual(set(f1p1._values.keys()), set(["abool", "astring"]))
            self.assertEqual(f1p1.abool, True)
            self.assertEqual(f1p1.astring, "hello")
            
            f2p1 = root.find_by_path("struct_test.ex1_reg.ex1_field2").get_property("p1")
            self.assertEqual(type(f2p1).__name__, "struct1")
            self.assertEqual(set(f2p1._values.keys()), set(["abool", "astring"]))
            self.assertEqual(f2p1.abool, False)
            self.assertEqual(f2p1.astring, "bye")
        
        with self.subTest("ex2"):
            p2 = root.find_by_path("struct_test.ex2_reg.f1").get_property("p2")
            self.assertEqual(type(p2).__name__, "struct_composed")
            self.assertEqual(set(p2._values.keys()), set(["str", "s"]))
            self.assertEqual(p2.str, "world")
            
            self.assertEqual(type(p2.s).__name__, "struct1")
            self.assertEqual(set(p2.s._values.keys()), set(["abool", "astring"]))
            self.assertEqual(p2.s.abool, True)
            self.assertEqual(p2.s.astring, "blah")
        
        with self.subTest("ex3"):
            f1p3 = root.find_by_path("struct_test.ex3_reg.ex3_field1").get_property("p3")
            self.assertEqual(type(f1p3).__name__, "substruct")
            self.assertEqual(set(f1p3._values.keys()), set(["abool", "astring"]))
            self.assertEqual(f1p3.abool, False)
            self.assertEqual(f1p3.astring, "foo")
            
            f2p3 = root.find_by_path("struct_test.ex3_reg.ex3_field2").get_property("p3")
            self.assertEqual(type(f2p3).__name__, "substruct")
            self.assertEqual(set(f2p3._values.keys()), set(["abool", "astring"]))
            self.assertEqual(f2p3.abool, True)
            self.assertEqual(f2p3.astring, "bar")
    
    
    def test_struct_compositions(self):
        root = self.compile(
            ["rdl_testcases/struct_compositions.rdl"],
            "top"
        )
        
        my_reg = root.find_by_path("top.my_reg")
        x = root.find_by_path("top.my_reg.x")
        
        self.assertEqual(my_reg.get_property("desc"), "hey")
        self.assertEqual(my_reg.get_property("name"), "foo")
        self.assertEqual(x.get_property("sw"), rdlt.AccessType.r)
        self.assertEqual(x.get_property("name"), "bar")
        self.assertEqual(my_reg.get_property("p_bool"), True)
        self.assertEqual(my_reg.get_property("p_int"), 61)
        
        p_s1 = my_reg.get_property("p_s1")
        self.assertEqual(type(p_s1).__name__, "s1_t")
        self.assertEqual(p_s1._values, {"bool":False, "str":"foo", "n_arr":[20,40,60,80]})
