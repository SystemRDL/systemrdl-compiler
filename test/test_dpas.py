from parameterized import parameterized_class

from systemrdl.node import RegNode, FieldNode
from unittest_utils import RDLSourceTestCase

@parameterized_class([
   {"single_elaborate_optimization": True},
   {"single_elaborate_optimization": False},
])
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

        expeted_desc = {
            "e.d1.c1.b1.a1": "a",
            "e.d1.c1.b1.a2": "b",
            "e.d1.c1.b2.a1": "a",
            "e.d1.c1.b2.a2": "c",
            "e.d1.c2.b1.a1": "a",
            "e.d1.c2.b1.a2": "b",
            "e.d1.c2.b2.a1": "a",
            "e.d1.c2.b2.a2": "d",
            "e.d2.c1.b1.a1": "a",
            "e.d2.c1.b1.a2": "b",
            "e.d2.c1.b2.a1": "a",
            "e.d2.c1.b2.a2": "c",
            "e.d2.c2.b1.a1": "a",
            "e.d2.c2.b1.a2": "b",
            "e.d2.c2.b2.a1": "a",
            "e.d2.c2.b2.a2": "e",
        }

        for node in top.descendants():
            path = node.get_path()
            with self.subTest(path):
                if isinstance(node, RegNode):
                    self.assertEqual(node.get_property("desc"), expeted_desc[path])
                else:
                    self.assertIsNone(node.get_property("desc"))


        expected_type_name = {
            "e": "e",
            "e.d1": "d",
            "e.d1.c1": "c",
            "e.d1.c1.b1": "b",
            "e.d1.c1.b1.a1": "a",
            "e.d1.c1.b1.a2": "a_desc_92eb5ffe",
            "e.d1.c1.b2": "b_a2_bf2a9099",
            "e.d1.c1.b2.a1": "a",
            "e.d1.c1.b2.a2": "a_desc_4a8a08f0",
            "e.d1.c2": "c_b2_e212e497",
            "e.d1.c2.b1": "b",
            "e.d1.c2.b1.a1": "a",
            "e.d1.c2.b1.a2": "a_desc_92eb5ffe",
            "e.d1.c2.b2": "b_a2_19613f6e",
            "e.d1.c2.b2.a1": "a",
            "e.d1.c2.b2.a2": "a_desc_8277e091",
            "e.d2": "d_c2_d5559644",
            "e.d2.c1": "c",
            "e.d2.c1.b1": "b",
            "e.d2.c1.b1.a1": "a",
            "e.d2.c1.b1.a2": "a_desc_92eb5ffe",
            "e.d2.c1.b2": "b_a2_bf2a9099",
            "e.d2.c1.b2.a1": "a",
            "e.d2.c1.b2.a2": "a_desc_4a8a08f0",
            "e.d2.c2": "c_b2_429ab215",
            "e.d2.c2.b1": "b",
            "e.d2.c2.b1.a1": "a",
            "e.d2.c2.b1.a2": "a_desc_92eb5ffe",
            "e.d2.c2.b2": "b_a2_81d01098",
            "e.d2.c2.b2.a1": "a",
            "e.d2.c2.b2.a2": "a_desc_e1671797",
        }

        for node in top.descendants():
            path = node.get_path()
            with self.subTest(path):
                if not isinstance(node, FieldNode):
                    print(path)
                    self.assertEqual(node.type_name, expected_type_name[path])
