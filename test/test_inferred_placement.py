
from .unittest_utils import RDLSourceTestCase

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
            field = top.find_by_path("example_10_7_2_lsb.regA.A")
            self.assertEqual(field.inst.low, 0)
            self.assertEqual(field.inst.high, 0)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("example_10_7_2_lsb.regA.B")
            self.assertEqual(field.inst.low, 1)
            self.assertEqual(field.inst.high, 3)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("example_10_7_2_lsb.regA.C")
            self.assertEqual(field.inst.low, 8)
            self.assertEqual(field.inst.high, 15)
            self.assertEqual(field.inst.width, 8)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("example_10_7_2_lsb.regA.D")
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
            field = top.find_by_path("example_10_7_2_msb.regA.A")
            self.assertEqual(field.inst.low, 31)
            self.assertEqual(field.inst.high, 31)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("example_10_7_2_msb.regA.B")
            self.assertEqual(field.inst.low, 28)
            self.assertEqual(field.inst.high, 30)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("example_10_7_2_msb.regA.C")
            self.assertEqual(field.inst.low, 8)
            self.assertEqual(field.inst.high, 15)
            self.assertEqual(field.inst.width, 8)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("example_10_7_2_msb.regA.D")
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
            field = top.find_by_path("lsb_packing.reg1.x")
            self.assertEqual(field.inst.low, 0)
            self.assertEqual(field.inst.high, 0)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("lsb_packing.reg1.y")
            self.assertEqual(field.inst.low, 6)
            self.assertEqual(field.inst.high, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("lsb_packing.reg1.z")
            self.assertEqual(field.inst.low, 10)
            self.assertEqual(field.inst.high, 12)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("lsb_packing.reg1.zz")
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
            field = top.find_by_path("lsb_packing.reg2.x")
            self.assertEqual(field.inst.low, 0)
            self.assertEqual(field.inst.high, 0)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("lsb_packing.reg2.y")
            self.assertEqual(field.inst.low, 6)
            self.assertEqual(field.inst.high, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("lsb_packing.reg2.z")
            self.assertEqual(field.inst.low, 10)
            self.assertEqual(field.inst.high, 12)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("lsb_packing.reg2.zz")
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
            field = top.find_by_path("msb_packing.reg1.x")
            self.assertEqual(field.inst.low, 31)
            self.assertEqual(field.inst.high, 31)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("msb_packing.reg1.y")
            self.assertEqual(field.inst.low, 6)
            self.assertEqual(field.inst.high, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("msb_packing.reg1.z")
            self.assertEqual(field.inst.low, 3)
            self.assertEqual(field.inst.high, 5)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("msb_packing.reg1.zz")
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
            field = top.find_by_path("msb_packing.reg2.x")
            self.assertEqual(field.inst.low, 15)
            self.assertEqual(field.inst.high, 15)
            self.assertEqual(field.inst.width, 1)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("msb_packing.reg2.y")
            self.assertEqual(field.inst.low, 6)
            self.assertEqual(field.inst.high, 9)
            self.assertEqual(field.inst.width, 4)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
        
        with self.subTest():
            field = top.find_by_path("msb_packing.reg2.z")
            self.assertEqual(field.inst.low, 3)
            self.assertEqual(field.inst.high, 5)
            self.assertEqual(field.inst.width, 3)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)
            
        with self.subTest():
            field = top.find_by_path("msb_packing.reg2.zz")
            self.assertEqual(field.inst.low, 1)
            self.assertEqual(field.inst.high, 2)
            self.assertEqual(field.inst.width, 2)
            self.assertEqual(field.get_property('fieldwidth'), field.inst.width)

#===============================================================================
# Validate inferred address placement/packing
#===============================================================================
class TestAddressingModes(RDLSourceTestCase):
    
    def test_example_5_1_2_2_2_ex1(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "example_5_1_2_2_2_ex1"
        )
        
        with self.subTest("reg a"):
            reg = top.find_by_path("example_5_1_2_2_2_ex1.a")
            self.assertEqual(reg.inst.addr_offset, 0)
            self.assertEqual(reg.absolute_address, 0)
            self.assertEqual(reg.size, 4)
        
        with self.subTest("reg b"):
            reg = top.find_by_path("example_5_1_2_2_2_ex1.b")
            self.assertEqual(reg.inst.addr_offset, 4)
            self.assertEqual(reg.absolute_address, 4)
            self.assertEqual(reg.size, 8)
        
        with self.subTest("reg c"):
            reg = top.find_by_path("example_5_1_2_2_2_ex1.c")
            self.assertEqual(reg.inst.addr_offset, 0x0C)
            self.assertEqual(reg.inst.is_array, True)
            self.assertEqual(reg.inst.array_dimensions, [20])
            self.assertEqual(reg.inst.array_stride, 4)
            self.assertEqual(reg.size, 4)
            self.assertEqual(reg.total_size, 20*4)
            
            for i in range(20):
                reg = top.find_by_path("example_5_1_2_2_2_ex1.c[%d]" % i)
                self.assertEqual(reg.absolute_address, 0x0C + i * 4)
    
    def test_example_5_1_2_2_2_ex2(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "example_5_1_2_2_2_ex2"
        )
        
        with self.subTest("reg a"):
            reg = top.find_by_path("example_5_1_2_2_2_ex2.a")
            self.assertEqual(reg.inst.addr_offset, 0)
            self.assertEqual(reg.absolute_address, 0)
            self.assertEqual(reg.size, 4)
        
        with self.subTest("reg b"):
            reg = top.find_by_path("example_5_1_2_2_2_ex2.b")
            self.assertEqual(reg.inst.addr_offset, 8)
            self.assertEqual(reg.absolute_address, 8)
            self.assertEqual(reg.size, 8)
        
        with self.subTest("reg c"):
            reg = top.find_by_path("example_5_1_2_2_2_ex2.c")
            self.assertEqual(reg.inst.addr_offset, 0x10)
            self.assertEqual(reg.inst.is_array, True)
            self.assertEqual(reg.inst.array_dimensions, [20])
            self.assertEqual(reg.inst.array_stride, 4)
            self.assertEqual(reg.size, 4)
            self.assertEqual(reg.total_size, 20*4)
            
            for i in range(20):
                reg = top.find_by_path("example_5_1_2_2_2_ex2.c[%d]" % i)
                self.assertEqual(reg.absolute_address, 0x10 + i * 4)
    
    def test_example_5_1_2_2_2_ex3(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "example_5_1_2_2_2_ex3"
        )
        
        with self.subTest("reg a"):
            reg = top.find_by_path("example_5_1_2_2_2_ex3.a")
            self.assertEqual(reg.inst.addr_offset, 0)
            self.assertEqual(reg.absolute_address, 0)
            self.assertEqual(reg.size, 4)
        
        with self.subTest("reg b"):
            reg = top.find_by_path("example_5_1_2_2_2_ex3.b")
            self.assertEqual(reg.inst.addr_offset, 8)
            self.assertEqual(reg.absolute_address, 8)
            self.assertEqual(reg.size, 8)
        
        with self.subTest("reg c"):
            reg = top.find_by_path("example_5_1_2_2_2_ex3.c")
            self.assertEqual(reg.inst.addr_offset, 0x10)
            self.assertEqual(reg.inst.is_array, True)
            self.assertEqual(reg.inst.array_dimensions, [20])
            self.assertEqual(reg.inst.array_stride, 4)
            self.assertEqual(reg.size, 4)
            self.assertEqual(reg.total_size, 20*4)
            
            for i in range(20):
                reg = top.find_by_path("example_5_1_2_2_2_ex3.c[%d]" % i)
                self.assertEqual(reg.absolute_address, 0x10 + i * 4)
    
    def test_example_5_1_2_2_2_ex4(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "example_5_1_2_2_2_ex4"
        )
        
        with self.subTest("reg a"):
            reg = top.find_by_path("example_5_1_2_2_2_ex4.a")
            self.assertEqual(reg.inst.addr_offset, 0)
            self.assertEqual(reg.absolute_address, 0)
            self.assertEqual(reg.size, 4)
        
        with self.subTest("reg b"):
            reg = top.find_by_path("example_5_1_2_2_2_ex4.b")
            self.assertEqual(reg.inst.addr_offset, 8)
            self.assertEqual(reg.absolute_address, 8)
            self.assertEqual(reg.size, 8)
        
        with self.subTest("reg c"):
            reg = top.find_by_path("example_5_1_2_2_2_ex4.c")
            self.assertEqual(reg.inst.addr_offset, 0x80)
            self.assertEqual(reg.inst.is_array, True)
            self.assertEqual(reg.inst.array_dimensions, [20])
            self.assertEqual(reg.inst.array_stride, 4)
            self.assertEqual(reg.size, 4)
            self.assertEqual(reg.total_size, 20*4)
            
            for i in range(20):
                reg = top.find_by_path("example_5_1_2_2_2_ex4.c[%d]" % i)
                self.assertEqual(reg.absolute_address, 0x80 + i * 4)

#-------------------------------------------------------------------------------
class TestAddressAllocators(RDLSourceTestCase):
    
    def test_example_5_1_2_5_ex1(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "example_5_1_2_5_ex1"
        )
        
        with self.subTest("reg a"):
            reg = top.find_by_path("example_5_1_2_5_ex1.example.a")
            self.assertEqual(reg.inst.addr_offset, 0x0)
            self.assertEqual(reg.absolute_address, 0x0)
            self.assertEqual(reg.size, 4)
        
        with self.subTest("reg b"):
            reg = top.find_by_path("example_5_1_2_5_ex1.example.b")
            self.assertEqual(reg.inst.addr_offset, 0x4)
            self.assertEqual(reg.absolute_address, 0x4)
            self.assertEqual(reg.size, 4)
        
        with self.subTest("reg c"):
            reg = top.find_by_path("example_5_1_2_5_ex1.example.c")
            self.assertEqual(reg.inst.addr_offset, 0x8)
            self.assertEqual(reg.absolute_address, 0x8)
            self.assertEqual(reg.size, 4)
        
        with self.subTest("reg d"):
            reg = top.find_by_path("example_5_1_2_5_ex1.example.d")
            self.assertEqual(reg.inst.addr_offset, 0x10)
            self.assertEqual(reg.absolute_address, 0x10)
            self.assertEqual(reg.size, 4)
    
    def test_example_5_1_2_5_ex2(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "example_5_1_2_5_ex2"
        )
        
        with self.subTest("reg a"):
            reg = top.find_by_path("example_5_1_2_5_ex2.example.a")
            self.assertEqual(reg.inst.addr_offset, 0x0)
            self.assertEqual(reg.inst.is_array, True)
            self.assertEqual(reg.inst.array_dimensions, [10])
            self.assertEqual(reg.inst.array_stride, 4)
            self.assertEqual(reg.size, 4)
            self.assertEqual(reg.total_size, 40)
            
            for i in range(10):
                reg = top.find_by_path("example_5_1_2_5_ex2.example.a[%d]" % i)
                self.assertEqual(reg.absolute_address, 0x0 + i * 4)
        
        with self.subTest("reg b"):
            reg = top.find_by_path("example_5_1_2_5_ex2.example.b")
            self.assertEqual(reg.inst.addr_offset, 0x100)
            self.assertEqual(reg.inst.is_array, True)
            self.assertEqual(reg.inst.array_dimensions, [10])
            self.assertEqual(reg.inst.array_stride, 0x10)
            self.assertEqual(reg.size, 4)
            self.assertEqual(reg.total_size, 10*16-12)
            
            for i in range(10):
                reg = top.find_by_path("example_5_1_2_5_ex2.example.b[%d]" % i)
                self.assertEqual(reg.absolute_address, 0x100 + i * 0x10)
    
    def test_example_5_1_2_5_ex3(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "example_5_1_2_5_ex3"
        )
        
        with self.subTest("reg a"):
            reg = top.find_by_path("example_5_1_2_5_ex3.example.a")
            self.assertEqual(reg.inst.addr_offset, 0x0)
            self.assertEqual(reg.inst.is_array, True)
            self.assertEqual(reg.inst.array_dimensions, [10])
            self.assertEqual(reg.inst.array_stride, 4)
            self.assertEqual(reg.size, 4)
            self.assertEqual(reg.total_size, 40)
            
            for i in range(10):
                reg = top.find_by_path("example_5_1_2_5_ex3.example.a[%d]" % i)
                self.assertEqual(reg.absolute_address, 0x0 + i * 4)
        
        with self.subTest("reg b"):
            reg = top.find_by_path("example_5_1_2_5_ex3.example.b")
            self.assertEqual(reg.inst.addr_offset, 0x100)
            self.assertEqual(reg.inst.is_array, True)
            self.assertEqual(reg.inst.array_dimensions, [10])
            self.assertEqual(reg.inst.array_stride, 0x10)
            self.assertEqual(reg.size, 4)
            self.assertEqual(reg.total_size, 10*16-12)
            
            for i in range(10):
                reg = top.find_by_path("example_5_1_2_5_ex3.example.b[%d]" % i)
                self.assertEqual(reg.absolute_address, 0x100 + i * 0x10)
        
        with self.subTest("reg c"):
            reg = top.find_by_path("example_5_1_2_5_ex3.example.c")
            self.assertEqual(reg.inst.addr_offset, 0x200)
            self.assertEqual(reg.absolute_address, 0x200)
            self.assertEqual(reg.size, 4)

#-------------------------------------------------------------------------------
class TestHierarchicalAddressing(RDLSourceTestCase):
    
    def test_hier(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )
        
        # Spot-check a few nodes
        with self.subTest():
            node = top.find_by_path("hier.x")
            self.assertEqual(node.absolute_address, 0x0)
            self.assertEqual(node.size, 148)
            self.assertEqual(node.total_size, 148)
        
        with self.subTest():
            node = top.find_by_path("hier.x.a[0][1]")
            self.assertEqual(node.absolute_address, 0x4)
            self.assertEqual(node.size, 4)
            self.assertEqual(node.total_size, 60)
        
        with self.subTest():
            node = top.find_by_path("hier.x.a[1][1]")
            self.assertEqual(node.absolute_address, 0x10)
        
        with self.subTest():
            node = top.find_by_path("hier.y[0]")
            self.assertEqual(node.absolute_address, 0x100)
            self.assertEqual(node.size, 148)
            self.assertEqual(node.total_size, 148*4)
        
        with self.subTest():
            node = top.find_by_path("hier.y[2]")
            self.assertEqual(node.absolute_address, 0x100+148*2)
            self.assertEqual(node.size, 148)
            self.assertEqual(node.total_size, 148*4)
