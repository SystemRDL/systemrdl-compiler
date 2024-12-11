import os
import unittest

from systemrdl.parser import sa_systemrdl

class TestInstalled(unittest.TestCase):
    def test_installed(self):
        if 'SYSTEMRDL_DISABLE_ACCELERATOR' not in os.environ:
            # Ensure that C++ accelerator installed correctly
            self.assertTrue(sa_systemrdl.USE_CPP_IMPLEMENTATION)
