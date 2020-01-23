from unittest_utils import RDLSourceTestCase
import systemrdl.rdltypes as rdlt

class TestMiscExamples(RDLSourceTestCase):
    def test_resetsignal_example(self):
        top = self.compile(
            ["rdl_testcases/signals_and_reset.rdl"],
            "top"
        )
        # TODO: Is there something to validate in this example?

    def test_pci_reset_example(self):
        top = self.compile(
            ["rdl_testcases/signals_and_reset.rdl"],
            "top2"
        )
        # TODO: Is there something to validate in this example?
    
    def test_counter_examples(self):
        top = self.compile(
            ["rdl_testcases/counter_examples.rdl"],
            "wrapper"
        )
        # TODO: Is there something to validate in this example?
