from unittest_utils import RDLSourceTestCase

class TestPropRefs(RDLSourceTestCase):

    def test_prop_value_ref(self):
        root = self.compile(
            ["rdl_src/prop_ref.rdl"],
            "prop_value_ref"
        )
        top = root.top

        a = top.find_by_path("y.a")
        b = top.find_by_path("y.b")
        c = top.find_by_path("y.c")
        d = top.find_by_path("y.d")
        e = top.find_by_path("y.e")

        b_ref = b.get_property('next')
        c_ref = c.get_property('next')
        d_ref = d.get_property('next')
        e_ref = e.get_property('next')

        self.assertRegex(
            str(b_ref),
            r"<PropRef_reset prop_value_ref.y.a->reset at 0x\w+>"
        )

        self.assertEqual(b_ref.node, a)
        self.assertEqual(b_ref.name, "reset")
        self.assertEqual(b_ref, c_ref)
        self.assertNotEqual(c_ref, d_ref)
        self.assertNotEqual(d_ref, e_ref)
        self.assertNotEqual(b_ref, 1234)




    def test_prop_ref_in_array(self):
        root = self.compile(
            ["rdl_src/prop_ref.rdl"],
            "ref_in_array"
        )
        a0 = root.find_by_path("ref_in_array.myreg[0].a")
        b0 = root.find_by_path("ref_in_array.myreg[0].b")
        a1 = root.find_by_path("ref_in_array.myreg[1].a")
        b1 = root.find_by_path("ref_in_array.myreg[1].b")

        b0_next = b0.get_property('next')
        b1_next = b1.get_property('next')

        self.assertEqual(b0_next.node, a0)
        self.assertEqual(b0_next.name, 'anded')
        self.assertEqual(b1_next.node, a1)
        self.assertEqual(b1_next.name, 'anded')


    def test_inferred_vector(self):
        root = self.compile(
            ["rdl_src/prop_ref.rdl"],
            "inferred_vector"
        )
        a = root.find_by_path("inferred_vector.y.a")
        we_ref = root.find_by_path("inferred_vector.y.b").get_property('next')
        wel_ref = root.find_by_path("inferred_vector.y.c").get_property('next')

        self.assertEqual(we_ref.node, a)
        self.assertEqual(we_ref.name, "we")

        self.assertEqual(wel_ref.node, a)
        self.assertEqual(wel_ref.name, "wel")


    def test_err_missing_reset(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_missing_reset",
            r"Assignment references the value of property 'reset', but its value was never set for instance 'a'"
        )


    def test_err_circular_ref(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_circular_ref",
            r"Assignment creates a circular reference"
        )

    def test_err_self_reset(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_self_reset",
            r"Field 'a' cannot reference itself in reset property"
        )

    def test_err_no_inferred(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_no_inferred",
            r"Assignment references property 'we', but the signal it represents was never defined or enabled for instance 'a'"
        )


    def test_err_not_a_counter(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_not_a_counter",
            r"Reference to property 'incr' is illegal because 'a' is not a counter"
        )


    def test_err_no_counter_threshold(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_no_counter_threshold",
            r"Reference to property 'incrthreshold' is illegal because the target field does not define any thresholds"
        )
