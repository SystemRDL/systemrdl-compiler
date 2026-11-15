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

    def test_bridge_size_of_largest_child(self):
        top = self.compile(
            ["rdl_src/bridge_size_order.rdl"],
            "bridge_root"
        )

        # All children of a bridge start at offset 0, so the size of the bridge
        # is set by the largest child even if it is not the last one
        self.assertEqual(
            top.find_by_path("bridge_root").size,
            0x8
        )

        self.assertEqual(
            top.find_by_path("bridge_root.big").size,
            0x8
        )

        self.assertEqual(
            top.find_by_path("bridge_root.small").size,
            0x4
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
