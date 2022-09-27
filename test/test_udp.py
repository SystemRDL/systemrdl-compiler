import os
from unittest_utils import RDLSourceTestCase
from systemrdl import RDLCompiler
from systemrdl.messages import RDLCompileError
from systemrdl import component as comp

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
            self.assertIs(foo.get_property('a_map_p'), None)

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
        rdlc = RDLCompiler()
        rdlc.define_udp("int_udp", int, default=123)
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_builtin.rdl"))
        root = rdlc.elaborate("top")

        top    = root.find_by_path("top")
        reg1   = root.find_by_path("top.reg1")
        field1 = root.find_by_path("top.reg1.field1")

        self.assertIs(top.get_property('int_udp'), 43)
        self.assertIs(reg1.get_property('int_udp'), 42)
        self.assertIs(field1.get_property('int_udp'), 123)

    def test_builtin_udp_validate(self):
        def my_validate(msg, node, value):
            msg.error("hi")
        rdlc = RDLCompiler()
        rdlc.define_udp("int_udp", int, default=123, validate_func=my_validate)
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_builtin.rdl"))
        with self.assertRaises(RDLCompileError):
            rdlc.elaborate("top")

    def test_soft_udp_undeclared(self):
        rdlc = RDLCompiler()
        rdlc.define_udp("int_udp", int, default=123, soft=True)
        with self.assertRaises(RDLCompileError):
            rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_builtin.rdl"))

    def test_soft_udp_query(self):
        rdlc = RDLCompiler()
        rdlc.define_udp("int_udp", int, default=123, soft=True)
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_15.2.2_ex2.rdl"))
        root = rdlc.elaborate("top")

        f = root.find_by_path("top.regA.f")
        self.assertIsNone(f.get_property('int_udp'))

    def test_soft_udp_success(self):
        rdlc = RDLCompiler()
        rdlc.define_udp("a_map_p", str, {comp.Addrmap, comp.Regfile}, soft=True)
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_15.2.2_ex1.rdl"))
        rdlc.elaborate("foo")

    def test_soft_udp_conflict(self):
        rdlc = RDLCompiler()
        rdlc.define_udp("a_map_p", int, {comp.Addrmap, comp.Regfile}, soft=True)
        with self.assertRaises(RDLCompileError):
            rdlc.compile_file(os.path.join(this_dir, "rdl_src/udp_15.2.2_ex1.rdl"))

    def test_soft_udp_dupe(self):
        rdlc = RDLCompiler()
        rdlc.define_udp("bool_udp", bool, {comp.Field}, soft=True)
        with self.assertRaises(RDLCompileError):
            rdlc.compile_file(os.path.join(this_dir, "rdl_err_src/err_duplicate_udp.rdl"))

    def test_list_udps(self):
        rdlc = RDLCompiler()
        rdlc.define_udp("int_udp", int, default=123)
        rdlc.define_udp("int_udp_soft", int, default=123, soft=True)
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
