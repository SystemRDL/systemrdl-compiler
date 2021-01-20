from unittest_utils import RDLSourceTestCase

from systemrdl import rdltypes

class TestPropSideEffects(RDLSourceTestCase):

    def test_property_side_effects(self):
        root = self.compile(
            ["rdl_src/property_side_effects.rdl"],
            "top"
        )

        #-----------------------------------------------------------------------
        with self.subTest("bool pair"):
            self.assertFalse(root.find_by_path("top.my_signal").get_property('async'))
            self.assertTrue(root.find_by_path("top.my_signal").get_property('sync'))

        #-----------------------------------------------------------------------
        with self.subTest("rclr"):
            self.assertFalse(root.find_by_path("top.r1.f0").get_property('rclr'))
            self.assertTrue(root.find_by_path("top.r1.f1").get_property('rclr'))
            self.assertFalse(root.find_by_path("top.r1.f2").get_property('rclr'))
            self.assertTrue(root.find_by_path("top.r1.f3").get_property('rclr'))
            self.assertFalse(root.find_by_path("top.r1.f4").get_property('rclr'))
            self.assertTrue(root.find_by_path("top.r1.f5").get_property('rclr'))
            self.assertFalse(root.find_by_path("top.r1.f6").get_property('rclr'))
            self.assertTrue(root.find_by_path("top.r1.f7").get_property('rclr'))
            self.assertFalse(root.find_by_path("top.r1.f8").get_property('rclr'))

        with self.subTest("rset"):
            self.assertFalse(root.find_by_path("top.r1.f0").get_property('rset'))
            self.assertFalse(root.find_by_path("top.r1.f1").get_property('rset'))
            self.assertTrue(root.find_by_path("top.r1.f2").get_property('rset'))
            self.assertFalse(root.find_by_path("top.r1.f3").get_property('rset'))
            self.assertTrue(root.find_by_path("top.r1.f4").get_property('rset'))
            self.assertFalse(root.find_by_path("top.r1.f5").get_property('rset'))
            self.assertTrue(root.find_by_path("top.r1.f6").get_property('rset'))
            self.assertFalse(root.find_by_path("top.r1.f7").get_property('rset'))
            self.assertTrue(root.find_by_path("top.r1.f8").get_property('rset'))

        with self.subTest("onread"):
            self.assertIsNone(root.find_by_path("top.r1.f0").get_property('onread'))

            self.assertEqual(
                root.find_by_path("top.r1.f1").get_property('onread'),
                rdltypes.OnReadType.rclr
            )

            self.assertEqual(
                root.find_by_path("top.r1.f2").get_property('onread'),
                rdltypes.OnReadType.rset
            )

            self.assertEqual(
                root.find_by_path("top.r1.f3").get_property('onread'),
                rdltypes.OnReadType.rclr
            )

            self.assertEqual(
                root.find_by_path("top.r1.f4").get_property('onread'),
                rdltypes.OnReadType.rset
            )

            self.assertEqual(
                root.find_by_path("top.r1.f5").get_property('onread'),
                rdltypes.OnReadType.rclr
            )

            self.assertEqual(
                root.find_by_path("top.r1.f6").get_property('onread'),
                rdltypes.OnReadType.rset
            )

            self.assertEqual(
                root.find_by_path("top.r1.f7").get_property('onread'),
                rdltypes.OnReadType.rclr
            )

            self.assertEqual(
                root.find_by_path("top.r1.f8").get_property('onread'),
                rdltypes.OnReadType.rset
            )

        #-----------------------------------------------------------------------
        with self.subTest("woclr"):
            self.assertFalse(root.find_by_path("top.r2.f0").get_property('woclr'))
            self.assertTrue(root.find_by_path("top.r2.f1").get_property('woclr'))
            self.assertFalse(root.find_by_path("top.r2.f2").get_property('woclr'))
            self.assertTrue(root.find_by_path("top.r2.f3").get_property('woclr'))
            self.assertFalse(root.find_by_path("top.r2.f4").get_property('woclr'))
            self.assertTrue(root.find_by_path("top.r2.f5").get_property('woclr'))
            self.assertFalse(root.find_by_path("top.r2.f6").get_property('woclr'))
            self.assertTrue(root.find_by_path("top.r2.f7").get_property('woclr'))
            self.assertFalse(root.find_by_path("top.r2.f8").get_property('woclr'))

        with self.subTest("woset"):
            self.assertFalse(root.find_by_path("top.r2.f0").get_property('woset'))
            self.assertFalse(root.find_by_path("top.r2.f1").get_property('woset'))
            self.assertTrue(root.find_by_path("top.r2.f2").get_property('woset'))
            self.assertFalse(root.find_by_path("top.r2.f3").get_property('woset'))
            self.assertTrue(root.find_by_path("top.r2.f4").get_property('woset'))
            self.assertFalse(root.find_by_path("top.r2.f5").get_property('woset'))
            self.assertTrue(root.find_by_path("top.r2.f6").get_property('woset'))
            self.assertFalse(root.find_by_path("top.r2.f7").get_property('woset'))
            self.assertTrue(root.find_by_path("top.r2.f8").get_property('woset'))

        with self.subTest("onwrite"):
            self.assertIsNone(root.find_by_path("top.r2.f0").get_property('onwrite'))

            self.assertEqual(
                root.find_by_path("top.r2.f1").get_property('onwrite'),
                rdltypes.OnWriteType.woclr
            )

            self.assertEqual(
                root.find_by_path("top.r2.f2").get_property('onwrite'),
                rdltypes.OnWriteType.woset
            )

            self.assertEqual(
                root.find_by_path("top.r2.f3").get_property('onwrite'),
                rdltypes.OnWriteType.woclr
            )

            self.assertEqual(
                root.find_by_path("top.r2.f4").get_property('onwrite'),
                rdltypes.OnWriteType.woset
            )

            self.assertEqual(
                root.find_by_path("top.r2.f5").get_property('onwrite'),
                rdltypes.OnWriteType.woclr
            )

            self.assertEqual(
                root.find_by_path("top.r2.f6").get_property('onwrite'),
                rdltypes.OnWriteType.woset
            )

            self.assertEqual(
                root.find_by_path("top.r2.f7").get_property('onwrite'),
                rdltypes.OnWriteType.woclr
            )

            self.assertEqual(
                root.find_by_path("top.r2.f8").get_property('onwrite'),
                rdltypes.OnWriteType.woset
            )

        #-----------------------------------------------------------------------
        with self.subTest("incrthreshold alias"):
            self.assertEqual(
                root.find_by_path("top.r3.f1").get_property('incrthreshold'),
                1
            )

            self.assertEqual(
                root.find_by_path("top.r3.f1").get_property('threshold'),
                1
            )

            self.assertEqual(
                root.find_by_path("top.r3.f2").get_property('incrthreshold'),
                2
            )

            self.assertEqual(
                root.find_by_path("top.r3.f2").get_property('threshold'),
                2
            )

        with self.subTest("incrsaturate alias"):
            self.assertEqual(
                root.find_by_path("top.r3.f1").get_property('incrsaturate'),
                3
            )

            self.assertEqual(
                root.find_by_path("top.r3.f1").get_property('saturate'),
                3
            )

            self.assertEqual(
                root.find_by_path("top.r3.f2").get_property('incrsaturate'),
                4
            )

            self.assertEqual(
                root.find_by_path("top.r3.f2").get_property('saturate'),
                4
            )
