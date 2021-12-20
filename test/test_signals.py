from unittest_utils import RDLSourceTestCase

class TestParameters(RDLSourceTestCase):

    def test_signalwidth(self):
        root = self.compile(
            ["rdl_src/signals.rdl"],
            "top"
        )
        self.assertEqual(root.find_by_path("top.s1").width, 8)

    def test_field_resets(self):
        root = self.compile(
            ["rdl_src/reset_signals.rdl"],
            "field_resets"
        )

        self.assertEqual(
            root.find_by_path("field_resets.rf.x.A").get_property('resetsignal'),
            root.find_by_path("field_resets.rf.x.reset_z"),
        )

        self.assertEqual(
            root.find_by_path("field_resets.rf.x.B").get_property('resetsignal'),
            root.find_by_path("field_resets.reset_x"),
        )

        self.assertEqual(
            root.find_by_path("field_resets.rf.x.C").get_property('resetsignal'),
            root.find_by_path("field_resets.rf.reset_y"),
        )

        self.assertEqual(
            root.find_by_path("field_resets.rf.y.A").get_property('resetsignal'),
            root.find_by_path("field_resets.rf.reset_y"),
        )

        self.assertEqual(
            root.find_by_path("field_resets.rf.y.B").get_property('resetsignal'),
            root.find_by_path("field_resets.reset_x"),
        )

        self.assertIsNone(
            root.find_by_path("field_resets.z.A").get_property('resetsignal')
        )

        self.assertEqual(
            root.find_by_path("field_resets.z.B").get_property('resetsignal'),
            root.find_by_path("field_resets.reset_x"),
        )

    def test_cpuif_resets(self):
        root = self.compile(
            ["rdl_src/reset_signals.rdl"],
            "cpuif_resets"
        )
        reset_x = root.find_by_path("cpuif_resets.rf.reset_x")
        reset_y = root.find_by_path("cpuif_resets.rf.x.reset_y")

        self.assertIsNone(root.find_by_path("cpuif_resets").cpuif_reset)
        self.assertEqual(root.find_by_path("cpuif_resets.rf").cpuif_reset, reset_x)
        self.assertEqual(root.find_by_path("cpuif_resets.rf.x").cpuif_reset, reset_y)
        self.assertEqual(root.find_by_path("cpuif_resets.rf.x.A").cpuif_reset, reset_y)
        self.assertEqual(root.find_by_path("cpuif_resets.rf.y").cpuif_reset, reset_x)
        self.assertEqual(root.find_by_path("cpuif_resets.rf.y.A").cpuif_reset, reset_x)
        self.assertIsNone(root.find_by_path("cpuif_resets.z").cpuif_reset)
        self.assertIsNone(root.find_by_path("cpuif_resets.z.A").cpuif_reset)

    def test_field_reset_err(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_reset_signals.rdl"],
            "field_resets",
            r"Only one 'field_reset' signal is allowed per hierarchy. Signal 'freset_root2' is redundant."
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_reset_signals.rdl"],
            "field_resets",
            r"Only one 'field_reset' signal is allowed per hierarchy. Signal 'reset_b' is redundant."
        )

    def test_cpuif_reset_err(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_reset_signals.rdl"],
            "cpuif_resets",
            r"Only one 'cpuif_reset' signal is allowed per hierarchy. Signal 'creset_root2' is redundant."
        )

        self.assertRDLCompileError(
            ["rdl_err_src/err_reset_signals.rdl"],
            "cpuif_resets",
            r"Only one 'cpuif_reset' signal is allowed per hierarchy. Signal 'reset_y' is redundant."
        )
