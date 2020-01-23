
from unittest_utils import RDLSourceTestCase

class TestScopes(RDLSourceTestCase):

    def test_scopes(self):
        root = self.compile(
            ["rdl_testcases/scopes.rdl"],
            "scope_test"
        )

        self.assertEqual(
            root.find_by_path("scope_test").inst.get_scope_path(),
            ""
        )
        self.assertEqual(
            root.find_by_path("scope_test.r1").inst.get_scope_path(),
            ""
        )
        self.assertEqual(
            root.find_by_path("scope_test.r1.f1").inst.get_scope_path(),
            "root_reg_t"
        )
        self.assertEqual(
            root.find_by_path("scope_test.r1.f2").inst.get_scope_path(),
            "root_reg_t"
        )
        self.assertEqual(
            root.find_by_path("scope_test.r2").inst.get_scope_path(),
            "scope_test"
        )
        self.assertEqual(
            root.find_by_path("scope_test.r2.f1").inst.get_scope_path(),
            "scope_test::r2_t"
        )
        self.assertEqual(
            root.find_by_path("scope_test.r2.f2").inst.get_scope_path(),
            "scope_test::r2_t"
        )

        r1f1_enum = root.find_by_path("scope_test.r1.f1").get_property("encode")
        r1f2_enum = root.find_by_path("scope_test.r1.f2").get_property("encode")
        r2f1_enum = root.find_by_path("scope_test.r2.f1").get_property("encode")
        r2f2_enum = root.find_by_path("scope_test.r2.f2").get_property("encode")

        self.assertEqual(r1f1_enum.get_scope_path(), "root_reg_t::f1")
        self.assertEqual(r1f2_enum.get_scope_path(), "")
        self.assertEqual(r2f1_enum.get_scope_path(), "scope_test::r2_t::f1")
        self.assertEqual(r2f2_enum.get_scope_path(), "")
