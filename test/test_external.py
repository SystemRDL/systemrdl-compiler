from parameterized import parameterized_class

from unittest_utils import RDLSourceTestCase

@parameterized_class([
   {"single_elaborate_optimization": True},
   {"single_elaborate_optimization": False},
])
class TestExternal(RDLSourceTestCase):

    def test_basic(self):
        root = self.compile(
            ["rdl_src/internal_external.rdl"],
            "extern_test"
        )

        extern_map = {
            "reg1"  : True,
            "reg2"  : True,
            "reg3"  : False,
            "reg4"  : False,
            "reg5"  : False,
            "reg6"  : True,
            "reg7"  : True,
            "reg8"  : False,
            "reg9"  : True,
            "reg10" : False,
            "reg11" : True,
            "reg12" : False,
        }

        for name, external in extern_map.items():
            with self.subTest(name):
                reg = root.find_by_path("extern_test.%s" % name)
                self.assertIs(reg.external, external)

        with self.subTest("addrmap"):
            addrmap = root.find_by_path("extern_test")
            self.assertIs(addrmap.external, True)

        with self.subTest("signal"):
            signal = root.find_by_path("test_signal")
            self.assertIs(signal.external, False)


    def test_regfile(self):
        root = self.compile(
            ["rdl_src/internal_external.rdl"],
            "extern_test"
        )

        extern_map = {
            "rf1a"       : True,
            "rf1a.rega"  : True,
            "rf1a.regb"  : True,
            "rf1a.regc"  : True,
            "rf1b"       : False,
            "rf1b.rega"  : False,
            "rf1b.regb"  : False,
            "rf1b.regc"  : False,
            "rf1c"       : False,
            "rf1c.rega"  : True,
            "rf1c.regb"  : False,
            "rf1c.regc"  : False,
        }

        for name, external in extern_map.items():
            with self.subTest(name):
                reg = root.find_by_path("extern_test.%s" % name)
                self.assertIs(reg.external, external)

    def test_nested_regfile(self):
        root = self.compile(
            ["rdl_src/internal_external.rdl"],
            "extern_test"
        )

        rf1_extern_map = {
            "rf1a"       : True,
            "rf1a.rega"  : True,
            "rf1a.regb"  : True,
            "rf1a.regc"  : True,
            "rf1b"       : False,
            "rf1b.rega"  : False,
            "rf1b.regb"  : False,
            "rf1b.regc"  : False,
            "rf1c"       : False,
            "rf1c.rega"  : True,
            "rf1c.regb"  : False,
            "rf1c.regc"  : False,
        }

        for name, external in rf1_extern_map.items():
            with self.subTest("rf2a.%s" % name):
                reg = root.find_by_path("extern_test.rf2a.%s" % name)
                self.assertIs(reg.external, True)

            with self.subTest("rf2b.%s" % name):
                reg = root.find_by_path("extern_test.rf2b.%s" % name)
                self.assertIs(reg.external, False)

            with self.subTest("rf2c.%s" % name):
                reg = root.find_by_path("extern_test.rf2c.%s" % name)
                self.assertIs(reg.external, external)
