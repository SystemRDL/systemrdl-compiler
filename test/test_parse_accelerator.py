import os
import sys
import unittest

from systemrdl.parser import sa_systemrdl

class TestInstalled(unittest.TestCase):
    def test_installed(self):
        if sys.version_info[0:2] <= (3, 5):
            # Don't care for older versions of Python. Accelerator is no longer supported
            return

        if 'SYSTEMRDL_DISABLE_ACCELERATOR' not in os.environ:
            # Ensure that C++ accelerator installed correctly
            self.assertTrue(sa_systemrdl.USE_CPP_IMPLEMENTATION)
