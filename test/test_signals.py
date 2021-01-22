
from unittest_utils import RDLSourceTestCase

class TestParameters(RDLSourceTestCase):

    def test_signalwidth(self):
        root = self.compile(["rdl_src/signals.rdl"])
        self.assertEqual(root.find_by_path("top.s1").width, 8)
