from systemrdl.node import RegNode, FieldNode, RegfileNode
from unittest_utils import RDLSourceTestCase

class TestDPAs(RDLSourceTestCase):
    def test_dpa_name_generation(self):
        top = self.compile(
            ["rdl_src/dpa_names.rdl"],
            "dpa_overrides"
        )

        self.assertEqual(top.find_by_path("dpa_overrides.r0.f1").type_name, "my_field")
        self.assertEqual(top.find_by_path("dpa_overrides.r0.f2").type_name, "my_field_rclr_t")
        self.assertEqual(top.find_by_path("dpa_overrides.r0.f3").type_name, "my_field_encode_onoff_e_next_50a21c60")
        self.assertEqual(top.find_by_path("dpa_overrides.r0").type_name,    "my_reg")

        self.assertEqual(top.find_by_path("dpa_overrides.r1.f1").type_name, "my_field_rclr_t")
        self.assertEqual(top.find_by_path("dpa_overrides.r1.f2").type_name, "my_field_rclr_t")
        self.assertEqual(top.find_by_path("dpa_overrides.r1.f3").type_name, "my_field_encode_onoff_e_next_50a21c60")
        self.assertEqual(top.find_by_path("dpa_overrides.r1").type_name,    "my_reg_f1_4e12afb6")

        self.assertEqual(top.find_by_path("dpa_overrides.r2.f1").type_name, "my_field_next_c9e1f96f")
        self.assertEqual(top.find_by_path("dpa_overrides.r2.f2").type_name, "my_field_rclr_t")
        self.assertEqual(top.find_by_path("dpa_overrides.r2.f3").type_name, "my_field_encode_onoff_e_next_50a21c60")
        self.assertEqual(top.find_by_path("dpa_overrides.r2").type_name,    "my_reg_f1_e0f883f9")

    def test_nested_dpa(self):
        top = self.compile(
            ["rdl_src/nested_dpa.rdl"],
            "e"
        )

        expected_desc = {
            "e.d1.c1.b1.a1": "a",
            "e.d1.c1.b1.a2": "b",
            "e.d1.c1.b1.a3": "a",
            "e.d1.c1.b2.a1": "a",
            "e.d1.c1.b2.a2": "c",
            "e.d1.c1.b2.a3": "a",
            "e.d1.c1.b3.a1": "a",
            "e.d1.c1.b3.a2": "b",
            "e.d1.c1.b3.a3": "a",
            "e.d1.c2.b1.a1": "a",
            "e.d1.c2.b1.a2": "b",
            "e.d1.c2.b1.a3": "a",
            "e.d1.c2.b2.a1": "a",
            "e.d1.c2.b2.a2": "d",
            "e.d1.c2.b2.a3": "a",
            "e.d1.c2.b3.a1": "a",
            "e.d1.c2.b3.a2": "b",
            "e.d1.c2.b3.a3": "a",
            "e.d1.c3.b1.a1": "a",
            "e.d1.c3.b1.a2": "b",
            "e.d1.c3.b1.a3": "a",
            "e.d1.c3.b2.a1": "a",
            "e.d1.c3.b2.a2": "c",
            "e.d1.c3.b2.a3": "a",
            "e.d1.c3.b3.a1": "a",
            "e.d1.c3.b3.a2": "b",
            "e.d1.c3.b3.a3": "a",
            "e.d2.c1.b1.a1": "a",
            "e.d2.c1.b1.a2": "b",
            "e.d2.c1.b1.a3": "a",
            "e.d2.c1.b2.a1": "a",
            "e.d2.c1.b2.a2": "c",
            "e.d2.c1.b2.a3": "a",
            "e.d2.c1.b3.a1": "a",
            "e.d2.c1.b3.a2": "b",
            "e.d2.c1.b3.a3": "a",
            "e.d2.c2.b1.a1": "a",
            "e.d2.c2.b1.a2": "b",
            "e.d2.c2.b1.a3": "a",
            "e.d2.c2.b2.a1": "a",
            "e.d2.c2.b2.a2": "e",
            "e.d2.c2.b2.a3": "a",
            "e.d2.c2.b3.a1": "a",
            "e.d2.c2.b3.a2": "b",
            "e.d2.c2.b3.a3": "a",
            "e.d2.c3.b1.a1": "a",
            "e.d2.c3.b1.a2": "b",
            "e.d2.c3.b1.a3": "a",
            "e.d2.c3.b2.a1": "a",
            "e.d2.c3.b2.a2": "c",
            "e.d2.c3.b2.a3": "a",
            "e.d2.c3.b3.a1": "a",
            "e.d2.c3.b3.a2": "b",
            "e.d2.c3.b3.a3": "a",
            "e.d3.c1.b1.a1": "a",
            "e.d3.c1.b1.a2": "b",
            "e.d3.c1.b1.a3": "a",
            "e.d3.c1.b2.a1": "a",
            "e.d3.c1.b2.a2": "c",
            "e.d3.c1.b2.a3": "a",
            "e.d3.c1.b3.a1": "a",
            "e.d3.c1.b3.a2": "b",
            "e.d3.c1.b3.a3": "a",
            "e.d3.c2.b1.a1": "a",
            "e.d3.c2.b1.a2": "b",
            "e.d3.c2.b1.a3": "a",
            "e.d3.c2.b2.a1": "a",
            "e.d3.c2.b2.a2": "d",
            "e.d3.c2.b2.a3": "a",
            "e.d3.c2.b3.a1": "a",
            "e.d3.c2.b3.a2": "b",
            "e.d3.c2.b3.a3": "a",
            "e.d3.c3.b1.a1": "a",
            "e.d3.c3.b1.a2": "b",
            "e.d3.c3.b1.a3": "a",
            "e.d3.c3.b2.a1": "a",
            "e.d3.c3.b2.a2": "c",
            "e.d3.c3.b2.a3": "a",
            "e.d3.c3.b3.a1": "a",
            "e.d3.c3.b3.a2": "b",
            "e.d3.c3.b3.a3": "a",
        }

        for node in top.descendants():
            path = node.get_path()
            with self.subTest(path):
                if isinstance(node, RegNode):
                    self.assertEqual(node.get_property("desc"), expected_desc[path])
                else:
                    self.assertIsNone(node.get_property("desc"))

    def test_nested_dpa_name_generation(self):
        top = self.compile(
            ["rdl_src/nested_dpa.rdl"],
            "e"
        )

        expected_type_name = {
            "e": "e",
            "e.d1": "d",
            "e.d1.c1": "c",
            "e.d1.c1.b1": "b",
            "e.d1.c1.b1.a1": "a",
            "e.d1.c1.b1.a2": "a_desc_92eb5ffe",
            "e.d1.c1.b1.a3": "a",
            "e.d1.c1.b2": "b_a2_bf2a9099",
            "e.d1.c1.b2.a1": "a",
            "e.d1.c1.b2.a2": "a_desc_4a8a08f0",
            "e.d1.c1.b2.a3": "a",
            "e.d1.c1.b3": "b",
            "e.d1.c1.b3.a1": "a",
            "e.d1.c1.b3.a2": "a_desc_92eb5ffe",
            "e.d1.c1.b3.a3": "a",
            "e.d1.c2": "c_b2_e212e497",
            "e.d1.c2.b1": "b",
            "e.d1.c2.b1.a1": "a",
            "e.d1.c2.b1.a2": "a_desc_92eb5ffe",
            "e.d1.c2.b1.a3": "a",
            "e.d1.c2.b2": "b_a2_19613f6e",
            "e.d1.c2.b2.a1": "a",
            "e.d1.c2.b2.a2": "a_desc_8277e091",
            "e.d1.c2.b2.a3": "a",
            "e.d1.c2.b3": "b",
            "e.d1.c2.b3.a1": "a",
            "e.d1.c2.b3.a2": "a_desc_92eb5ffe",
            "e.d1.c2.b3.a3": "a",
            "e.d1.c3": "c",
            "e.d1.c3.b1": "b",
            "e.d1.c3.b1.a1": "a",
            "e.d1.c3.b1.a2": "a_desc_92eb5ffe",
            "e.d1.c3.b1.a3": "a",
            "e.d1.c3.b2": "b_a2_bf2a9099",
            "e.d1.c3.b2.a1": "a",
            "e.d1.c3.b2.a2": "a_desc_4a8a08f0",
            "e.d1.c3.b2.a3": "a",
            "e.d1.c3.b3": "b",
            "e.d1.c3.b3.a1": "a",
            "e.d1.c3.b3.a2": "a_desc_92eb5ffe",
            "e.d1.c3.b3.a3": "a",
            "e.d2": "d_c2_d5559644",
            "e.d2.c1": "c",
            "e.d2.c1.b1": "b",
            "e.d2.c1.b1.a1": "a",
            "e.d2.c1.b1.a2": "a_desc_92eb5ffe",
            "e.d2.c1.b1.a3": "a",
            "e.d2.c1.b2": "b_a2_bf2a9099",
            "e.d2.c1.b2.a1": "a",
            "e.d2.c1.b2.a2": "a_desc_4a8a08f0",
            "e.d2.c1.b2.a3": "a",
            "e.d2.c1.b3": "b",
            "e.d2.c1.b3.a1": "a",
            "e.d2.c1.b3.a2": "a_desc_92eb5ffe",
            "e.d2.c1.b3.a3": "a",
            "e.d2.c2": "c_b2_429ab215",
            "e.d2.c2.b1": "b",
            "e.d2.c2.b1.a1": "a",
            "e.d2.c2.b1.a2": "a_desc_92eb5ffe",
            "e.d2.c2.b1.a3": "a",
            "e.d2.c2.b2": "b_a2_81d01098",
            "e.d2.c2.b2.a1": "a",
            "e.d2.c2.b2.a2": "a_desc_e1671797",
            "e.d2.c2.b2.a3": "a",
            "e.d2.c2.b3": "b",
            "e.d2.c2.b3.a1": "a",
            "e.d2.c2.b3.a2": "a_desc_92eb5ffe",
            "e.d2.c2.b3.a3": "a",
            "e.d2.c3": "c",
            "e.d2.c3.b1": "b",
            "e.d2.c3.b1.a1": "a",
            "e.d2.c3.b1.a2": "a_desc_92eb5ffe",
            "e.d2.c3.b1.a3": "a",
            "e.d2.c3.b2": "b_a2_bf2a9099",
            "e.d2.c3.b2.a1": "a",
            "e.d2.c3.b2.a2": "a_desc_4a8a08f0",
            "e.d2.c3.b2.a3": "a",
            "e.d2.c3.b3": "b",
            "e.d2.c3.b3.a1": "a",
            "e.d2.c3.b3.a2": "a_desc_92eb5ffe",
            "e.d2.c3.b3.a3": "a",
            "e.d3": "d",
            "e.d3.c1": "c",
            "e.d3.c1.b1": "b",
            "e.d3.c1.b1.a1": "a",
            "e.d3.c1.b1.a2": "a_desc_92eb5ffe",
            "e.d3.c1.b1.a3": "a",
            "e.d3.c1.b2": "b_a2_bf2a9099",
            "e.d3.c1.b2.a1": "a",
            "e.d3.c1.b2.a2": "a_desc_4a8a08f0",
            "e.d3.c1.b2.a3": "a",
            "e.d3.c1.b3": "b",
            "e.d3.c1.b3.a1": "a",
            "e.d3.c1.b3.a2": "a_desc_92eb5ffe",
            "e.d3.c1.b3.a3": "a",
            "e.d3.c2": "c_b2_e212e497",
            "e.d3.c2.b1": "b",
            "e.d3.c2.b1.a1": "a",
            "e.d3.c2.b1.a2": "a_desc_92eb5ffe",
            "e.d3.c2.b1.a3": "a",
            "e.d3.c2.b2": "b_a2_19613f6e",
            "e.d3.c2.b2.a1": "a",
            "e.d3.c2.b2.a2": "a_desc_8277e091",
            "e.d3.c2.b2.a3": "a",
            "e.d3.c2.b3": "b",
            "e.d3.c2.b3.a1": "a",
            "e.d3.c2.b3.a2": "a_desc_92eb5ffe",
            "e.d3.c2.b3.a3": "a",
            "e.d3.c3": "c",
            "e.d3.c3.b1": "b",
            "e.d3.c3.b1.a1": "a",
            "e.d3.c3.b1.a2": "a_desc_92eb5ffe",
            "e.d3.c3.b1.a3": "a",
            "e.d3.c3.b2": "b_a2_bf2a9099",
            "e.d3.c3.b2.a1": "a",
            "e.d3.c3.b2.a2": "a_desc_4a8a08f0",
            "e.d3.c3.b2.a3": "a",
            "e.d3.c3.b3": "b",
            "e.d3.c3.b3.a1": "a",
            "e.d3.c3.b3.a2": "a_desc_92eb5ffe",
            "e.d3.c3.b3.a3": "a",
        }

        for node in top.descendants():
            path = node.get_path()
            with self.subTest(path):
                if not isinstance(node, FieldNode):
                    self.assertEqual(node.type_name, expected_type_name[path])

    def test_indexed_dpa_reset(self):
        top = self.compile(
            ["rdl_src/dpa_array_reset.rdl"],
            "top"
        )

        gpio_enum_pll_lock = 0xB
        gpio_enum_pll_bypass = 0xA

        resets = {}
        gpio_nodes = {}
        for node in top.descendants(unroll=True):
            if isinstance(node, RegfileNode) and node.inst_name == "GPIO":
                gpio_nodes[node.get_path()] = node
            if isinstance(node, FieldNode) and node.inst_name == "CFG":
                resets[node.get_path()] = node.get_property("reset")

        self.assertEqual(resets["top.GPIO[0].CFG.CFG"], gpio_enum_pll_lock)
        self.assertIsNone(resets["top.GPIO[1].CFG.CFG"])
        self.assertIsNone(resets["top.GPIO[2].CFG.CFG"])
        self.assertEqual(resets["top.GPIO[3].CFG.CFG"], gpio_enum_pll_bypass)

        gpio_size = gpio_nodes["top.GPIO[0]"].size
        self.assertEqual(gpio_nodes["top.GPIO[0]"].address_offset, 0)
        self.assertEqual(gpio_nodes["top.GPIO[1]"].address_offset, gpio_nodes["top.GPIO[0]"].address_offset + gpio_size)
        self.assertEqual(gpio_nodes["top.GPIO[3]"].address_offset, gpio_nodes["top.GPIO[0]"].address_offset + 3 * gpio_size)

        for path, node in gpio_nodes.items():
            with self.subTest(path=path):
                self.assertTrue(node.is_array)
                self.assertEqual(node.array_dimensions, [4])
                self.assertEqual(node.n_elements, 4)
                self.assertEqual(node.total_size, 4 * gpio_size)

        self.assertEqual(
            top.find_by_path("top.GPIO[0].CFG.CFG").type_name,
            "CFG_reset_b"
        )
        self.assertEqual(
            top.find_by_path("top.GPIO[3].CFG.CFG").type_name,
            "CFG_reset_a"
        )

    def test_indexed_dpa_reset_on_reg_array(self):
        top = self.compile(
            ["rdl_src/dpa_array_reg_reset.rdl"],
            "top"
        )

        resets = {}
        for node in top.descendants(unroll=True):
            if isinstance(node, FieldNode) and node.inst_name == "f":
                resets[node.get_path()] = (node.get_property("reset"), node.width, node.msb, node.lsb)

        self.assertEqual(resets["top.my_reg[0].f"], (None, 4, 3, 0))
        self.assertEqual(resets["top.my_reg[1].f"], (3, 4, 3, 0))
        self.assertEqual(resets["top.my_reg[2].f"], (None, 4, 3, 0))

    def test_indexed_dpa_reset_propagates_whole_array_dpa(self):
        top = self.compile(
            ["rdl_src/dpa_array_reset_propagate.rdl"],
            "top"
        )

        names = {}
        for node in top.descendants(unroll=True):
            if isinstance(node, FieldNode) and node.inst_name == "f":
                names[node.get_path()] = node.get_property("name")

        self.assertEqual(names["top.rf[0].r1.f"], "SHARED")
        self.assertEqual(names["top.rf[1].r1.f"], "SHARED")
        self.assertEqual(names["top.rf[2].r1.f"], "SHARED")
        self.assertEqual(names["top.rf[3].r1.f"], "SHARED")

    def test_indexed_dpa_reset_rejects_non_reset(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_dpa_array_non_reset.rdl"],
            "top",
            "Use of array suffixes in dynamic property assignments is only supported for the 'reset' property"
        )

    def test_indexed_dpa_reset_rejects_oob_index(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_dpa_array_oob.rdl"],
            "top",
            "Array index '4' is out of range"
        )

    def test_indexed_dpa_reset_rejects_multi_suffix(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_dpa_array_multi_suffix.rdl"],
            "top",
            "Multiple array suffixes in a dynamic property assignment reference are not supported"
        )

    def test_indexed_dpa_reset_rejects_dim_mismatch(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_dpa_array_dim_mismatch.rdl"],
            "top",
            "Incompatible number of index dimensions"
        )

    def test_indexed_dpa_reset_rejects_invalid_reset(self):
        self.assertRDLCompileError(
            ["rdl_err_src/err_dpa_array_reset_oob.rdl"],
            "top",
            "cannot fit within its width"
        )

    def test_indexed_dpa_reset_parameterized_array(self):
        top = self.compile(
            ["rdl_src/dpa_array_reset_param.rdl"],
            "top"
        )

        resets = {}
        for node in top.descendants(unroll=True):
            if isinstance(node, FieldNode) and node.inst_name == "f":
                resets[node.get_path()] = node.get_property("reset")

        self.assertEqual(resets["top.my_reg[6].f"], 1)
        self.assertIsNone(resets["top.my_reg[0].f"])

    def test_indexed_dpa_reset_many_elements(self):
        top = self.compile(
            ["rdl_src/dpa_array_reset_many.rdl"],
            "top"
        )

        resets = {}
        for node in top.descendants(unroll=True):
            if isinstance(node, FieldNode) and node.inst_name == "f":
                resets[node.get_path()] = node.get_property("reset")

        for i in range(32):
            self.assertEqual(resets[f"top.my_reg[{i}].f"], i)

        my_reg = top.find_by_path("top.my_reg")
        self.assertIsNotNone(my_reg.inst.array_element_overrides)
        for elem_inst in my_reg.inst.array_element_overrides.values():
            self.assertIsNone(elem_inst.array_element_overrides)
            self.assertIsNone(elem_inst.array_element_override_pending)
            self.assertEqual(elem_inst.array_dimensions, [32])
