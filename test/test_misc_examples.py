from unittest_utils import RDLSourceTestCase

class TestMiscExamples(RDLSourceTestCase):
    def test_resetsignal_example(self):
        root = self.compile(
            ["rdl_src/signals_and_reset.rdl"],
            "top"
        )
        top = root.top

        reset = top.find_by_path("reset_l")
        field1 = top.find_by_path("some_reg_inst.field1")
        field2 = top.find_by_path("some_reg_inst.field2")
        self.assertIsNone(field1.get_property('resetsignal'))
        self.assertEqual(field2.get_property('resetsignal'), reset)


    def test_pci_reset_example(self):
        root = self.compile(
            ["rdl_src/signals_and_reset.rdl"],
            "top2"
        )
        top = root.top

        pci_soft_reset = top.find_by_path("pci_soft_reset")
        pci_hard_reset = top.find_by_path("pci_hard_reset")
        cplCode = top.find_by_path("PCIE_REG_BIST.cplCode")
        start = top.find_by_path("PCIE_REG_BIST.start")
        capable = top.find_by_path("PCIE_REG_BIST.capable")

        self.assertEqual(cplCode.get_property('resetsignal'), pci_soft_reset)
        self.assertEqual(start.get_property('resetsignal'), pci_soft_reset)
        self.assertEqual(capable.get_property('resetsignal'), pci_hard_reset)

        self.assertEqual(cplCode.cpuif_reset, pci_hard_reset)
        self.assertEqual(start.cpuif_reset, pci_hard_reset)
        self.assertEqual(capable.cpuif_reset, pci_hard_reset)

    def test_rest_signal_value(self):
        root = self.compile(
            ["rdl_src/signals_and_reset.rdl"],
            "foo"
        )
        top = root.top
        a = top.find_by_path("reg1.a")
        mysig = top.find_by_path("mySig")
        self.assertEqual(a.get_property('reset'), mysig)
