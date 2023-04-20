
from unittest_utils import RDLSourceTestCase
import systemrdl.rdltypes as rdlt

class TestIntr(RDLSourceTestCase):

    def test_intr_prop_mod(self):
        root = self.compile(
            ["rdl_src/intr_prop_mod.rdl"],
            "intr_prop_mod_test"
        )
        top = root.top

        with self.subTest("irq1"):
            irq1 = top.find_by_path("reg1.irq1")
            self.assertEqual(irq1.get_property('intr'), True)
            self.assertEqual(irq1.get_property('intr type'), rdlt.InterruptType.posedge)
            self.assertEqual(irq1.get_property('stickybit'), True)

        with self.subTest("irq2"):
            irq2 = top.find_by_path("reg1.irq2")
            self.assertEqual(irq2.get_property('intr'), True)
            self.assertEqual(irq2.get_property('intr type'), rdlt.InterruptType.posedge)
            self.assertEqual(irq2.get_property('stickybit'), True)

        with self.subTest("irq3"):
            irq3 = top.find_by_path("reg1.irq3")
            self.assertEqual(irq3.get_property('intr'), False)
            self.assertEqual(irq3.get_property('stickybit'), False)

        with self.subTest("irq4"):
            irq4 = top.find_by_path("reg1.irq4")
            self.assertEqual(irq4.get_property('intr'), True)
            self.assertEqual(irq4.get_property('intr type'), rdlt.InterruptType.negedge)
            self.assertEqual(irq4.get_property('stickybit'), True)

        with self.subTest("irqA"):
            irqA = top.find_by_path("reg2.irqA")
            self.assertEqual(irqA.get_property('intr'), True)
            self.assertEqual(irqA.get_property('intr type'), rdlt.InterruptType.posedge)
            self.assertEqual(irqA.get_property('stickybit'), False)

        with self.subTest("irqX"):
            irqX = top.find_by_path("reg3.irqX")
            self.assertEqual(irqX.get_property('intr'), True)
            self.assertEqual(irqX.get_property('intr type'), rdlt.InterruptType.level)


    def test_intr_example(self):
        root = self.compile(
            ["rdl_src/intr_prop.rdl"],
            "int_map_m"
        )
        top = root.top

        self.assertIs(top.find_by_path("block_a_int").is_interrupt_reg, True)
        self.assertIs(top.find_by_path("block_a_int").is_halt_reg, True)
        self.assertIs(top.find_by_path("block_a_int_en").is_interrupt_reg, False)
        self.assertIs(top.find_by_path("block_a_int_en").is_halt_reg, False)
