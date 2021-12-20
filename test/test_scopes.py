
from unittest_utils import RDLSourceTestCase

class TestScopes(RDLSourceTestCase):

    def test_scopes(self):
        root = self.compile(
            ["rdl_src/scopes.rdl"],
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

        r1f1_enum = root.find_by_path("scope_test.r1.f1").get_property('encode')
        r1f2_enum = root.find_by_path("scope_test.r1.f2").get_property('encode')
        r1f3_enum = root.find_by_path("scope_test.r1.f3").get_property('encode')
        r2f1_enum = root.find_by_path("scope_test.r2.f1").get_property('encode')
        r2f2_enum = root.find_by_path("scope_test.r2.f2").get_property('encode')

        self.assertEqual(r1f1_enum.get_scope_path(), "root_reg_t::f1")
        self.assertEqual(r1f2_enum.get_scope_path(), "")
        self.assertEqual(r1f3_enum.get_scope_path(), "root_reg_t")
        self.assertEqual(r2f1_enum.get_scope_path(), "scope_test::r2_t::f1")
        self.assertEqual(r2f2_enum.get_scope_path(), "")

    def test_struct_scopes(self):
        root = self.compile(
            ["rdl_src/structs.rdl"],
            "struct_test"
        )

        amap = root.find_by_path("struct_test")
        p01 = amap.get_property('p01')
        self.assertEqual(p01.get_scope_path(), "")

        f1 = root.find_by_path("struct_test.ex2_reg.f1")
        p2 = f1.get_property('p2')
        self.assertEqual(p2.get_scope_path(), "ex2_reg_t")

        f1 = root.find_by_path("struct_test.ex3_reg.ex3_field2")
        p2 = f1.get_property('p2')
        self.assertEqual(p2.get_scope_path(), "struct_test::ex3_reg::ex3_field2")
