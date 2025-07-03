from unittest_utils import RDLSourceTestCase

class TestParameters(RDLSourceTestCase):

    def test_signalwidth(self):
        root = self.compile(
            ["rdl_src/signals.rdl"],
            "top"
        )
        self.assertEqual(root.find_by_path("top.s1").width, 8)
        self.assertEqual(root.find_by_path("top.r1.s1").width, 6)
        self.assertEqual(root.find_by_path("top.r1.f1.s1").width, 4)

    def test_field_resets(self):
        root = self.compile(
            ["rdl_src/reset_signals.rdl"],
            "field_resets"
        )
        top = root.top

        self.assertIs(top.find_by_path("not_a_reset").get_property('field_reset'), False)

        self.assertEqual(
            top.find_by_path("rf.x.A").get_property('resetsignal'),
            top.find_by_path("rf.x.reset_z"),
        )

        self.assertEqual(
            top.find_by_path("rf.x.B").get_property('resetsignal'),
            top.find_by_path("reset_x"),
        )

        self.assertEqual(
            top.find_by_path("rf.x.C").get_property('resetsignal'),
            top.find_by_path("rf.reset_y"),
        )

        self.assertEqual(
            top.find_by_path("rf.y.A").get_property('resetsignal'),
            top.find_by_path("rf.reset_y"),
        )

        self.assertEqual(
            top.find_by_path("rf.y.B").get_property('resetsignal'),
            top.find_by_path("reset_x"),
        )

        self.assertIsNone(
            top.find_by_path("z.A").get_property('resetsignal')
        )

        self.assertEqual(
            top.find_by_path("z.B").get_property('resetsignal'),
            top.find_by_path("reset_x"),
        )

    def test_cpuif_resets(self):
        root = self.compile(
            ["rdl_src/reset_signals.rdl"],
            "cpuif_resets"
        )
        top = root.top

        reset_x = top.find_by_path("rf.reset_x")
        reset_y = top.find_by_path("rf.x.reset_y")

        self.assertIs(top.find_by_path("not_a_reset").get_property('cpuif_reset'), False)

        self.assertIsNone(root.find_by_path("cpuif_resets").cpuif_reset)
        self.assertEqual(top.find_by_path("rf").cpuif_reset, reset_x)
        self.assertEqual(top.find_by_path("rf.x").cpuif_reset, reset_y)
        self.assertEqual(top.find_by_path("rf.x.A").cpuif_reset, reset_y)
        self.assertEqual(top.find_by_path("rf.y").cpuif_reset, reset_x)
        self.assertEqual(top.find_by_path("rf.y.A").cpuif_reset, reset_x)
        self.assertIsNone(top.find_by_path("z").cpuif_reset)
        self.assertIsNone(top.find_by_path("z.A").cpuif_reset)

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
