import unittest
import os

from systemrdl import RDLCompiler

from unittest_utils import TestPrinter

this_dir = os.path.dirname(os.path.realpath(__file__))

class TestMultipleElab(unittest.TestCase):
    def test_multiple_different_elab(self):
        rdlc = RDLCompiler(message_printer=TestPrinter())
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/parameters.rdl"))

        myAmap_root = rdlc.elaborate("myAmap")
        amap2_root = rdlc.elaborate("amap2")
        nested_root = rdlc.elaborate("nested")
        param_scope_root = rdlc.elaborate("param_scope")

        # Test that each root only contains one top, and that it is the expected one
        self.assertListEqual(myAmap_root.children(), [myAmap_root.top])
        self.assertEqual(myAmap_root.top, myAmap_root.get_child_by_name("myAmap"))

        self.assertListEqual(amap2_root.children(), [amap2_root.top])
        self.assertEqual(amap2_root.top, amap2_root.get_child_by_name("amap2"))

        self.assertListEqual(nested_root.children(), [nested_root.top])
        self.assertEqual(nested_root.top, nested_root.get_child_by_name("nested"))

        self.assertListEqual(param_scope_root.children(), [param_scope_root.top])
        self.assertEqual(param_scope_root.top, param_scope_root.get_child_by_name("param_scope"))

    def test_repeat_elab(self):
        rdlc = RDLCompiler(message_printer=TestPrinter())
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/parameters.rdl"))

        inst1_root = rdlc.elaborate("nested", "inst1")
        inst2_root = rdlc.elaborate("nested", "inst2")

        self.assertListEqual(inst1_root.children(), [inst1_root.top])
        self.assertEqual(inst1_root.top, inst1_root.get_child_by_name("inst1"))

        self.assertListEqual(inst2_root.children(), [inst2_root.top])
        self.assertEqual(inst2_root.top, inst2_root.get_child_by_name("inst2"))

    def test_multi_elab_params(self):
        rdlc = RDLCompiler(message_printer=TestPrinter())
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/parameters.rdl"))

        default_root = rdlc.elaborate("elab_params")
        W10_root = rdlc.elaborate("elab_params", parameters={
            "INT": 10,
        })

        self.assertEqual(default_root.top.find_by_path("r1.f").width, 1)
        self.assertEqual(W10_root.top.find_by_path("r1.f").width, 10)

    def test_multi_elab_common_dpa(self):
        rdlc = RDLCompiler(message_printer=TestPrinter())
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/shared_dpa.rdl"))

        top_root = rdlc.elaborate("top")
        top_a_root = rdlc.elaborate("top_a")
        top_b_root = rdlc.elaborate("top_b")

        self.assertEqual(top_root.top.find_by_path("myreg").get_property("desc"), "reg default")
        self.assertEqual(top_root.top.find_by_path("myreg.f").get_property("desc"), "field default")
        self.assertEqual(top_a_root.top.find_by_path("myreg").get_property("desc"), "reg a")
        self.assertEqual(top_a_root.top.find_by_path("myreg.f").get_property("desc"), "field a")
        self.assertEqual(top_b_root.top.find_by_path("myreg").get_property("desc"), "reg b")
        self.assertEqual(top_b_root.top.find_by_path("myreg.f").get_property("desc"), "field b")


    def test_illegal_multi_elab(self):
        rdlc = RDLCompiler(
            message_printer=TestPrinter(),
            single_elaborate_optimization=True,
        )
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/parameters.rdl"))

        rdlc.elaborate("nested", "inst1")
        with self.assertRaises(RuntimeError):
            # Calling elaborate a second time is not allowed if single_elaborate_optimization=True
            rdlc.elaborate("nested", "inst2")
