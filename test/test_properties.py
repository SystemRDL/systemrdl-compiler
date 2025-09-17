from unittest_utils import RDLSourceTestCase

class TestProperties(RDLSourceTestCase):

    def test_donttest(self):
        root = self.compile(
            ["rdl_src/properties.rdl"],
            "donttest_top"
        )
        top = root.top

        self.assertIs(top.find_by_path("r1.f1").get_property('donttest'), 1)
        self.assertIs(top.find_by_path("r1.f2").get_property('donttest'), True)
        self.assertIs(top.find_by_path("r1.f3").get_property('donttest'), False)
        self.assertIs(top.find_by_path("r1.f4").get_property('donttest'), 1)
        self.assertIs(top.find_by_path("r1.f5").get_property('donttest'), True)
        self.assertIs(top.find_by_path("r1.f6").get_property('donttest'), True)
        self.assertIs(top.find_by_path("r2").get_property('donttest'), False)
        self.assertIs(top.find_by_path("r3").get_property('donttest'), True)
        self.assertIs(top.find_by_path("r4").get_property('donttest'), True)
        self.assertIs(top.find_by_path("r5").get_property('donttest'), False)
        self.assertIs(top.find_by_path("r6").get_property('donttest'), True)

    def test_dontcompare(self):
        root = self.compile(
            ["rdl_src/properties.rdl"],
            "dontcompare_top"
        )
        top = root.top

        self.assertIs(top.find_by_path("r1.f1").get_property('dontcompare'), 1)
        self.assertIs(top.find_by_path("r1.f2").get_property('dontcompare'), True)
        self.assertIs(top.find_by_path("r1.f3").get_property('dontcompare'), False)
        self.assertIs(top.find_by_path("r1.f4").get_property('dontcompare'), 1)
        self.assertIs(top.find_by_path("r1.f5").get_property('dontcompare'), True)
        self.assertIs(top.find_by_path("r1.f6").get_property('dontcompare'), True)
        self.assertIs(top.find_by_path("r2").get_property('dontcompare'), False)
        self.assertIs(top.find_by_path("r3").get_property('dontcompare'), True)
        self.assertIs(top.find_by_path("r4").get_property('dontcompare'), True)
        self.assertIs(top.find_by_path("r5").get_property('dontcompare'), False)
        self.assertIs(top.find_by_path("r6").get_property('dontcompare'), True)

    def test_misc(self):
        root = self.compile(
            ["rdl_src/properties.rdl"],
            "misc"
        )
        top = root.top

        self.assertIs(top.find_by_path("r1").get_property('errextbus'), True)
        self.assertIs(top.find_by_path("r1.f1").get_property('swwe'), False)
        self.assertEqual(top.find_by_path("r1.f2").get_property('swwe'), top.find_by_path("r1.f1"))
        self.assertEqual(top.find_by_path("r1.f3").get_property('swwel'), top.find_by_path("r1.f1"))
        self.assertEqual(top.find_by_path("r1.f4").get_property('we'), top.find_by_path("r1.f1"))
        self.assertEqual(top.find_by_path("r1.f5").get_property('wel'), top.find_by_path("r1.f1"))

        self.assertEqual(top.find_by_path("r2.f1").get_property('hwset'), True)
        self.assertEqual(top.find_by_path("r2.f1").get_property('hwmask'), top.find_by_path("r2.fx"))
        self.assertEqual(top.find_by_path("r2.f2").get_property('hwclr'), True)
        self.assertEqual(top.find_by_path("r2.f2").get_property('hwenable'), top.find_by_path("r2.fx"))

        self.assertEqual(
            top.find_by_path("r2").get_property('accesswidth'),
            top.find_by_path("r2").get_property('regwidth')
        )

        self.assertFalse(top.get_property('bridge'))


        self.assertIs(top.find_by_path("intr_reg.irq").get_property('sticky'), False)
        self.assertIs(top.find_by_path("intr_reg.irq").get_property('stickybit'), True)
        self.assertEqual(top.find_by_path("intr_reg.irq").get_property('mask'), top.find_by_path("intr_reg.f1"))
        self.assertEqual(top.find_by_path("intr_reg.irq").get_property('haltmask'), top.find_by_path("intr_reg.f2"))

        self.assertIs(top.find_by_path("intr_reg.irq2").get_property('sticky'), True)
        self.assertIs(top.find_by_path("intr_reg.irq2").get_property('stickybit'), False)

        self.assertIs(top.find_by_path("intr_reg.irq3").get_property('sticky'), False)
        self.assertIs(top.find_by_path("intr_reg.irq3").get_property('stickybit'), True)
