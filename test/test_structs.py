import pickle

from unittest_utils import RDLSourceTestCase
import systemrdl.rdltypes as rdlt

class TestStructs(RDLSourceTestCase):

    def test_structs(self):
        root = self.compile(
            ["rdl_src/structs.rdl"],
            "struct_test"
        )

        with self.subTest("6.3.2.2.1"):
            amap = root.find_by_path("struct_test")
            p01 = amap.get_property('p01')
            p02 = amap.get_property('p02')
            p03 = amap.get_property('p03')

            self.assertEqual(p01.type_name, "base_struct")
            self.assertEqual(set(p01.members.keys()), set(["foo"]))
            self.assertEqual(p01.foo, 1)

            self.assertEqual(p02.type_name, "derived_struct")
            self.assertEqual(set(p02.members.keys()), set(["foo", "bar"]))
            self.assertEqual(p02.foo, 0)
            self.assertEqual(p02.bar, 1234)

            self.assertEqual(p03.type_name, "final_struct")
            self.assertEqual(set(p03.members.keys()), set(["foo", "bar", "baz"]))
            self.assertEqual(p03.foo, 1)
            self.assertEqual(p03.bar, 5678)
            self.assertEqual(p03.baz, "abcde")

        with self.subTest("6.3.2.2.2-c"):
            reg = root.find_by_path("struct_test.ex1_reg")
            p01 = reg.get_property('p01')

            self.assertEqual(p01.type_name, "derived_struct")
            self.assertEqual(set(p01.members.keys()), set(["foo", "bar"]))
            self.assertEqual(p01.foo, 1)
            self.assertEqual(p01.bar, 4567)

        with self.subTest("ex1"):
            f1p1 = root.find_by_path("struct_test.ex1_reg.ex1_field1").get_property('p1')
            self.assertEqual(f1p1.type_name, "struct1")
            self.assertEqual(set(f1p1.members.keys()), set(["abool", "astring"]))
            self.assertEqual(f1p1.abool, True)
            self.assertEqual(f1p1.astring, "hello")

            f2p1 = root.find_by_path("struct_test.ex1_reg.ex1_field2").get_property('p1')
            self.assertEqual(f2p1.type_name, "struct1")
            self.assertEqual(set(f2p1.members.keys()), set(["abool", "astring"]))
            self.assertEqual(f2p1.abool, False)
            self.assertEqual(f2p1.astring, "bye")

        with self.subTest("ex2"):
            p2 = root.find_by_path("struct_test.ex2_reg.f1").get_property('p2')
            self.assertEqual(p2.type_name, "struct_composed")
            self.assertEqual(set(p2.members.keys()), set(["str", "s"]))
            self.assertEqual(p2.str, "world")

            self.assertEqual(p2.s.type_name, "struct1")
            self.assertEqual(set(p2.s.members.keys()), set(["abool", "astring"]))
            self.assertEqual(p2.s.abool, True)
            self.assertEqual(p2.s.astring, "blah")

        with self.subTest("ex3"):
            f1p3 = root.find_by_path("struct_test.ex3_reg.ex3_field1").get_property('p3')
            self.assertEqual(f1p3.type_name, "substruct")
            self.assertEqual(set(f1p3.members.keys()), set(["abool", "astring"]))
            self.assertEqual(f1p3.abool, False)
            self.assertEqual(f1p3.astring, "foo")

            f2p3 = root.find_by_path("struct_test.ex3_reg.ex3_field2").get_property('p3')
            self.assertEqual(f2p3.type_name, "substruct")
            self.assertEqual(set(f2p3.members.keys()), set(["abool", "astring"]))
            self.assertEqual(f2p3.abool, True)
            self.assertEqual(f2p3.astring, "bar")

        with self.subTest("__repr__"):
            f2p3 = root.find_by_path("struct_test.ex3_reg.ex3_field2").get_property('p3')
            self.assertRegex(str(f2p3), r"<struct 'substruct' \(astring, abool\) at 0x\w+>")


    def test_struct_compositions(self):
        root = self.compile(
            ["rdl_src/struct_compositions.rdl"],
            "top"
        )

        my_reg = root.find_by_path("top.my_reg")
        x = root.find_by_path("top.my_reg.x")

        self.assertEqual(my_reg.get_property('desc'), "hey")
        self.assertEqual(my_reg.get_property('name'), "foo")
        self.assertEqual(x.get_property('sw'), rdlt.AccessType.r)
        self.assertEqual(x.get_property('name'), "bar")
        self.assertEqual(my_reg.get_property('p_bool'), True)
        self.assertEqual(my_reg.get_property('p_int'), 61)

        p_s1 = my_reg.get_property('p_s1')
        self.assertEqual(p_s1.type_name, "s1_t")
        self.assertEqual(p_s1.members, {"bool":False, "str":"foo", "n_arr":[20,40,60,80]})


    def test_struct_pickleable(self):
        root = self.compile(
            ["rdl_src/structs.rdl"],
            "struct_test"
        )

        amap = root.find_by_path("struct_test")
        p01 = amap.get_property('p01')
        p02 = amap.get_property('p02')
        p03 = amap.get_property('p03')

        for struct in [p01, p02, p03]:
            pickled = pickle.dumps(struct)
            struct2 = pickle.loads(pickled)

            # Compare members
            self.assertEqual(struct.members, struct2.members)
            self.assertEqual(struct._is_abstract, struct2._is_abstract)
            self.assertIs(type(struct).__class__, type(struct2).__class__)
            self.assertIs(type(struct).__module__, type(struct2).__module__)

    def test_incomplete_struct(self):
        root = self.compile(
            ["rdl_src/incomplete_struct.rdl"],
            "top"
        )

        struct = root.find_by_path("top.r1.f1").get_property('struct_prop')
        self.assertEqual(struct.a, False)
        self.assertEqual(struct.b, "")
        self.assertEqual(struct.c, rdlt.AccessType.rw)
        self.assertEqual(struct.d, rdlt.AddressingType.regalign)
        self.assertEqual(struct.e, [])
