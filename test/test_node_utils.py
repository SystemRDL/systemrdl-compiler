
from .unittest_utils import RDLSourceTestCase

#===============================================================================
# Validate inferred field bit placement/packing
#===============================================================================
class TestNodeUtils(RDLSourceTestCase):

    def test_index_tools(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )

        with self.subTest("hier.x"):
            node = top.find_by_path("hier.x")
            self.assertEqual(node.get_path(), "hier.x")
            node.clear_lineage_index()
            self.assertEqual(node.get_path(), "hier.x")
            node.zero_lineage_index()
            self.assertEqual(node.get_path(), "hier.x")

        with self.subTest("hier.y.a"):
            node = top.find_by_path("hier.y[2].a")
            self.assertEqual(node.get_path(), "hier.y[2].a[][]")
            node.zero_lineage_index()
            self.assertEqual(node.get_path(), "hier.y[0].a[0][0]")
            node.clear_lineage_index()
            self.assertEqual(node.get_path(), "hier.y[].a[][]")
    
    def test_address_tools(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )

        with self.subTest("hier.y[2].a"):
            node = top.find_by_path("hier.y[2].a")
            with self.assertRaises(ValueError):
                node.address_offset
            with self.assertRaises(ValueError):
                node.absolute_address
            self.assertEqual(node.raw_address_offset, 0)
            self.assertEqual(node.raw_absolute_address, 0x100)
        
        with self.subTest("hier.y.c[1][1]"):
            node = top.find_by_path("hier.y.c[1][1]")
            self.assertEqual(node.address_offset, 0x64 + 4*4+4)
            with self.assertRaises(ValueError):
                node.absolute_address
            self.assertEqual(node.raw_address_offset, 0x64)
            self.assertEqual(node.raw_absolute_address, 0x100 + 0x64)

    def test_repr(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )

        node = top.find_by_path("hier.x.b.a")
        self.assertRegex(str(node), "<FieldNode hier\.x\.b\[\]\.a at 0x\w+>")
