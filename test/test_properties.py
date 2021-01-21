
from unittest_utils import RDLSourceTestCase

class TestProperties(RDLSourceTestCase):

    def test_donttest(self):
        root = self.compile(
            ["rdl_src/properties.rdl"],
            "donttest_top"
        )

        self.assertIs(root.find_by_path("donttest_top.r1.f1").get_property('donttest'), 1)
        self.assertIs(root.find_by_path("donttest_top.r1.f2").get_property('donttest'), True)
        self.assertIs(root.find_by_path("donttest_top.r1.f3").get_property('donttest'), False)
        self.assertIs(root.find_by_path("donttest_top.r1.f4").get_property('donttest'), 1)
        self.assertIs(root.find_by_path("donttest_top.r1.f5").get_property('donttest'), True)
        self.assertIs(root.find_by_path("donttest_top.r2").get_property('donttest'), False)
        self.assertIs(root.find_by_path("donttest_top.r3").get_property('donttest'), True)
        self.assertIs(root.find_by_path("donttest_top.r4").get_property('donttest'), True)
        self.assertIs(root.find_by_path("donttest_top.r5").get_property('donttest'), False)

    def test_dontcompare(self):
        root = self.compile(
            ["rdl_src/properties.rdl"],
            "dontcompare_top"
        )

        self.assertIs(root.find_by_path("dontcompare_top.r1.f1").get_property('dontcompare'), 1)
        self.assertIs(root.find_by_path("dontcompare_top.r1.f2").get_property('dontcompare'), True)
        self.assertIs(root.find_by_path("dontcompare_top.r1.f3").get_property('dontcompare'), False)
        self.assertIs(root.find_by_path("dontcompare_top.r1.f4").get_property('dontcompare'), 1)
        self.assertIs(root.find_by_path("dontcompare_top.r1.f5").get_property('dontcompare'), True)
        self.assertIs(root.find_by_path("dontcompare_top.r2").get_property('dontcompare'), False)
        self.assertIs(root.find_by_path("dontcompare_top.r3").get_property('dontcompare'), True)
        self.assertIs(root.find_by_path("dontcompare_top.r4").get_property('dontcompare'), True)
        self.assertIs(root.find_by_path("dontcompare_top.r5").get_property('dontcompare'), False)
