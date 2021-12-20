
from unittest_utils import RDLSourceTestCase

class TestReferences(RDLSourceTestCase):

    def test_bad_traversal(self):
        root = self.compile(
            ["rdl_src/references_direct_lhs.rdl"],
            "top"
        )

        with self.assertRaises(ValueError):
            root.find_by_path("top.[[]")
        with self.assertRaises(IndexError):
            root.find_by_path("top.reg1[1]")
        with self.assertRaises(IndexError):
            root.find_by_path("top.reg2[100]")
        with self.assertRaises(IndexError):
            root.find_by_path("top.reg2[1][1][1]")
        with self.assertRaises(IndexError):
            root.find_by_path("top.reg1.x[2]")

        self.assertIsNone(root.find_by_path("top.doesntexist"))

        self.assertEqual(root.find_by_path("^"), root)

    def test_traversal(self):
        root = self.compile(
            ["rdl_src/references_direct_lhs.rdl"],
            "top"
        )

        top = root.top
        self.assertEqual(len(list(root.signals())), 1)
        self.assertEqual(len(list(top.registers())), 2)
        self.assertEqual(len(list(top.registers(unroll=True))), 3)
        self.assertEqual(len(list(root.descendants())), 10)
        self.assertEqual(len(list(root.descendants(unroll=True))), 14)

    def test_direct_lhs_refs(self):
        root = self.compile(
            ["rdl_src/references_direct_lhs.rdl"],
            "top"
        )

        glbl_sig      = root.find_by_path("glbl_sig")
        top           = root.find_by_path("top")
        top_reg1      = root.find_by_path("top.reg1")
        top_reg1_sig  = root.find_by_path("top.reg1.sig")
        top_reg1_x    = root.find_by_path("top.reg1.x")
        top_reg1_y    = root.find_by_path("top.reg1.y")
        top_reg20     = root.find_by_path("top.reg2[0]")
        top_reg20_sig = root.find_by_path("top.reg2[0].sig")
        top_reg20_x   = root.find_by_path("top.reg2[0].x")
        top_reg20_y   = root.find_by_path("top.reg2[0].y")
        top_reg21     = root.find_by_path("top.reg2[1]")
        top_reg21_sig = root.find_by_path("top.reg2[1].sig")
        top_reg21_x   = root.find_by_path("top.reg2[1].x")
        top_reg21_y   = root.find_by_path("top.reg2[1].y")

        with self.subTest("bad lookup"):
            with self.assertRaises(LookupError):
                top.get_property('thisisnotaprop')
            with self.assertRaises(LookupError):
                top.get_property('sw')
            with self.assertRaises(TypeError):
                top.get_property('sw', bad_kwarg=1234)

            self.assertEqual(top.get_property('name'), "top")
            self.assertEqual(top.get_property('name', default="NA"), "NA")

        with self.subTest("glbl_sig"):
            self.assertIs(glbl_sig.get_property('ref_prop'), None)

        with self.subTest("top"):
            self.assertEqual(top.get_property('ref_prop'), top_reg21_x)
            self.assertIs(top.get_property('ref_prop').inst, top_reg21_x.inst)


        with self.subTest("top.reg1"):
            self.assertEqual(top_reg1.get_property('ref_prop'), top_reg1_x)
            self.assertIs(top_reg1.get_property('ref_prop').inst, top_reg1_x.inst)

        with self.subTest("top.reg1.sig"):
            self.assertIs(top_reg1_sig.get_property('ref_prop'), None)

        with self.subTest("top.reg1.x"):
            self.assertEqual(top_reg1_x.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg1_x.get_property('resetsignal').inst, glbl_sig.inst)

        with self.subTest("top.reg1.y"):
            self.assertEqual(top_reg1_y.get_property('resetsignal'), top_reg1_sig)
            self.assertIs(top_reg1_y.get_property('resetsignal').inst, top_reg1_sig.inst)

        with self.subTest("top.reg2[0]"):
            self.assertEqual(top_reg20.get_property('ref_prop'), top_reg20_x)
            self.assertIs(top_reg20.get_property('ref_prop').inst, top_reg20_x.inst)

        with self.subTest("top.reg2[0].sig"):
            self.assertIs(top_reg20_sig.get_property('ref_prop'), None)

        with self.subTest("top.reg2[0].x"):
            self.assertEqual(top_reg20_x.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg20_x.get_property('resetsignal').inst, glbl_sig.inst)

        with self.subTest("top.reg2[0].y"):
            self.assertEqual(top_reg20_y.get_property('resetsignal'), top_reg20_sig)
            self.assertIs(top_reg20_y.get_property('resetsignal').inst, top_reg20_sig.inst)


        with self.subTest("top.reg2[1]"):
            self.assertEqual(top_reg21.get_property('ref_prop'), top_reg21_x)
            self.assertIs(top_reg21.get_property('ref_prop').inst, top_reg21_x.inst)

        with self.subTest("top.reg2[1].sig"):
            self.assertIs(top_reg21_sig.get_property('ref_prop'), None)

        with self.subTest("top.reg2[1].x"):
            self.assertEqual(top_reg21_x.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg21_x.get_property('resetsignal').inst, glbl_sig.inst)

        with self.subTest("top.reg2[1].y"):
            self.assertEqual(top_reg21_y.get_property('resetsignal'), top_reg21_sig)
            self.assertIs(top_reg21_y.get_property('resetsignal').inst, top_reg21_sig.inst)


    def test_dynamic_lhs_refs(self):
        root = self.compile(
            ["rdl_src/references_dynamic_lhs.rdl"],
            "top"
        )

        glbl_sig      = root.find_by_path("glbl_sig")
        top           = root.find_by_path("top")
        top_reg1      = root.find_by_path("top.reg1")
        top_reg1_sig  = root.find_by_path("top.reg1.sig")
        top_reg1_x    = root.find_by_path("top.reg1.x")
        top_reg1_y    = root.find_by_path("top.reg1.y")
        top_reg20     = root.find_by_path("top.reg2[0]")
        top_reg20_sig = root.find_by_path("top.reg2[0].sig")
        top_reg20_x   = root.find_by_path("top.reg2[0].x")
        top_reg20_y   = root.find_by_path("top.reg2[0].y")
        top_reg21     = root.find_by_path("top.reg2[1]")
        top_reg21_sig = root.find_by_path("top.reg2[1].sig")
        top_reg21_x   = root.find_by_path("top.reg2[1].x")
        top_reg21_y   = root.find_by_path("top.reg2[1].y")

        with self.subTest("glbl_sig"):
            self.assertIs(glbl_sig.get_property('ref_prop'), None)

        with self.subTest("top"):
            self.assertIs(top.get_property('ref_prop'), None)


        with self.subTest("top.reg1"):
            self.assertEqual(top_reg1.get_property('ref_prop'), top_reg20)
            self.assertIs(top_reg1.get_property('ref_prop').inst, top_reg20.inst)

        with self.subTest("top.reg1.sig"):
            self.assertIs(top_reg1_sig.get_property('ref_prop'), None)

        with self.subTest("top.reg1.x"):
            self.assertEqual(top_reg1_x.get_property('ref_prop'), top_reg1_y)
            self.assertIs(top_reg1_x.get_property('ref_prop').inst, top_reg1_y.inst)
            self.assertEqual(top_reg1_x.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg1_x.get_property('resetsignal').inst, glbl_sig.inst)
            self.assertEqual(top_reg1_x.get_property('next').name, "ored")
            self.assertEqual(top_reg1_x.get_property('next').node, top_reg20_y)

        with self.subTest("top.reg1.y"):
            self.assertEqual(top_reg1_y.get_property('ref_prop'), top_reg1_x)
            self.assertIs(top_reg1_y.get_property('ref_prop').inst, top_reg1_x.inst)
            self.assertEqual(top_reg1_y.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg1_y.get_property('resetsignal').inst, glbl_sig.inst)
            self.assertEqual(top_reg1_y.get_property('next').name, "anded")
            self.assertEqual(top_reg1_y.get_property('next').node, top_reg1_x)


        with self.subTest("top.reg2[0]"):
            self.assertEqual(top_reg20.get_property('ref_prop'), top_reg21_x)
            self.assertIs(top_reg20.get_property('ref_prop').inst, top_reg21_x.inst)

        with self.subTest("top.reg2[0].sig"):
            self.assertIs(top_reg20_sig.get_property('ref_prop'), None)

        with self.subTest("top.reg2[0].x"):
            self.assertEqual(top_reg20_x.get_property('ref_prop'), top_reg1)
            self.assertIs(top_reg20_x.get_property('ref_prop').inst, top_reg1.inst)
            self.assertEqual(top_reg20_x.get_property('resetsignal'), top_reg20_sig)
            self.assertIs(top_reg20_x.get_property('resetsignal').inst, top_reg20_sig.inst)

        with self.subTest("top.reg2[0].y"):
            self.assertEqual(top_reg20_y.get_property('ref_prop'), top_reg1_x)
            self.assertIs(top_reg20_y.get_property('ref_prop').inst, top_reg1_x.inst)
            self.assertEqual(top_reg20_y.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg20_y.get_property('resetsignal').inst, glbl_sig.inst)
            self.assertEqual(top_reg20_y.get_property('next').name, "anded")
            self.assertEqual(top_reg20_y.get_property('next').node, top_reg20_x)


        with self.subTest("top.reg2[1]"):
            self.assertEqual(top_reg21.get_property('ref_prop'), top_reg21_x)
            self.assertIs(top_reg21.get_property('ref_prop').inst, top_reg21_x.inst)

        with self.subTest("top.reg2[1].sig"):
            self.assertIs(top_reg21_sig.get_property('ref_prop'), None)

        with self.subTest("top.reg2[1].x"):
            self.assertEqual(top_reg21_x.get_property('ref_prop'), top_reg1)
            self.assertIs(top_reg21_x.get_property('ref_prop').inst, top_reg1.inst)
            self.assertEqual(top_reg21_x.get_property('resetsignal'), top_reg21_sig)
            self.assertIs(top_reg21_x.get_property('resetsignal').inst, top_reg21_sig.inst)

        with self.subTest("top.reg2[1].y"):
            self.assertEqual(top_reg21_y.get_property('ref_prop'), top_reg1_x)
            self.assertIs(top_reg21_y.get_property('ref_prop').inst, top_reg1_x.inst)
            self.assertEqual(top_reg21_y.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg21_y.get_property('resetsignal').inst, glbl_sig.inst)
            self.assertEqual(top_reg21_y.get_property('next').name, "anded")
            self.assertEqual(top_reg21_y.get_property('next').node, top_reg21_x)


    def test_default_lhs_refs(self):
        root = self.compile(
            ["rdl_src/references_default_lhs.rdl"],
            "top"
        )

        glbl_sig      = root.find_by_path("glbl_sig")
        top           = root.find_by_path("top")
        top_reg1      = root.find_by_path("top.reg1")
        top_reg1_sig  = root.find_by_path("top.reg1.sig")
        top_reg1_x    = root.find_by_path("top.reg1.x")
        top_reg1_y    = root.find_by_path("top.reg1.y")
        top_reg20     = root.find_by_path("top.reg2[0]")
        top_reg20_sig = root.find_by_path("top.reg2[0].sig")
        top_reg20_x   = root.find_by_path("top.reg2[0].x")
        top_reg20_y   = root.find_by_path("top.reg2[0].y")
        top_reg21     = root.find_by_path("top.reg2[1]")
        top_reg21_sig = root.find_by_path("top.reg2[1].sig")
        top_reg21_x   = root.find_by_path("top.reg2[1].x")
        top_reg21_y   = root.find_by_path("top.reg2[1].y")
        top_reg3      = root.find_by_path("top.reg3")
        top_reg3_z    = root.find_by_path("top.reg3.z")

        with self.subTest("glbl_sig"):
            self.assertIs(glbl_sig.get_property('ref_prop'), None)

        with self.subTest("top"):
            self.assertIs(top.get_property('ref_prop'), None)


        with self.subTest("top.reg1"):
            self.assertIs(top_reg1.get_property('ref_prop'), None)

        with self.subTest("top.reg1.sig"):
            self.assertIs(top_reg1_sig.get_property('ref_prop'), None)

        with self.subTest("top.reg1.x"):
            self.assertIs(top_reg1_x.get_property('ref_prop'), None)
            self.assertEqual(top_reg1_x.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg1_x.get_property('resetsignal').inst, glbl_sig.inst)

        with self.subTest("top.reg1.y"):
            self.assertEqual(top_reg1_y.get_property('ref_prop'), top_reg1_x)
            self.assertIs(top_reg1_y.get_property('ref_prop').inst, top_reg1_x.inst)
            self.assertEqual(top_reg1_y.get_property('resetsignal'), top_reg1_sig)
            self.assertIs(top_reg1_y.get_property('resetsignal').inst, top_reg1_sig.inst)
            self.assertEqual(top_reg1_y.get_property('next').name, "anded")
            self.assertEqual(top_reg1_y.get_property('next').node, top_reg1_x)


        with self.subTest("top.reg2[0]"):
            self.assertIs(top_reg20.get_property('ref_prop'), None)

        with self.subTest("top.reg2[0].sig"):
            self.assertIs(top_reg20_sig.get_property('ref_prop'), None)

        with self.subTest("top.reg2[0].x"):
            self.assertIs(top_reg20_x.get_property('ref_prop'), None)
            self.assertEqual(top_reg20_x.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg20_x.get_property('resetsignal').inst, glbl_sig.inst)

        with self.subTest("top.reg2[0].y"):
            self.assertEqual(top_reg20_y.get_property('ref_prop'), top_reg20_x)
            self.assertIs(top_reg20_y.get_property('ref_prop').inst, top_reg20_x.inst)
            self.assertEqual(top_reg20_y.get_property('resetsignal'), top_reg20_sig)
            self.assertIs(top_reg20_y.get_property('resetsignal').inst, top_reg20_sig.inst)
            self.assertEqual(top_reg20_y.get_property('next').name, "anded")
            self.assertEqual(top_reg20_y.get_property('next').node, top_reg20_x)


        with self.subTest("top.reg2[1]"):
            self.assertIs(top_reg21.get_property('ref_prop'), None)

        with self.subTest("top.reg2[1].sig"):
            self.assertIs(top_reg21_sig.get_property('ref_prop'), None)

        with self.subTest("top.reg2[1].x"):
            self.assertIs(top_reg21_x.get_property('ref_prop'), None)
            self.assertEqual(top_reg21_x.get_property('resetsignal'), glbl_sig)
            self.assertIs(top_reg21_x.get_property('resetsignal').inst, glbl_sig.inst)

        with self.subTest("top.reg2[1].y"):
            self.assertEqual(top_reg21_y.get_property('ref_prop'), top_reg21_x)
            self.assertIs(top_reg21_y.get_property('ref_prop').inst, top_reg21_x.inst)
            self.assertEqual(top_reg21_y.get_property('resetsignal'), top_reg21_sig)
            self.assertIs(top_reg21_y.get_property('resetsignal').inst, top_reg21_sig.inst)
            self.assertEqual(top_reg21_y.get_property('next').name, "anded")
            self.assertEqual(top_reg21_y.get_property('next').node, top_reg21_x)


        with self.subTest("top.reg3"):
            self.assertEqual(top_reg3.get_property('ref_prop'), top_reg1)
            self.assertIs(top_reg3.get_property('ref_prop').inst, top_reg1.inst)

        with self.subTest("top.reg3.z"):
            self.assertEqual(top_reg3_z.get_property('ref_prop'), top_reg1)
            self.assertIs(top_reg3_z.get_property('ref_prop').inst, top_reg1.inst)
            self.assertEqual(top_reg3_z.get_property('resetsignal'), top_reg21_sig)
            self.assertIs(top_reg3_z.get_property('resetsignal').inst, top_reg21_sig.inst)
            self.assertEqual(top_reg3_z.get_property('next').name, "ored")
            self.assertEqual(top_reg3_z.get_property('next').node, top_reg20_y)

    def test_signal_dpa(self):
        root = self.compile(
            ["rdl_src/signal_scope.rdl"],
            "top"
        )

        my_signal = root.find_by_path("top.my_signal")
        b = root.find_by_path("top.a.b")
        my_signal_via_prop = b.get_property('resetsignal')

        self.assertEqual(my_signal, my_signal_via_prop)

        self.assertEqual(
            my_signal.get_property('name'),
            my_signal_via_prop.get_property('name')
        )
        self.assertEqual(my_signal.get_property('name'), "override")
