from unittest_utils import RDLSourceTestCase

class TestMemories(RDLSourceTestCase):

    def test_basic(self):
        root = self.compile(
            ["rdl_src/memories.rdl"],
            "memories"
        )

        extern_map = {
            "mem_2_32_w": { 'entries' : 2, 'width' : 32, 'sw_access': 'w'},
            "mem_2_32_r": {'entries': 2, 'width': 32, 'sw_access': 'r'},
            "mem_2_32_rw": {'entries': 2, 'width': 32, 'sw_access': 'rw'},
            "mem_5_64_w": {'entries': 5, 'width': 64, 'sw_access': 'w'},
            "mem_5_64_r": {'entries': 5, 'width': 64, 'sw_access': 'r'},
            "mem_5_64_rw": {'entries': 5, 'width': 64, 'sw_access': 'rw'},
        }

        for name, props in extern_map.items():
            with self.subTest(name):
                mem = root.find_by_path("memories.%s" % name)
                self.assertEqual(mem.external, True)

                if props['sw_access'] == 'w':
                    self.assertEqual(mem.is_sw_readable, False)
                    self.assertEqual(mem.is_sw_writable, True)
                elif props['sw_access'] == 'r':
                    self.assertEqual(mem.is_sw_readable, True)
                    self.assertEqual(mem.is_sw_writable, False)
                elif props['sw_access'] == 'rw':
                    self.assertEqual(mem.is_sw_readable, True)
                    self.assertEqual(mem.is_sw_writable, True)
                else:
                    raise ValueError('unrecognised software access type: %s'% props['sw_access'])

                size_in_bytes = (props['width'] >> 3) * props['entries']
                self.assertEqual(mem.size, size_in_bytes)
