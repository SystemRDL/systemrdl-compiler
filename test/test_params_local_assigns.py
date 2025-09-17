from unittest_utils import RDLSourceTestCase

from systemrdl.node import AddrmapNode, RegfileNode, RegNode, FieldNode

class TestParamsLocalAssign(RDLSourceTestCase):

    def check_f(self, f: FieldNode, P1=None, P2=None, P3=None):
        if P1 is None:
            P1 = 1
        if P2 is None:
            P2 = 2
        if P3 is None:
            P3 = P1 + P2 + 1

        self.assertEqual(f.get_property("udp1"), P1)
        self.assertEqual(f.get_property("udp2"), P2)
        self.assertEqual(f.get_property("udp3"), P3)

    def check_r(self, r: RegNode, P1=None, P2=None, P3=None):
        if P1 is None:
            P1 = 10
        if P2 is None:
            P2 = 20
        if P3 is None:
            P3 = P2 + 10

        self.assertEqual(r.get_property("udp1"), P1)
        self.assertEqual(r.get_property("udp2"), P2)
        self.assertEqual(r.get_property("udp3"), P3)

        f0: FieldNode = r.get_child_by_name("f0")
        self.assertEqual(f0.width, 1)
        self.assertEqual(f0.get_property("reset"), 0)
        self.check_f(f0, P2=50)

        f1: FieldNode = r.get_child_by_name("f1")
        self.assertEqual(f1.width, 10)
        self.assertEqual(f1.get_property("reset"), P1)
        self.check_f(f1)

        f2: FieldNode = r.get_child_by_name("f2")
        self.assertEqual(f2.width, 10)
        self.assertEqual(f2.get_property("reset"), P2)
        self.check_f(f2, P2=5, P3=P3)

        f3: FieldNode = r.get_child_by_name("f3")
        self.assertEqual(f3.width, P3 % 9 + 1)
        self.assertEqual(f3.get_property("reset"), 0)
        self.check_f(f3)

    def check_rf(self, rf: RegfileNode, P1=None, P2=None, P3=None):
        if P1 is None:
            P1 = 0x100
        if P2 is None:
            P2 = 0x200
        if P3 is None:
            P3 = P2 + 0x100

        self.assertEqual(rf.get_property("udp1"), P1)
        self.assertEqual(rf.get_property("udp2"), P2)
        self.assertEqual(rf.get_property("udp3"), P3)

        r0: RegNode = rf.get_child_by_name("r0")
        self.assertIsNone(r0.array_dimensions)
        self.assertEqual(r0.raw_address_offset, 0)
        self.check_r(r0, P2=30)

        r1: RegNode = rf.get_child_by_name("r1")
        self.assertListEqual(r1.array_dimensions, [int(P1/0x8)])
        self.assertEqual(r1.raw_address_offset, P1)
        self.check_r(r1)

        r2: RegNode = rf.get_child_by_name("r2")
        self.assertListEqual(r2.array_dimensions, [int(P2/0x8)])
        self.assertEqual(r2.raw_address_offset, P2 + 0x1000)
        self.check_r(r2, P2=6, P3=int(P3/8))

        r3: RegNode = rf.get_child_by_name("r3")
        self.assertListEqual(r3.array_dimensions, [int(P3/0x8)])
        self.assertEqual(r3.raw_address_offset, P2 + P3)
        self.check_r(r3)

    def check_top(self, top: AddrmapNode, P1, P2, P3):
        self.assertEqual(top.get_property("udp1"), P1)
        self.assertEqual(top.get_property("udp2"), P2)
        self.assertEqual(top.get_property("udp3"), P3)

        rf0: RegfileNode = top.get_child_by_name("rf0")
        self.assertIsNone(rf0.array_dimensions)
        self.assertEqual(rf0.raw_address_offset, 0)
        self.check_rf(rf0, P2=0x180)

        rf1: RegfileNode = top.get_child_by_name("rf1")
        self.assertListEqual(rf1.array_dimensions, [int(P1/0x100)])
        self.assertEqual(rf1.raw_address_offset, P1 + 0x1000)
        self.check_rf(rf1)

        rf2: RegfileNode = top.get_child_by_name("rf2")
        self.assertListEqual(rf2.array_dimensions, [int(P2/0x100)])
        self.assertEqual(rf2.raw_address_offset, P2 + 0x80_000)
        self.check_rf(rf2, P2=0x1A0, P3=int(P3/0x80))

        rf3: RegfileNode = top.get_child_by_name("rf3")
        self.assertListEqual(rf3.array_dimensions, [int(P3/0x100)])
        self.assertEqual(rf3.raw_address_offset, P2 + P3 + 0x100_000)
        self.check_rf(rf3)


    def check_f_upref_assigns(self, f: FieldNode, TOP_PARAM, REGFILE_PARAM, REG_PARAM, FIELD_PARAM=None):
        if FIELD_PARAM is None:
            FIELD_PARAM = 4

        self.assertEqual(f.get_property("udp4"), TOP_PARAM)
        self.assertEqual(f.get_property("udp5"), REGFILE_PARAM)
        self.assertEqual(f.get_property("udp6"), REG_PARAM)
        self.assertEqual(f.get_property("udp7"), FIELD_PARAM)

    def check_r_upref_assigns(self, r: RegNode, TOP_PARAM, REGFILE_PARAM, REG_PARAM=None):
        if REG_PARAM is None:
            REG_PARAM = 3

        self.assertEqual(r.get_property("udp4"), TOP_PARAM)
        self.assertEqual(r.get_property("udp5"), REGFILE_PARAM)
        self.assertEqual(r.get_property("udp6"), REG_PARAM)

        f0: FieldNode = r.get_child_by_name("f0")
        self.check_f_upref_assigns(f0, TOP_PARAM=TOP_PARAM, REGFILE_PARAM=REGFILE_PARAM, REG_PARAM=REG_PARAM)

        f1: FieldNode = r.get_child_by_name("f1")
        self.check_f_upref_assigns(f1, TOP_PARAM=TOP_PARAM, REGFILE_PARAM=REGFILE_PARAM, REG_PARAM=REG_PARAM)

        f2: FieldNode = r.get_child_by_name("f2")
        self.check_f_upref_assigns(f2, TOP_PARAM=TOP_PARAM, REGFILE_PARAM=REGFILE_PARAM, REG_PARAM=REG_PARAM, FIELD_PARAM=40)

        f3: FieldNode = r.get_child_by_name("f3")
        self.check_f_upref_assigns(f3, TOP_PARAM=TOP_PARAM, REGFILE_PARAM=REGFILE_PARAM, REG_PARAM=REG_PARAM)


    def check_rf_upref_assigns(self, rf: RegfileNode, TOP_PARAM, REGFILE_PARAM=None):
        if REGFILE_PARAM is None:
            REGFILE_PARAM = 2

        self.assertEqual(rf.get_property("udp4"), TOP_PARAM)
        self.assertEqual(rf.get_property("udp5"), REGFILE_PARAM)

        r0: RegNode = rf.get_child_by_name("r0")
        self.check_r_upref_assigns(r0, TOP_PARAM=TOP_PARAM, REGFILE_PARAM=REGFILE_PARAM)

        r1: RegNode = rf.get_child_by_name("r1")
        self.check_r_upref_assigns(r1, TOP_PARAM=TOP_PARAM, REGFILE_PARAM=REGFILE_PARAM)

        r2: RegNode = rf.get_child_by_name("r2")
        self.check_r_upref_assigns(r2, TOP_PARAM=TOP_PARAM, REGFILE_PARAM=REGFILE_PARAM, REG_PARAM=30)

        r3: RegNode = rf.get_child_by_name("r3")
        self.check_r_upref_assigns(r3, TOP_PARAM=TOP_PARAM, REGFILE_PARAM=REGFILE_PARAM)


    def check_top_upref_assigns(self, top: AddrmapNode, TOP_PARAM=None):
        if TOP_PARAM is None:
            TOP_PARAM = 1

        self.assertEqual(top.get_property("udp4"), TOP_PARAM)

        rf0: RegfileNode = top.get_child_by_name("rf0")
        self.check_rf_upref_assigns(rf0, TOP_PARAM=TOP_PARAM)

        rf1: RegfileNode = top.get_child_by_name("rf1")
        self.check_rf_upref_assigns(rf1, TOP_PARAM=TOP_PARAM)

        rf2: RegfileNode = top.get_child_by_name("rf2")
        self.check_rf_upref_assigns(rf2, TOP_PARAM=TOP_PARAM, REGFILE_PARAM=20)

        rf3: RegfileNode = top.get_child_by_name("rf3")
        self.check_rf_upref_assigns(rf3, TOP_PARAM=TOP_PARAM)


    def test_root_decl_variant(self):
        root = self.compile(
            ["rdl_src/nested_params_root_decl.rdl"]
        )

        top = root.top
        top_P1 = 0x1000
        top_P2 = 0x2000
        top_P3 = top_P2 + 0x1000
        self.check_top(top, top_P1, top_P2, top_P3)


    def test_local_decl_variant(self):
        root = self.compile(
            ["rdl_src/nested_params_local_decl.rdl"]
        )

        top = root.top
        top_P1 = 0x1000
        top_P2 = 0x2000
        top_P3 = top_P2 + 0x1000
        self.check_top(top, top_P1, top_P2, top_P3)
        self.check_top_upref_assigns(top)
