import unittest
import os

from systemrdl import RDLCompiler
from systemrdl import rdltypes

from unittest_utils import TestPrinter

this_dir = os.path.dirname(os.path.realpath(__file__))

class TestMultipleElab(unittest.TestCase):
    def test_multiple_different_elab(self):
        rdlc = RDLCompiler(message_printer=TestPrinter())
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/all_params.rdl"))

        myAmap_root = rdlc.elaborate("myAmap")
        param_types_root = rdlc.elaborate("param_types")
        nested_root = rdlc.elaborate("nested_params")
        param_scope_root = rdlc.elaborate("param_scope")

        # Test that each root only contains one top, and that it is the expected one
        self.assertListEqual(myAmap_root.children(), [myAmap_root.top])
        self.assertEqual(myAmap_root.top, myAmap_root.get_child_by_name("myAmap"))

        self.assertListEqual(param_types_root.children(), [param_types_root.top])
        self.assertEqual(param_types_root.top, param_types_root.get_child_by_name("param_types"))

        self.assertListEqual(nested_root.children(), [nested_root.top])
        self.assertEqual(nested_root.top, nested_root.get_child_by_name("nested_params"))

        self.assertListEqual(param_scope_root.children(), [param_scope_root.top])
        self.assertEqual(param_scope_root.top, param_scope_root.get_child_by_name("param_scope"))

    def test_repeat_elab(self):
        rdlc = RDLCompiler(message_printer=TestPrinter())
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/nested_params.rdl"))

        inst1_root = rdlc.elaborate("nested_params", "inst1")
        inst2_root = rdlc.elaborate("nested_params", "inst2")

        self.assertListEqual(inst1_root.children(), [inst1_root.top])
        self.assertEqual(inst1_root.top, inst1_root.get_child_by_name("inst1"))

        self.assertListEqual(inst2_root.children(), [inst2_root.top])
        self.assertEqual(inst2_root.top, inst2_root.get_child_by_name("inst2"))

    def test_multi_elab_params(self):
        rdlc = RDLCompiler(message_printer=TestPrinter())
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/elab_params.rdl"))

        print("1")
        default_root = rdlc.elaborate("elab_params")
        print("2")
        W10_root = rdlc.elaborate("elab_params", parameters={
            "STR": "ovr1",
            "INT": 10,
            "INTARR": [20, 30],
            "UNUSED_STR": "ovr2",
        })

        self.assertEqual(default_root.top.find_by_path("r1.f").width, 1)
        self.assertEqual(W10_root.top.find_by_path("r1.f").width, 10)

        # Test old parameter API - Was not explicitly made a private API!
        expected = {
            "STR": "default",
            "INT": 1,
            "INTARR": [2, 3],
            "ONWR": rdltypes.OnWriteType.woset,
            "BOOL": True,
            "UNUSED_STR": "asdf",
        }
        for param in default_root.top.inst.parameters:
            self.assertEqual(expected[param.name], param.get_value())

        expected = {
            "STR": "ovr1",
            "INT": 10,
            "INTARR": [20, 30],
            "ONWR": rdltypes.OnWriteType.woset,
            "BOOL": True,
            "UNUSED_STR": "ovr2",
        }
        for param in W10_root.top.inst.parameters:
            self.assertEqual(expected[param.name], param.get_value())


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
