from parameterized import parameterized_class
from unittest_utils import RDLSourceTestCase

@parameterized_class([
   {"single_elaborate_optimization": True},
   {"single_elaborate_optimization": False},
])
class TestIntr(RDLSourceTestCase):

    def test_intr(self):
        top = self.compile(
            ["rdl_src/property_typecast.rdl"],
            "enum_cast"
        )

        f1 = top.find_by_path("enum_cast.r1.f1")
        f2 = top.find_by_path("enum_cast.r1.f2")
        f3 = top.find_by_path("enum_cast.r1.f3")
        f4 = top.find_by_path("enum_cast.r1.f4")

        self.assertEqual(f1.get_property('reset'), 3)
        self.assertEqual(f1.get_property('we'), True)
        self.assertEqual(f2.get_property('we'), True)
        self.assertEqual(f3.get_property('we'), False)
        self.assertEqual(f4.get_property('we'), False)
