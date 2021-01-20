
from unittest_utils import RDLSourceTestCase

class TestNodeUtils(RDLSourceTestCase):

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
