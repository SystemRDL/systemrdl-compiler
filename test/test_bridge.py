from unittest_utils import RDLSourceTestCase

class TestBridge(RDLSourceTestCase):

    def test_bridge(self):
        top = self.compile(
            ["rdl_src/bridge.rdl"],
            "some_bridge"
        )

        self.assertEqual(
            top.find_by_path("some_bridge.ahb.ahb_credits").absolute_address,
            0x0
        )

        self.assertEqual(
            top.find_by_path("some_bridge.ahb.ahb_stat").absolute_address,
            0x20
        )

        self.assertEqual(
            top.find_by_path("some_bridge.axi.axi_credits").absolute_address,
            0x0
        )

        self.assertEqual(
            top.find_by_path("some_bridge.axi.axi_stat").absolute_address,
            0x40
        )

    def test_bridge_errors(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_bridge.rdl"],
            "illegal_wrapper",
            r"The 'bridge' property can only be applied to the root address map"
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_bridge.rdl"],
            "not_enough_addrmaps",
            r"Addrmap 'not_enough_addrmaps' is a bridge and shall contain 2 or more sub-addrmaps"
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_bridge.rdl"],
            "illegal_children",
            r"Addrmap 'illegal_children' is a bridge which can only contain other addrmaps. Contains a child instance 'y' which is a reg"
        )
