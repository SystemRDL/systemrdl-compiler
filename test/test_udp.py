
from .unittest_utils import RDLSourceTestCase

class TestUDP(RDLSourceTestCase):
    
    def test_15_2_2_ex1(self):
        root = self.compile(
            ["rdl_testcases/udp_15.2.2_ex1.rdl"],
            "foo"
        )
        
        foo    = root.find_by_path("foo")
        bar    = root.find_by_path("foo.bar")
        field1 = root.find_by_path("foo.bar.field1")
        field2 = root.find_by_path("foo.bar.field2")
        
        with self.subTest("foo"):
            self.assertIs(foo.get_property("some_ref_p"), None)
            self.assertIs(foo.get_property("a_map_p"), None)
        
        with self.subTest("bar"):
            self.assertIs(bar.get_property("some_ref_p"), None)
            self.assertEqual(bar.get_property("some_num_p"), 0x20)
        
        with self.subTest("field1"):
            self.assertEqual(field1.get_property("some_ref_p"), field2)
            self.assertEqual(field1.get_property("some_bool_p"), False)
            self.assertIs(field1.get_property("some_num_p"), None)
        
        with self.subTest("field2"):
            self.assertIs(field2.get_property("some_ref_p"), None)
            self.assertEqual(field2.get_property("some_bool_p"), True)
            self.assertIs(field2.get_property("some_num_p"), 0x10)
    
    def test_15_2_2_ex2(self):
        root = self.compile(
            ["rdl_testcases/udp_15.2.2_ex2.rdl"],
            "top"
        )
        
        f = root.find_by_path("top.regA.f")
        self.assertEqual(f.get_property("my_enc_prop").value, 0)
        self.assertEqual(f.get_property("my_enc_prop").name, "alpha")
