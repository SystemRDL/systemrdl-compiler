#!/usr/bin/env python3
import unittest

import os

from rdl_unittest_base import RDLSourceTestCase

#===============================================================================
# Validate inferred field bit placement/packing
#===============================================================================
class TestFieldPlacement(RDLSourceTestCase):
    
    def test_example_10_7_2_lsb(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "example_10_7_2_lsb"
        )
        
        with self.subTest():
            field = top.find_by_path("regA.A")
            self.assertEqual(field.inst.low, 0)
            self.assertEqual(field.inst.high, 0)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("regA.B")
            self.assertEqual(field.inst.low, 1)
            self.assertEqual(field.inst.high, 3)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("regA.C")
            self.assertEqual(field.inst.low, 8)
            self.assertEqual(field.inst.high, 15)
            self.assertEqual(field.inst.width, 8)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("regA.D")
            self.assertEqual(field.inst.low, 16)
            self.assertEqual(field.inst.high, 20)
            self.assertEqual(field.inst.width, 5)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
    
    
    def test_example_10_7_2_msb(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "example_10_7_2_msb"
        )
        
        with self.subTest():
            field = top.find_by_path("regA.A")
            self.assertEqual(field.inst.low, 31)
            self.assertEqual(field.inst.high, 31)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("regA.B")
            self.assertEqual(field.inst.low, 28)
            self.assertEqual(field.inst.high, 30)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("regA.C")
            self.assertEqual(field.inst.low, 8)
            self.assertEqual(field.inst.high, 15)
            self.assertEqual(field.inst.width, 8)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("regA.D")
            self.assertEqual(field.inst.low, 3)
            self.assertEqual(field.inst.high, 7)
            self.assertEqual(field.inst.width, 5)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
    
    
    def test_lsb_packing_32bit(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "lsb_packing"
        )
        
        with self.subTest():
            field = top.find_by_path("reg1.x")
            self.assertEqual(field.inst.low, 0)
            self.assertEqual(field.inst.high, 0)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg1.y")
            self.assertEqual(field.inst.low, 6)
            self.assertEqual(field.inst.high, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg1.z")
            self.assertEqual(field.inst.low, 10)
            self.assertEqual(field.inst.high, 12)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("reg1.zz")
            self.assertEqual(field.inst.low, 13)
            self.assertEqual(field.inst.high, 14)
            self.assertEqual(field.inst.width, 2)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
    def test_lsb_packing_16bit(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "lsb_packing"
        )
        
        with self.subTest():
            field = top.find_by_path("reg2.x")
            self.assertEqual(field.inst.low, 0)
            self.assertEqual(field.inst.high, 0)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg2.y")
            self.assertEqual(field.inst.low, 6)
            self.assertEqual(field.inst.high, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg2.z")
            self.assertEqual(field.inst.low, 10)
            self.assertEqual(field.inst.high, 12)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("reg2.zz")
            self.assertEqual(field.inst.low, 13)
            self.assertEqual(field.inst.high, 14)
            self.assertEqual(field.inst.width, 2)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
    
    def test_msb_packing_32bit(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "msb_packing"
        )
        
        with self.subTest():
            field = top.find_by_path("reg1.x")
            self.assertEqual(field.inst.low, 31)
            self.assertEqual(field.inst.high, 31)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg1.y")
            self.assertEqual(field.inst.low, 6)
            self.assertEqual(field.inst.high, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg1.z")
            self.assertEqual(field.inst.low, 3)
            self.assertEqual(field.inst.high, 5)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("reg1.zz")
            self.assertEqual(field.inst.low, 1)
            self.assertEqual(field.inst.high, 2)
            self.assertEqual(field.inst.width, 2)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
    def test_msb_packing_16bit(self):
        top = self.compile(
            ["rdl_testcases/field_packing.rdl"],
            "msb_packing"
        )
        
        with self.subTest():
            field = top.find_by_path("reg2.x")
            self.assertEqual(field.inst.low, 15)
            self.assertEqual(field.inst.high, 15)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg2.y")
            self.assertEqual(field.inst.low, 6)
            self.assertEqual(field.inst.high, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("reg2.z")
            self.assertEqual(field.inst.low, 3)
            self.assertEqual(field.inst.high, 5)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("reg2.zz")
            self.assertEqual(field.inst.low, 1)
            self.assertEqual(field.inst.high, 2)
            self.assertEqual(field.inst.width, 2)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)

#===============================================================================
# Validate inferred address placement/packing
#===============================================================================
