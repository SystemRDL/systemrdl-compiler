from unittest_utils import RDLSourceTestCase

class TestNodeUtils(RDLSourceTestCase):

    def test_index_tools(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )

        with self.subTest("hier.x"):
            node = top.find_by_path("hier.x")
            self.assertEqual(node.get_path(), "hier.x")
            node.clear_lineage_index()
            self.assertEqual(node.get_path(), "hier.x")
            node.zero_lineage_index()
            self.assertEqual(node.get_path(), "hier.x")

        with self.subTest("hier.y.a"):
            node = top.find_by_path("hier.y[2].a")
            self.assertEqual(node.get_path(), "hier.y[2].a[][]")
            node.zero_lineage_index()
            self.assertEqual(node.get_path(), "hier.y[0].a[0][0]")
            node.clear_lineage_index()
            self.assertEqual(node.get_path(), "hier.y[].a[][]")

    def test_rel_path(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )
        with self.subTest("descendant"):
            a = top.find_by_path("hier")
            b = top.find_by_path("hier.x.a")
            self.assertEqual(b.get_rel_path(a), "x.a[][]")

        with self.subTest("parent"):
            a = top.find_by_path("hier.x.a")
            b = top.find_by_path("hier")
            self.assertEqual(b.get_rel_path(a), "^.^")

        with self.subTest("fromroot"):
            a = top.find_by_path("hier.x.a")
            self.assertEqual(a.get_rel_path(top), "hier.x.a[][]")

        with self.subTest("updown1"):
            a = top.find_by_path("hier.x.a")
            b = top.find_by_path("hier.x.b")
            self.assertEqual(b.get_rel_path(a), "^.b[]")

        with self.subTest("updown2"):
            a = top.find_by_path("hier.x.a")
            b = top.find_by_path("hier.y[2].b[1]")
            self.assertEqual(b.get_rel_path(a), "^.^.y[2].b[1]")

        with self.subTest("self"):
            a = top.find_by_path("hier.y[0].a[1][1]")
            self.assertEqual(a.get_rel_path(a), "")

        with self.subTest("self-index1"):
            a = top.find_by_path("hier.y[0].a[1][1]")
            b = top.find_by_path("hier.y[1].a[1][1]")
            self.assertEqual(b.get_rel_path(a), "^.^.y[1].a[1][1]")

        with self.subTest("self-index2"):
            a = top.find_by_path("hier.y[0].a[1][1]")
            b = top.find_by_path("hier.y.a")
            self.assertEqual(b.get_rel_path(a), "^.^.y[].a[][]")

        with self.subTest("self-index3"):
            a = top.find_by_path("hier.y.a")
            b = top.find_by_path("hier.y.a[1][1]")
            self.assertEqual(b.get_rel_path(a), "^.a[1][1]")

    def test_address_tools(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )

        with self.subTest("hier.y[2].a"):
            node = top.find_by_path("hier.y[2].a")
            with self.assertRaises(ValueError):
                node.address_offset
            with self.assertRaises(ValueError):
                node.absolute_address
            self.assertEqual(node.raw_address_offset, 0)
            self.assertEqual(node.raw_absolute_address, 0x100)

        with self.subTest("hier.y.c[1][1]"):
            node = top.find_by_path("hier.y.c[1][1]")
            self.assertEqual(node.address_offset, 0x64 + 4*4+4)
            with self.assertRaises(ValueError):
                node.absolute_address
            self.assertEqual(node.raw_address_offset, 0x64)
            self.assertEqual(node.raw_absolute_address, 0x100 + 0x64)

    def test_class_utils(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )

        with self.subTest("__repr__"):
            node = top.find_by_path("hier.x.b.a")
            self.assertRegex(str(node), r"<FieldNode hier\.x\.b\[\]\.a at 0x\w+>")

        with self.subTest("__eq__"):
            a = top.find_by_path("hier.x.b.a")
            a2 = top.find_by_path("hier.x.b.a")
            b = top.find_by_path("hier.x.b")

            self.assertTrue(a == a2)
            self.assertFalse(a == b)
            self.assertFalse(a == 123)

    def test_iterators(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )

        with self.subTest("descendants"):
            d_paths = [n.get_path() for n in top.descendants()]
            self.assertEqual(
                d_paths,
                [
                    'hier',
                    'hier.x',
                    'hier.x.a[][]',
                    'hier.x.a[][].a',
                    'hier.x.b[]',
                    'hier.x.b[].a',
                    'hier.x.c[][]',
                    'hier.x.c[][].a',
                    'hier.y[]',
                    'hier.y[].a[][]',
                    'hier.y[].a[][].a',
                    'hier.y[].b[]',
                    'hier.y[].b[].a',
                    'hier.y[].c[][]',
                    'hier.y[].c[][].a',
                    'hier.z_mem',
                    'hier.z_mem.x[]',
                    'hier.z_mem.x[].a',
                ]
            )

        with self.subTest("descendants-post-order"):
            d_paths = [n.get_path() for n in top.descendants(in_post_order=True)]
            self.assertEqual(
                d_paths,
                [
                    'hier.x.a[][].a',
                    'hier.x.a[][]',
                    'hier.x.b[].a',
                    'hier.x.b[]',
                    'hier.x.c[][].a',
                    'hier.x.c[][]',
                    'hier.x',
                    'hier.y[].a[][].a',
                    'hier.y[].a[][]',
                    'hier.y[].b[].a',
                    'hier.y[].b[]',
                    'hier.y[].c[][].a',
                    'hier.y[].c[][]',
                    'hier.y[]',
                    'hier.z_mem.x[].a',
                    'hier.z_mem.x[]',
                    'hier.z_mem',
                    'hier',
                ]
            )

    def test_list_properties(self):
        top = self.compile(["rdl_testcases/udp_15.2.2_ex1.rdl"], None)

        with self.subTest("udps"):
            n = top.find_by_path("foo.bar.field2")

            self.assertEqual(
                sorted(n.list_properties()),
                [
                    'some_bool_p',
                    'some_num_p',
                    'sw',
                ]
            )

            self.assertEqual(
                sorted(n.list_properties(include_native=False)),
                [
                    'some_bool_p',
                    'some_num_p',
                ]
            )

            self.assertEqual(
                sorted(n.list_properties(include_udp=False)),
                [
                    'sw',
                ]
            )

        with self.subTest("all"):
            n = top.find_by_path("foo")

            self.assertEqual(
                sorted(n.list_properties(list_all=True)),
                [
                    'a_map_p',
                    'addressing',
                    'alignment',
                    'bigendian',
                    'bridge',
                    'desc',
                    'dontcompare',
                    'donttest',
                    'errextbus',
                    'hdl_path',
                    'hdl_path_gate',
                    'ispresent',
                    'littleendian',
                    'lsb0',
                    'msb0',
                    'name',
                    'rsvdset',
                    'rsvdsetX',
                    'sharedextbus',
                    'some_ref_p',
                ]
            )

            self.assertEqual(
                sorted(n.list_properties(list_all=True, include_native=False)),
                [
                    'a_map_p',
                    'some_ref_p',
                ]
            )

            self.assertEqual(
                sorted(n.list_properties(list_all=True, include_udp=False)),
                [
                    'addressing',
                    'alignment',
                    'bigendian',
                    'bridge',
                    'desc',
                    'dontcompare',
                    'donttest',
                    'errextbus',
                    'hdl_path',
                    'hdl_path_gate',
                    'ispresent',
                    'littleendian',
                    'lsb0',
                    'msb0',
                    'name',
                    'rsvdset',
                    'rsvdsetX',
                    'sharedextbus',
                ]
            )

    def test_names(self):
        top = self.compile(
            ["rdl_testcases/parameters.rdl"],
            "nested"
        )
        r1 = top.find_by_path("nested.r1_inst")
        r1_2 = top.find_by_path("nested.r1_inst2")
        f = top.find_by_path("nested.r1_inst.f")
        f2 = top.find_by_path("nested.r1_inst.f2")

        self.assertEqual(r1.inst_name, "r1_inst")
        self.assertEqual(r1.type_name, "r1_WIDTH_5")
        self.assertEqual(r1.orig_type_name, "r1")

        self.assertEqual(r1_2.inst_name, "r1_inst2")
        self.assertEqual(r1_2.type_name, "r1_WIDTH_5")
        self.assertEqual(r1_2.orig_type_name, "r1")

        self.assertEqual(f.inst_name, "f")
        self.assertEqual(f.type_name, "f")
        self.assertIsNone(f.orig_type_name)

        self.assertEqual(f2.inst_name, "f2")
        self.assertEqual(f2.type_name, "f")
        self.assertIsNone(f2.orig_type_name)


    def test_owning_addrmap(self):
        top = self.compile(
            ["rdl_testcases/references_default_lhs.rdl"],
            "top"
        )
        top_addrmap = top.find_by_path("top")
        self.assertIsNone(top.owning_addrmap)
        self.assertIsNone(top.find_by_path("glbl_sig").owning_addrmap)
        self.assertEqual(top_addrmap.owning_addrmap, top_addrmap)
        self.assertEqual(top.find_by_path("top.reg3.z").owning_addrmap, top_addrmap)


    def test_find_by_path_via_parent(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )

        a = top.find_by_path("hier.x.a")
        b = top.find_by_path("hier.y.b")
        ba = top.find_by_path("hier.y.b.a")

        self.assertEqual(top.find_by_path("hier.x.b.^.a"), a)
        self.assertEqual(ba.find_by_path("^"), b)
        self.assertEqual(ba.find_by_path("^.^.^.^.^.^.^.^.hier.y.b"), b)

    def test_typed_iterators(self):
        top = self.compile(
            ["rdl_testcases/address_packing.rdl"],
            "hier"
        )

        x = top.find_by_path("hier.x")
        a = top.find_by_path("hier.x.a")

        with self.subTest("registers"):
            paths = [n.get_path() for n in top.top.registers()]
            self.assertEqual(paths, [])

            paths = [n.get_path() for n in x.registers()]
            self.assertEqual(
                paths,
                [
                    'hier.x.a[][]',
                    'hier.x.b[]',
                    'hier.x.c[][]',
                ]
            )

        with self.subTest("registers"):
            paths = [n.get_path() for n in x.fields()]
            self.assertEqual(paths, [])

            paths = [n.get_path() for n in a.fields()]
            self.assertEqual(
                paths,
                [
                    'hier.x.a[][].a',
                ]
            )

    def test_field_prop_helpers(self):
        root = self.compile(
            ["rdl_testcases/field_access_types.rdl"],
            "top"
        )

        f1 = root.find_by_path("top.r1.f1")
        f2 = root.find_by_path("top.r1.f2")
        f3 = root.find_by_path("top.r1.f3")
        f4 = root.find_by_path("top.r1.f4")
        f5 = root.find_by_path("top.r1.f5")
        f6 = root.find_by_path("top.r1.f6")

        r1 = root.find_by_path("top.r1")
        r2 = root.find_by_path("top.r2")
        r3 = root.find_by_path("top.r3")

        self.assertFalse(f1.is_volatile)
        self.assertTrue(f2.is_volatile)
        self.assertTrue(f1.implements_storage)
        self.assertFalse(f2.implements_storage)
        self.assertTrue(f3.implements_storage)
        self.assertTrue(f4.implements_storage)
        self.assertTrue(f5.implements_storage)
        self.assertTrue(f6.implements_storage)

        self.assertTrue(r1.has_sw_writable)
        self.assertTrue(r1.has_sw_readable)

        self.assertFalse(r2.has_sw_writable)
        self.assertTrue(r2.has_sw_readable)

        self.assertTrue(r3.has_sw_writable)
        self.assertFalse(r3.has_sw_readable)
