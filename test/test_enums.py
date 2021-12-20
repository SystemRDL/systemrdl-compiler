
from unittest_utils import RDLSourceTestCase

class TestEnums(RDLSourceTestCase):

    def test_enums(self):
        root = self.compile(
            ["rdl_src/enums.rdl"],
            "enum_test1"
        )

        f_default = root.find_by_path("enum_test1.reg1.f_default")
        f_zero = root.find_by_path("enum_test1.reg1.f_zero")
        f_one = root.find_by_path("enum_test1.reg1.f_one")
        f_three = root.find_by_path("enum_test1.reg1.f_three")
        f_four = root.find_by_path("enum_test1.reg1.f_four")
        f_five = root.find_by_path("enum_test1.reg1.f_five")
        self.assertEqual(f_default.get_property('reset'), 5)
        self.assertEqual(f_zero.get_property('reset'), 1)
        self.assertEqual(f_one.get_property('reset'), 2)
        self.assertEqual(f_three.get_property('reset'), 4)
        self.assertEqual(f_four.get_property('reset'), 5)
        self.assertEqual(f_five.get_property('reset'), 6)

        self.assertEqual(f_default.get_property('encode').five.rdl_name, "five's [b]name[/b]")
        self.assertEqual(f_default.get_property('encode').five.rdl_desc, "this is five")

        self.assertIsNone(f_default.get_property('encode').four.get_html_name())
        self.assertIsNone(f_default.get_property('encode').four.get_html_desc())

        self.assertEqual(f_default.get_property('encode').five.get_html_name(), "five's <b>name</b>")
        self.assertEqual(f_default.get_property('encode').five.get_html_desc(), "<p>this is five</p>")
