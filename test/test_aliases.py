from unittest_utils import RDLSourceTestCase

class TestAliases(RDLSourceTestCase):

    def test_basics(self):
        top = self.compile(
            ["rdl_src/alias.rdl"],
            "alias_basics"
        ).top

        primary = top.find_by_path("primary")
        primary_x = top.find_by_path("primary.x")
        primary_y = top.find_by_path("primary.y")
        alias1 = top.find_by_path("alias1")
        alias1_x = top.find_by_path("alias1.x")
        alias1_y = top.find_by_path("alias1.y")
        alias2 = top.find_by_path("alias2")
        alias2_x = top.find_by_path("alias2.x")
        alias2_y = top.find_by_path("alias2.y")
        alias3 = top.find_by_path("alias3")
        alias3_x = top.find_by_path("alias3.x")

        self.assertIsNone(top.find_by_path("alias3.y"))

        self.assertFalse(primary.external)
        self.assertFalse(primary.is_alias)
        with self.assertRaises(ValueError):
            primary.alias_primary
        self.assertTrue(primary.has_aliases)
        a_paths = [r.get_path() for r in primary.aliases()]
        self.assertEqual(len(a_paths), 3)
        self.assertIn(alias1.get_path(), a_paths)
        self.assertIn(alias2.get_path(), a_paths)
        self.assertIn(alias3.get_path(), a_paths)

        self.assertFalse(alias1.external)
        self.assertTrue(alias1.is_alias)
        self.assertEqual(alias1.alias_primary, primary)
        self.assertFalse(alias1.has_aliases)
        self.assertEqual(list(alias1.aliases()), [])

        self.assertFalse(alias2.external)
        self.assertTrue(alias2.is_alias)
        self.assertEqual(alias2.alias_primary, primary)
        self.assertFalse(alias2.has_aliases)
        self.assertEqual(list(alias2.aliases()), [])

        self.assertFalse(alias3.external)
        self.assertTrue(alias3.is_alias)
        self.assertEqual(alias3.alias_primary, primary)
        self.assertFalse(alias3.has_aliases)
        self.assertEqual(list(alias3.aliases()), [])

        self.assertFalse(primary_x.external)
        self.assertFalse(primary_x.is_alias)
        with self.assertRaises(ValueError):
            primary_x.alias_primary
        self.assertTrue(primary_x.has_aliases)
        a_paths = [r.get_path() for r in primary_x.aliases()]
        self.assertEqual(len(a_paths), 3)
        self.assertIn(alias1_x.get_path(), a_paths)
        self.assertIn(alias2_x.get_path(), a_paths)
        self.assertIn(alias3_x.get_path(), a_paths)

        self.assertFalse(primary_y.external)
        self.assertFalse(primary_y.is_alias)
        with self.assertRaises(ValueError):
            primary_y.alias_primary
        self.assertTrue(primary_y.has_aliases)
        a_paths = [r.get_path() for r in primary_y.aliases()]
        self.assertEqual(len(a_paths), 2)
        self.assertIn(alias1_y.get_path(), a_paths)
        self.assertIn(alias2_y.get_path(), a_paths)

        self.assertFalse(alias1_x.external)
        self.assertTrue(alias1_x.is_alias)
        self.assertEqual(alias1_x.alias_primary, primary_x)
        self.assertFalse(alias1_x.has_aliases)
        self.assertEqual(list(alias1_x.aliases()), [])

        self.assertFalse(alias2_x.external)
        self.assertTrue(alias2_x.is_alias)
        self.assertEqual(alias2_x.alias_primary, primary_x)
        self.assertFalse(alias2_x.has_aliases)
        self.assertEqual(list(alias2_x.aliases()), [])


        ext_primary = top.find_by_path("ext_primary")
        ext_alias1 = top.find_by_path("ext_alias1")
        ext_alias2 = top.find_by_path("ext_alias2")
        ext_alias3 = top.find_by_path("ext_alias3")
        self.assertTrue(ext_primary.external)
        self.assertTrue(ext_alias1.external)
        self.assertTrue(ext_alias2.external)
        self.assertTrue(ext_alias3.external)


        primary_array = top.find_by_path("primary_array")
        primary_array0 = top.find_by_path("primary_array[0]")
        primary_array1 = top.find_by_path("primary_array[1]")
        primary_array_x = top.find_by_path("primary_array.x")
        primary_array0_x = top.find_by_path("primary_array[0].x")
        primary_array1_x = top.find_by_path("primary_array[1].x")
        alias_array = top.find_by_path("alias_array")
        alias_array0 = top.find_by_path("alias_array[0]")
        alias_array1 = top.find_by_path("alias_array[1]")
        alias_array_x = top.find_by_path("alias_array.x")
        alias_array0_x = top.find_by_path("alias_array[0].x")
        alias_array1_x = top.find_by_path("alias_array[1].x")

        self.assertEqual(list(primary_array.aliases())[0].get_path(), "alias_basics.alias_array[]")
        self.assertEqual(list(primary_array0.aliases())[0].get_path(), "alias_basics.alias_array[0]")
        self.assertEqual(list(primary_array1.aliases())[0].get_path(), "alias_basics.alias_array[1]")

        self.assertEqual(list(primary_array_x.aliases())[0].get_path(), "alias_basics.alias_array[].x")
        self.assertEqual(list(primary_array0_x.aliases())[0].get_path(), "alias_basics.alias_array[0].x")
        self.assertEqual(list(primary_array1_x.aliases())[0].get_path(), "alias_basics.alias_array[1].x")

        self.assertEqual(alias_array.alias_primary.get_path(), "alias_basics.primary_array[]")
        self.assertEqual(alias_array0.alias_primary.get_path(), "alias_basics.primary_array[0]")
        self.assertEqual(alias_array1.alias_primary.get_path(), "alias_basics.primary_array[1]")

        self.assertEqual(alias_array_x.alias_primary.get_path(), "alias_basics.primary_array[].x")
        self.assertEqual(alias_array0_x.alias_primary.get_path(), "alias_basics.primary_array[0].x")
        self.assertEqual(alias_array1_x.alias_primary.get_path(), "alias_basics.primary_array[1].x")

    def test_mixed_access(self):
        top = self.compile(
            ["rdl_src/alias.rdl"],
            "mixed_access"
        ).top

        r1 = top.find_by_path("r1.x")
        r2 = top.find_by_path("r2.x")
        primary_x = top.find_by_path("primary.x")
        alias1_x = top.find_by_path("alias1.x")

        self.assertFalse(r1.implements_storage)
        self.assertTrue(r2.implements_storage)
        self.assertTrue(primary_x.implements_storage)
        self.assertFalse(alias1_x.implements_storage)
