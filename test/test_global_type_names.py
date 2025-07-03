from unittest_utils import RDLSourceTestCase

class TestGlobalTypeNames(RDLSourceTestCase):

    def test_global_type_names(self):
        root = self.compile(
            ["rdl_src/global_type_names.rdl"],
            "top"
        )
        top = root.top

        self.assertEqual(top.find_by_path("rf1").get_global_type_name("|"), "rf_global")
        self.assertEqual(top.find_by_path("rf1.r1").get_global_type_name("|"), "rf_global|r_local")
        self.assertEqual(top.find_by_path("rf1.r1.f_param").get_global_type_name("|"), "rf_global|r_local|f_param")
        self.assertEqual(top.find_by_path("rf1.r1.f_param2").get_global_type_name("|"), "rf_global|r_local|myfield_w4")
        self.assertEqual(top.find_by_path("rf1.r2").get_global_type_name("|"), "r_global")
        self.assertEqual(top.find_by_path("rf1.r2.f1").get_global_type_name("|"), "r_global|f1")
        self.assertEqual(top.find_by_path("rf1.r2.f2").get_global_type_name("|"), "r_global|myfield")
        self.assertEqual(top.find_by_path("rf1.r2.f3").get_global_type_name("|"), "r_global|myfield_w4")
        self.assertEqual(top.find_by_path("rf1.r2.f4").get_global_type_name("|"), "r_global|myfield2")

        self.assertEqual(top.find_by_path("rf2").get_global_type_name("|"), "rf_global_NUM_8")
        self.assertEqual(top.find_by_path("rf2.r1").get_global_type_name("|"), "rf_global_NUM_8|r_local")
        self.assertEqual(top.find_by_path("rf2.r1.f_param").get_global_type_name("|"), "rf_global_NUM_8|r_local|f_param")
        self.assertEqual(top.find_by_path("rf2.r1.f_param2").get_global_type_name("|"), "rf_global_NUM_8|r_local|myfield_w8")
        self.assertEqual(top.find_by_path("rf2.r2").get_global_type_name("|"), "r_global")
        self.assertEqual(top.find_by_path("rf2.r2.f1").get_global_type_name("|"), "r_global|f1")
        self.assertEqual(top.find_by_path("rf2.r2.f2").get_global_type_name("|"), "r_global|myfield")
        self.assertEqual(top.find_by_path("rf2.r2.f3").get_global_type_name("|"), "r_global|myfield_w4")
        self.assertEqual(top.find_by_path("rf2.r2.f4").get_global_type_name("|"), "r_global|myfield2")
