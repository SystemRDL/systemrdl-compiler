#!/usr/bin/env python3
import unittest

import sys
import os
this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))

from src.rdl_compiler import RDLCompiler


class TestFieldPlacement(unittest.TestCase):
    def compile(self, files, top_name):
        rdlc = RDLCompiler()
        for file in files:
            rdlc.compile_file(os.path.join(this_dir, file))
        return(rdlc.elaborate(top_name))
        
    def test_lsb_packing_32bit(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "lsb_packing"
        )
        
        with self.subTest():
            field = top.find_by_path("reg1.x")
            self.assertEqual(field.inst.lsb, 0)
            self.assertEqual(field.inst.msb, 0)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg1.y")
            self.assertEqual(field.inst.lsb, 6)
            self.assertEqual(field.inst.msb, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg1.z")
            self.assertEqual(field.inst.lsb, 10)
            self.assertEqual(field.inst.msb, 12)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("reg1.zz")
            self.assertEqual(field.inst.lsb, 13)
            self.assertEqual(field.inst.msb, 14)
            self.assertEqual(field.inst.width, 2)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
    def test_lsb_packing_16bit(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "lsb_packing"
        )
        
        with self.subTest():
            field = top.find_by_path("reg2.x")
            self.assertEqual(field.inst.lsb, 0)
            self.assertEqual(field.inst.msb, 0)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg2.y")
            self.assertEqual(field.inst.lsb, 6)
            self.assertEqual(field.inst.msb, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg2.z")
            self.assertEqual(field.inst.lsb, 10)
            self.assertEqual(field.inst.msb, 12)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("reg2.zz")
            self.assertEqual(field.inst.lsb, 13)
            self.assertEqual(field.inst.msb, 14)
            self.assertEqual(field.inst.width, 2)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
    
    def test_msb_packing_32bit(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "msb_packing"
        )
        
        with self.subTest():
            field = top.find_by_path("reg1.x")
            self.assertEqual(field.inst.lsb, 31)
            self.assertEqual(field.inst.msb, 31)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg1.y")
            self.assertEqual(field.inst.lsb, 6)
            self.assertEqual(field.inst.msb, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg1.z")
            self.assertEqual(field.inst.lsb, 3)
            self.assertEqual(field.inst.msb, 5)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("reg1.zz")
            self.assertEqual(field.inst.lsb, 1)
            self.assertEqual(field.inst.msb, 2)
            self.assertEqual(field.inst.width, 2)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
    def test_msb_packing_16bit(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "msb_packing"
        )
        
        with self.subTest():
            field = top.find_by_path("reg2.x")
            self.assertEqual(field.inst.lsb, 15)
            self.assertEqual(field.inst.msb, 15)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg2.y")
            self.assertEqual(field.inst.lsb, 6)
            self.assertEqual(field.inst.msb, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg2.z")
            self.assertEqual(field.inst.lsb, 3)
            self.assertEqual(field.inst.msb, 5)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("reg2.zz")
            self.assertEqual(field.inst.lsb, 1)
            self.assertEqual(field.inst.msb, 2)
            self.assertEqual(field.inst.width, 2)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
