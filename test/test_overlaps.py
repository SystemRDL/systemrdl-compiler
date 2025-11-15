from systemrdl.node import RegNode, FieldNode

from unittest_utils import RDLSourceTestCase

class TestOverlaps(RDLSourceTestCase):

    def test_reg_overlaps(self):
        root = self.compile(
            ["rdl_src/overlaps.rdl"],
            "top"
        )
        top = root.top

        r0_ro: RegNode = top.get_child_by_name("r0_ro")
        r0_wo: RegNode = top.get_child_by_name("r0_wo")
        r1_ro: RegNode = top.get_child_by_name("r1_ro")
        r1_wo: RegNode = top.get_child_by_name("r1_wo")
        r2_ro: RegNode = top.get_child_by_name("r2_ro")
        r2_wo_a: RegNode = top.get_child_by_name("r2_wo_a")
        r2_wo_b: RegNode = top.get_child_by_name("r2_wo_b")
        r2_wo_c: RegNode = top.get_child_by_name("r2_wo_c")
        r2_wo_d: RegNode = top.get_child_by_name("r2_wo_d")
        r3_ro_a: RegNode = top.get_child_by_name("r3_ro_a")
        r3_ro_b: RegNode = top.get_child_by_name("r3_ro_b")
        r3_ro_c: RegNode = top.get_child_by_name("r3_ro_c")
        r3_ro_d: RegNode = top.get_child_by_name("r3_ro_d")
        r3_wo: RegNode = top.get_child_by_name("r3_wo")
        r4: RegNode = top.get_child_by_name("r4")

        self.assertTrue(r0_ro.has_overlaps)
        self.assertTrue(r0_wo.has_overlaps)
        self.assertListEqual(r0_ro.overlapping_regs, [r0_wo])
        self.assertListEqual(r0_wo.overlapping_regs, [r0_ro])

        self.assertTrue(r1_ro.has_overlaps)
        self.assertTrue(r1_wo.has_overlaps)
        self.assertListEqual(r1_ro.overlapping_regs, [r1_wo])
        self.assertListEqual(r1_wo.overlapping_regs, [r1_ro])

        self.assertTrue(r2_ro.has_overlaps)
        self.assertTrue(r2_wo_a.has_overlaps)
        self.assertTrue(r2_wo_b.has_overlaps)
        self.assertTrue(r2_wo_c.has_overlaps)
        self.assertTrue(r2_wo_d.has_overlaps)
        self.assertListEqual(r2_ro.overlapping_regs, [
            r2_wo_a,
            r2_wo_b,
            r2_wo_c,
            r2_wo_d,
        ])
        self.assertListEqual(r2_wo_a.overlapping_regs, [r2_ro])
        self.assertListEqual(r2_wo_b.overlapping_regs, [r2_ro])
        self.assertListEqual(r2_wo_c.overlapping_regs, [r2_ro])
        self.assertListEqual(r2_wo_d.overlapping_regs, [r2_ro])

        self.assertTrue(r3_ro_a.has_overlaps)
        self.assertTrue(r3_ro_b.has_overlaps)
        self.assertTrue(r3_ro_c.has_overlaps)
        self.assertTrue(r3_ro_d.has_overlaps)
        self.assertTrue(r3_wo.has_overlaps)
        self.assertListEqual(r3_ro_a.overlapping_regs, [r3_wo])
        self.assertListEqual(r3_ro_b.overlapping_regs, [r3_wo])
        self.assertListEqual(r3_ro_c.overlapping_regs, [r3_wo])
        self.assertListEqual(r3_ro_d.overlapping_regs, [r3_wo])
        self.assertListEqual(r3_wo.overlapping_regs, [
            r3_ro_a,
            r3_ro_b,
            r3_ro_c,
            r3_ro_d,
        ])

        self.assertFalse(r4.has_overlaps)
        self.assertListEqual(r4.overlapping_regs, [])


    def test_field_overlaps(self):
        root = self.compile(
            ["rdl_src/overlaps.rdl"],
            "top"
        )
        top = root.top

        with self.subTest("simple"):
            f_ro: FieldNode = top.find_by_path("simple_overlap.f_ro")
            f_wo: FieldNode = top.find_by_path("simple_overlap.f_wo")
            self.assertTrue(f_ro.has_overlaps)
            self.assertTrue(f_wo.has_overlaps)
            self.assertListEqual(f_ro.overlapping_fields, [f_wo])
            self.assertListEqual(f_wo.overlapping_fields, [f_ro])

        with self.subTest("offset"):
            f_ro = top.find_by_path("offset_overlap.f_ro")
            f_wo = top.find_by_path("offset_overlap.f_wo")
            self.assertTrue(f_ro.has_overlaps)
            self.assertTrue(f_wo.has_overlaps)
            self.assertListEqual(f_ro.overlapping_fields, [f_wo])
            self.assertListEqual(f_wo.overlapping_fields, [f_ro])

        with self.subTest("wide_narrow"):
            f_ro: FieldNode = top.find_by_path("wide_narrow_overlap.f_ro")
            f_wo_a: FieldNode = top.find_by_path("wide_narrow_overlap.f_wo_a")
            f_wo_b: FieldNode = top.find_by_path("wide_narrow_overlap.f_wo_b")
            f_wo_c: FieldNode = top.find_by_path("wide_narrow_overlap.f_wo_c")
            f_wo_d: FieldNode = top.find_by_path("wide_narrow_overlap.f_wo_d")

            self.assertTrue(f_ro.has_overlaps)
            self.assertTrue(f_wo_a.has_overlaps)
            self.assertTrue(f_wo_b.has_overlaps)
            self.assertTrue(f_wo_c.has_overlaps)
            self.assertTrue(f_wo_d.has_overlaps)
            self.assertListEqual(f_ro.overlapping_fields, [
                f_wo_a,
                f_wo_b,
                f_wo_c,
                f_wo_d,
            ])
            self.assertListEqual(f_wo_a.overlapping_fields, [f_ro])
            self.assertListEqual(f_wo_b.overlapping_fields, [f_ro])
            self.assertListEqual(f_wo_c.overlapping_fields, [f_ro])
            self.assertListEqual(f_wo_d.overlapping_fields, [f_ro])

        with self.subTest("narrow_wide"):
            f_ro_a: FieldNode = top.find_by_path("narrow_wide_overlap.f_ro_a")
            f_ro_b: FieldNode = top.find_by_path("narrow_wide_overlap.f_ro_b")
            f_ro_c: FieldNode = top.find_by_path("narrow_wide_overlap.f_ro_c")
            f_ro_d: FieldNode = top.find_by_path("narrow_wide_overlap.f_ro_d")
            f_wo: FieldNode = top.find_by_path("narrow_wide_overlap.f_wo")

            self.assertTrue(f_ro_a.has_overlaps)
            self.assertTrue(f_ro_b.has_overlaps)
            self.assertTrue(f_ro_c.has_overlaps)
            self.assertTrue(f_ro_d.has_overlaps)
            self.assertTrue(f_wo.has_overlaps)
            self.assertListEqual(f_ro_a.overlapping_fields, [f_wo])
            self.assertListEqual(f_ro_b.overlapping_fields, [f_wo])
            self.assertListEqual(f_ro_c.overlapping_fields, [f_wo])
            self.assertListEqual(f_ro_d.overlapping_fields, [f_wo])
            self.assertListEqual(f_wo.overlapping_fields, [
                f_ro_a,
                f_ro_b,
                f_ro_c,
                f_ro_d,
            ])

        with self.subTest("no overlap"):
            f1: FieldNode = top.find_by_path("r4.f1")
            f2: FieldNode = top.find_by_path("r4.f2")

            self.assertFalse(f1.has_overlaps)
            self.assertFalse(f2.has_overlaps)
            self.assertListEqual(f1.overlapping_fields, [])
            self.assertListEqual(f2.overlapping_fields, [])
