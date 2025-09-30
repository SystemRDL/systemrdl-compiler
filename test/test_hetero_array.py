from absl.testing import flagsaver
from unittest_utils import RDLSourceTestCase

class TestHeteroArray(RDLSourceTestCase):
    """Test hetero arrays."""

    maxDiff = None  # pylint: disable=invalid-name

    @flagsaver.flagsaver(experimental_hetero_arrays=False)
    def test_disabled(self):
        self.assertRDLCompileError(
                ['rdl_err_src/hetero_array.rdl'],
                None,
                'Use of array suffixes in dynamic property assignments is not'
                ' supported',
        )
