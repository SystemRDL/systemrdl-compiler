
from .unittest_utils import RDLSourceTestCase

class TestReferences(RDLSourceTestCase):
    
    def test_direct_lhs_refs(self):
        root = self.compile(
            ["rdl_testcases/references_direct_lhs.rdl"],
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
            self.assertIs(glbl_sig.get_property("ref_prop"), None)
        
        with self.subTest("top"):
            self.assertEqual(top.get_property("ref_prop"), top_reg21_x)
            self.assertIs(top.get_property("ref_prop").inst, top_reg21_x.inst)
        
        
        with self.subTest("top.reg1"):
            self.assertEqual(top_reg1.get_property("ref_prop"), top_reg1_x)
            self.assertIs(top_reg1.get_property("ref_prop").inst, top_reg1_x.inst)
        
        with self.subTest("top.reg1.sig"):
            self.assertIs(top_reg1_sig.get_property("ref_prop"), None)
        
        with self.subTest("top.reg1.x"):
            self.assertEqual(top_reg1_x.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg1_x.get_property("resetsignal").inst, glbl_sig.inst)
        
        with self.subTest("top.reg1.y"):
            self.assertEqual(top_reg1_y.get_property("resetsignal"), top_reg1_sig)
            self.assertIs(top_reg1_y.get_property("resetsignal").inst, top_reg1_sig.inst)
        
        with self.subTest("top.reg2[0]"):
            self.assertEqual(top_reg20.get_property("ref_prop"), top_reg20_x)
            self.assertIs(top_reg20.get_property("ref_prop").inst, top_reg20_x.inst)
        
        with self.subTest("top.reg2[0].sig"):
            self.assertIs(top_reg20_sig.get_property("ref_prop"), None)
        
        with self.subTest("top.reg2[0].x"):
            self.assertEqual(top_reg20_x.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg20_x.get_property("resetsignal").inst, glbl_sig.inst)
        
        with self.subTest("top.reg2[0].y"):
            self.assertEqual(top_reg20_y.get_property("resetsignal"), top_reg20_sig)
            self.assertIs(top_reg20_y.get_property("resetsignal").inst, top_reg20_sig.inst)
        
        
        with self.subTest("top.reg2[1]"):
            self.assertEqual(top_reg21.get_property("ref_prop"), top_reg21_x)
            self.assertIs(top_reg21.get_property("ref_prop").inst, top_reg21_x.inst)
        
        with self.subTest("top.reg2[1].sig"):
            self.assertIs(top_reg21_sig.get_property("ref_prop"), None)
        
        with self.subTest("top.reg2[1].x"):
            self.assertEqual(top_reg21_x.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg21_x.get_property("resetsignal").inst, glbl_sig.inst)
        
        with self.subTest("top.reg2[1].y"):
            self.assertEqual(top_reg21_y.get_property("resetsignal"), top_reg21_sig)
            self.assertIs(top_reg21_y.get_property("resetsignal").inst, top_reg21_sig.inst)


    def test_dynamic_lhs_refs(self):
        root = self.compile(
            ["rdl_testcases/references_dynamic_lhs.rdl"],
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
            self.assertIs(glbl_sig.get_property("ref_prop"), None)
        
        with self.subTest("top"):
            self.assertIs(top.get_property("ref_prop"), None)
        
        
        with self.subTest("top.reg1"):
            self.assertEqual(top_reg1.get_property("ref_prop"), top_reg20)
            self.assertIs(top_reg1.get_property("ref_prop").inst, top_reg20.inst)
        
        with self.subTest("top.reg1.sig"):
            self.assertIs(top_reg1_sig.get_property("ref_prop"), None)
        
        with self.subTest("top.reg1.x"):
            self.assertEqual(top_reg1_x.get_property("ref_prop"), top_reg1_y)
            self.assertIs(top_reg1_x.get_property("ref_prop").inst, top_reg1_y.inst)
            self.assertEqual(top_reg1_x.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg1_x.get_property("resetsignal").inst, glbl_sig.inst)
        
        with self.subTest("top.reg1.y"):
            self.assertEqual(top_reg1_y.get_property("ref_prop"), top_reg1_x)
            self.assertIs(top_reg1_y.get_property("ref_prop").inst, top_reg1_x.inst)
            self.assertEqual(top_reg1_y.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg1_y.get_property("resetsignal").inst, glbl_sig.inst)
        
        
        with self.subTest("top.reg2[0]"):
            self.assertEqual(top_reg20.get_property("ref_prop"), top_reg21_x)
            self.assertIs(top_reg20.get_property("ref_prop").inst, top_reg21_x.inst)
        
        with self.subTest("top.reg2[0].sig"):
            self.assertIs(top_reg20_sig.get_property("ref_prop"), None)
        
        with self.subTest("top.reg2[0].x"):
            self.assertEqual(top_reg20_x.get_property("ref_prop"), top_reg1)
            self.assertIs(top_reg20_x.get_property("ref_prop").inst, top_reg1.inst)
            self.assertEqual(top_reg20_x.get_property("resetsignal"), top_reg20_sig)
            self.assertIs(top_reg20_x.get_property("resetsignal").inst, top_reg20_sig.inst)
        
        with self.subTest("top.reg2[0].y"):
            self.assertEqual(top_reg20_y.get_property("ref_prop"), top_reg1_x)
            self.assertIs(top_reg20_y.get_property("ref_prop").inst, top_reg1_x.inst)
            self.assertEqual(top_reg20_y.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg20_y.get_property("resetsignal").inst, glbl_sig.inst)
        
        
        with self.subTest("top.reg2[1]"):
            self.assertEqual(top_reg21.get_property("ref_prop"), top_reg21_x)
            self.assertIs(top_reg21.get_property("ref_prop").inst, top_reg21_x.inst)
        
        with self.subTest("top.reg2[1].sig"):
            self.assertIs(top_reg21_sig.get_property("ref_prop"), None)
        
        with self.subTest("top.reg2[1].x"):
            self.assertEqual(top_reg21_x.get_property("ref_prop"), top_reg1)
            self.assertIs(top_reg21_x.get_property("ref_prop").inst, top_reg1.inst)
            self.assertEqual(top_reg21_x.get_property("resetsignal"), top_reg21_sig)
            self.assertIs(top_reg21_x.get_property("resetsignal").inst, top_reg21_sig.inst)
        
        with self.subTest("top.reg2[1].y"):
            self.assertEqual(top_reg21_y.get_property("ref_prop"), top_reg1_x)
            self.assertIs(top_reg21_y.get_property("ref_prop").inst, top_reg1_x.inst)
            self.assertEqual(top_reg21_y.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg21_y.get_property("resetsignal").inst, glbl_sig.inst)
    
    
    def test_default_lhs_refs(self):
        root = self.compile(
            ["rdl_testcases/references_default_lhs.rdl"],
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
            self.assertIs(glbl_sig.get_property("ref_prop"), None)
        
        with self.subTest("top"):
            self.assertIs(top.get_property("ref_prop"), None)
        
        
        with self.subTest("top.reg1"):
            self.assertIs(top_reg1.get_property("ref_prop"), None)
        
        with self.subTest("top.reg1.sig"):
            self.assertIs(top_reg1_sig.get_property("ref_prop"), None)
        
        with self.subTest("top.reg1.x"):
            self.assertIs(top_reg1_x.get_property("ref_prop"), None)
            self.assertEqual(top_reg1_x.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg1_x.get_property("resetsignal").inst, glbl_sig.inst)
        
        with self.subTest("top.reg1.y"):
            self.assertEqual(top_reg1_y.get_property("ref_prop"), top_reg1_x)
            self.assertIs(top_reg1_y.get_property("ref_prop").inst, top_reg1_x.inst)
            self.assertEqual(top_reg1_y.get_property("resetsignal"), top_reg1_sig)
            self.assertIs(top_reg1_y.get_property("resetsignal").inst, top_reg1_sig.inst)
        
        
        with self.subTest("top.reg2[0]"):
            self.assertIs(top_reg20.get_property("ref_prop"), None)
        
        with self.subTest("top.reg2[0].sig"):
            self.assertIs(top_reg20_sig.get_property("ref_prop"), None)
        
        with self.subTest("top.reg2[0].x"):
            self.assertIs(top_reg20_x.get_property("ref_prop"), None)
            self.assertEqual(top_reg20_x.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg20_x.get_property("resetsignal").inst, glbl_sig.inst)
        
        with self.subTest("top.reg2[0].y"):
            self.assertEqual(top_reg20_y.get_property("ref_prop"), top_reg20_x)
            self.assertIs(top_reg20_y.get_property("ref_prop").inst, top_reg20_x.inst)
            self.assertEqual(top_reg20_y.get_property("resetsignal"), top_reg20_sig)
            self.assertIs(top_reg20_y.get_property("resetsignal").inst, top_reg20_sig.inst)
        
        
        with self.subTest("top.reg2[1]"):
            self.assertIs(top_reg21.get_property("ref_prop"), None)
        
        with self.subTest("top.reg2[1].sig"):
            self.assertIs(top_reg21_sig.get_property("ref_prop"), None)
        
        with self.subTest("top.reg2[1].x"):
            self.assertIs(top_reg21_x.get_property("ref_prop"), None)
            self.assertEqual(top_reg21_x.get_property("resetsignal"), glbl_sig)
            self.assertIs(top_reg21_x.get_property("resetsignal").inst, glbl_sig.inst)
        
        with self.subTest("top.reg2[1].y"):
            self.assertEqual(top_reg21_y.get_property("ref_prop"), top_reg21_x)
            self.assertIs(top_reg21_y.get_property("ref_prop").inst, top_reg21_x.inst)
            self.assertEqual(top_reg21_y.get_property("resetsignal"), top_reg21_sig)
            self.assertIs(top_reg21_y.get_property("resetsignal").inst, top_reg21_sig.inst)
        
        
        with self.subTest("top.reg3"):
            self.assertEqual(top_reg3.get_property("ref_prop"), top_reg1)
            self.assertIs(top_reg3.get_property("ref_prop").inst, top_reg1.inst)
        
        with self.subTest("top.reg3.z"):
            self.assertEqual(top_reg3_z.get_property("ref_prop"), top_reg1)
            self.assertIs(top_reg3_z.get_property("ref_prop").inst, top_reg1.inst)
            self.assertEqual(top_reg3_z.get_property("resetsignal"), top_reg21_sig)
            self.assertIs(top_reg3_z.get_property("resetsignal").inst, top_reg21_sig.inst)
