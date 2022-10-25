import os
from unittest_utils import RDLSourceTestCase
from systemrdl import RDLCompiler
from systemrdl.messages import RDLCompileError
from systemrdl import component as comp
from systemrdl.udp import UDPDefinition
from systemrdl.rdltypes import NoValue

this_dir = os.path.dirname(os.path.realpath(__file__))

class TestUDP(RDLSourceTestCase):

    def test_15_2_2_ex1(self):
        root = self.compile(
            ["rdl_src/udp_15.2.2_ex1.rdl"],
            "foo"
        )

        foo    = root.find_by_path("foo")
        bar    = root.find_by_path("foo.bar")
        field1 = root.find_by_path("foo.bar.field1")
        field2 = root.find_by_path("foo.bar.field2")

        with self.subTest("foo"):
            self.assertIs(foo.get_property('some_ref_p'), None)
            self.assertIs(foo.get_property('a_map_p'), NoValue)

        with self.subTest("bar"):
            self.assertIs(bar.get_property('some_ref_p'), None)
            self.assertEqual(bar.get_property('some_num_p'), 0x20)

        with self.subTest("field1"):
            self.assertEqual(field1.get_property('some_ref_p'), field2)
            self.assertIs(field1.get_property('some_bool_p'), False)
            self.assertIs(field1.get_property('some_num_p'), None)

        with self.subTest("field2"):
            self.assertIs(field2.get_property('some_ref_p'), None)
            self.assertIs(field2.get_property('some_bool_p'), True)
            self.assertIs(field2.get_property('some_num_p'), 0x10)

    def test_15_2_2_ex2(self):
        root = self.compile(
            ["rdl_src/udp_15.2.2_ex2.rdl"],
            "top"
        )

        f = root.find_by_path("top.regA.f")
        self.assertEqual(f.get_property('my_enc_prop').value, 0)
        self.assertEqual(f.get_property('my_enc_prop').name, "alpha")

    def test_builtin_udp(self):
        class MyUDP(UDPDefinition):
            name = "int_udp"
            valid_type = int
            default_assignment = 123

        rdlc = RDLCompiler()
        rdlc.register_udp(MyUDP, soft=False)
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_builtin.rdl"))
        root = rdlc.elaborate("top")

        top    = root.find_by_path("top")
        reg1   = root.find_by_path("top.reg1")
        field1 = root.find_by_path("top.reg1.field1")

        self.assertIs(top.get_property('int_udp'), 43)
        self.assertIs(reg1.get_property('int_udp'), 42)
        self.assertIs(field1.get_property('int_udp'), 123)

    def test_builtin_udp_validate(self):
        class MyUDP(UDPDefinition):
            name = "int_udp"
            valid_type = int
            default_assignment = 123

            def validate(self, node, value) -> None:
                self.msg.error("my error msg")

        rdlc = RDLCompiler()
        rdlc.register_udp(MyUDP, soft=False)
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_builtin.rdl"))
        with self.assertRaises(RDLCompileError):
            rdlc.elaborate("top")

    def test_soft_udp_undeclared(self):
        class MyUDP(UDPDefinition):
            name = "int_udp"
            valid_type = int
            default_assignment = 123
        rdlc = RDLCompiler()
        rdlc.register_udp(MyUDP)
        with self.assertRaises(RDLCompileError):
            rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_builtin.rdl"))

    def test_soft_udp_query(self):
        class MyUDP(UDPDefinition):
            name = "int_udp"
            valid_type = int
            default_assignment = 123
        rdlc = RDLCompiler()
        rdlc.register_udp(MyUDP)
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_15.2.2_ex2.rdl"))
        root = rdlc.elaborate("top")

        f = root.find_by_path("top.regA.f")
        self.assertIsNone(f.get_property('int_udp'))

    def test_soft_udp_success(self):
        class MyUDP(UDPDefinition):
            name = "a_map_p"
            valid_type = str
            valid_components = {comp.Addrmap, comp.Regfile}
        rdlc = RDLCompiler()
        rdlc.register_udp(MyUDP)
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_15.2.2_ex1.rdl"))
        rdlc.elaborate("foo")

    def test_soft_udp_conflict(self):
        class MyUDP(UDPDefinition):
            name = "a_map_p"
            valid_type = int # src defines as a string
            valid_components = {comp.Addrmap, comp.Regfile}
        rdlc = RDLCompiler()
        rdlc.register_udp(MyUDP)
        with self.assertRaises(RDLCompileError):
            rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_15.2.2_ex1.rdl"))

    def test_soft_udp_dupe(self):
        class MyUDP(UDPDefinition):
            name = "bool_udp"
            valid_type = bool
            valid_components = {comp.Field}
        rdlc = RDLCompiler()
        rdlc.register_udp(MyUDP)
        with self.assertRaises(RDLCompileError):
            rdlc.compile_file(os.path.join(this_dir, "rdl_err_src/err_duplicate_udp.rdl"))

    def test_list_udps(self):

        class MyUDP1(UDPDefinition):
            name = "int_udp"
            valid_type = int
            default_assignment = 123

        class MyUDP2(UDPDefinition):
            name = "int_udp_soft"
            valid_type = int
            default_assignment = 123

        rdlc = RDLCompiler()
        rdlc.register_udp(MyUDP1, soft=False)
        rdlc.register_udp(MyUDP2, soft=True)
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_15.2.2_ex1.rdl"))
        rdlc.elaborate("foo")

        self.assertEqual(
            sorted(rdlc.list_udps()),
            [
                'a_map_p',
                'int_udp',
                'some_bool_p',
                'some_num_p',
                'some_ref_p',
            ]
        )
