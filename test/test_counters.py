from unittest_utils import RDLSourceTestCase

class TestCounters(RDLSourceTestCase):
    def test_counter_examples(self):
        root = self.compile(
            ["rdl_src/counter_examples.rdl"],
            "wrapper"
        )
        top = root.top

        # 9.8.1 Example 1
        f = top.find_by_path("example_9_8_1_e1.count1")
        self.assertTrue(f.is_up_counter)
        self.assertFalse(f.is_down_counter)
        self.assertEqual(f.get_property('incrvalue'), 3)
        self.assertIsNone(f.get_property('decrvalue'))

        f = top.find_by_path("example_9_8_1_e1.count2")
        self.assertFalse(f.is_up_counter)
        self.assertTrue(f.is_down_counter)
        self.assertIsNone(f.get_property('incrvalue'))
        self.assertIsNone(f.get_property('decrvalue'))

        f = top.find_by_path("example_9_8_1_e1.count3")
        self.assertTrue(f.is_up_counter)
        self.assertTrue(f.is_down_counter)
        self.assertEqual(f.get_property('incrvalue'), 2)
        self.assertEqual(f.get_property('decrvalue'), 4)

        f = top.find_by_path("example_9_8_1_e1.count4")
        self.assertTrue(f.is_up_counter)
        self.assertFalse(f.is_down_counter)

        f = top.find_by_path("example_9_8_1_e1.count4_incr")
        self.assertFalse(f.is_up_counter)
        self.assertFalse(f.is_down_counter)

        # 9.8.1 Example 2
        f = top.find_by_path("example_9_8_1_e2.count1_low.count")
        self.assertTrue(f.is_up_counter)
        self.assertFalse(f.is_down_counter)
        self.assertEqual(f.get_property('incrvalue'), 1)
        self.assertIsNone(f.get_property('decrvalue'))
        f = top.find_by_path("example_9_8_1_e2.count1_high.count")
        self.assertTrue(f.is_up_counter)
        self.assertFalse(f.is_down_counter)
        self.assertEqual(f.get_property('incrvalue'), 1)
        self.assertIsNone(f.get_property('decrvalue'))

        # 9.8.2 Example 1
        f = top.find_by_path("example_9_8_2_e1.count1")
        self.assertTrue(f.is_up_counter)
        self.assertFalse(f.is_down_counter)
        f = top.find_by_path("example_9_8_2_e1.count2")
        self.assertFalse(f.is_up_counter)
        self.assertTrue(f.is_down_counter)
        f = top.find_by_path("example_9_8_2_e1.count3")
        self.assertTrue(f.is_up_counter)
        self.assertTrue(f.is_down_counter)
        f = top.find_by_path("example_9_8_2_e1.count4_sat")
        self.assertFalse(f.is_up_counter)
        self.assertFalse(f.is_down_counter)
        f = top.find_by_path("example_9_8_2_e1.count4_thresh")
        self.assertFalse(f.is_up_counter)
        self.assertFalse(f.is_down_counter)
        f = top.find_by_path("example_9_8_2_e1.count4")
        self.assertTrue(f.is_up_counter)
        self.assertFalse(f.is_down_counter)

    def test_basics(self):
        root = self.compile(
            ["rdl_src/counter_extras.rdl"],
            "top"
        )
        top = root.top

        f1 = top.find_by_path("r1.f1")
        self.assertTrue(f1.get_property('counter'))
        self.assertEqual(f1.get_property('incr'), top.find_by_path("incr_signal"))
        self.assertEqual(f1.get_property('decr'), top.find_by_path("decr_signal"))
        self.assertTrue(f1.get_property('overflow'))
        self.assertTrue(f1.get_property('underflow'))
        self.assertEqual(f1.get_property('incrwidth'), 2)
        self.assertEqual(f1.get_property('decrwidth'), 3)

        f2 = top.find_by_path("r1.f2")
        self.assertEqual(f2.is_up_counter, True)
        self.assertEqual(f2.is_down_counter, True)
        self.assertEqual(f2.get_property('incrvalue'), 1)
        self.assertEqual(f2.get_property('decrvalue'), 1)
        self.assertEqual(f2.implements_storage, True)
