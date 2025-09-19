import unittest
import os

from systemrdl import RDLCompiler, FieldNode, AddressableNode
from systemrdl.importer import RDLImporter

#-------------------------------------------------------------------------------
class MyImporter(RDLImporter):
    def import_file(self, path: str) -> None:
        super().import_file(path)

        my_rf = self.create_regfile_definition("my_rf")
        self.register_root_component(my_rf)

        # reg1
        reg1 = self.instantiate_reg(self.create_reg_definition(), "reg1", 0)
        self.add_child(my_rf, reg1)

        my_field_t = self.create_field_definition("my_field_t")
        self.assign_property(my_field_t, "name", "my superb field")
        f1 = self.instantiate_field(my_field_t, "f1", 0, 8)
        self.add_child(reg1, f1)
        f2 = self.instantiate_field(my_field_t, "f2", 16, 8)
        self.add_child(reg1, f2)

        f3 = self.instantiate_field(self.create_field_definition(), "f3", 8, 8)
        self.add_child(reg1, f3)

        # reg2
        my_reg_t = self.create_reg_definition("my_reg_t")
        f1 = self.instantiate_field(my_field_t, "f1", 0, 8)
        self.add_child(my_reg_t, f1)
        f2 = self.instantiate_field(my_field_t, "f2", 8, 8)
        self.add_child(my_reg_t, f2)
        f3 = self.instantiate_field(my_field_t, "f3", 16, 8)
        self.add_child(my_reg_t, f3)

        r2 = self.instantiate_reg(my_reg_t, "r2", 0x10)
        self.add_child(my_rf, r2)
        r3 = self.instantiate_reg(my_reg_t, "r3", 0x20)
        self.add_child(my_rf, r3)


        top = self.create_addrmap_definition("top")
        self.register_root_component(top)
        sub = self.instantiate_addrmap(self.create_addrmap_definition(), "sub", 0x100)
        self.add_child(top, sub)

        my_rf = self.lookup_root_component("my_rf")
        subsub = self.instantiate_regfile(my_rf, "subsub", 0)
        self.add_child(sub, subsub)

        mem = self.create_mem_definition()
        self.assign_property(mem, "memwidth", 32)
        self.add_child(
            top,
            self.instantiate_mem(mem, "my_mem", 0x400, [2], 0x100)
        )

        mem2 = self.create_mem_definition("my_mem_t")
        self.assign_property(mem2, "memwidth", 32)
        self.add_child(
            top,
            self.instantiate_mem(
                mem2,
                "my_mem2", 0x800, [2], 0x100
            )
        )


class InstNameErrorTestcaseImporter(RDLImporter):
    def import_file(self, path: str) -> None:
        super().import_file(path)

        my_rf = self.create_regfile_definition("error_testcases")
        self.register_root_component(my_rf)

        # Creates a register instance with an illegal name.
        reg1 = self.instantiate_reg(self.create_reg_definition(),
                                    "reg1.some_signal", 0)
        self.add_child(my_rf, reg1)


class TypeNameErrorTestcaseImporter(RDLImporter):

    def import_file(self, path: str) -> None:
        super().import_file(path)

        my_rf = self.create_regfile_definition("error_testcases")
        self.register_root_component(my_rf)

        # Creates a register instance with an illegal name.
        reg_t = self.create_reg_definition("illegal.type.name")

#-------------------------------------------------------------------------------
class TypeTestImporter(RDLImporter):
    def import_file(self, path: str) -> None:
        super().import_file(path)

        top = self.create_addrmap_definition("top")
        self.register_root_component(top)

        reg = self.instantiate_reg(
            self.create_reg_definition(),
            "r",
            0x0,
        )
        self.add_child(top, reg)

        field = self.instantiate_field(
            self.create_field_definition(),
            "f",
            0,
            32,
        )
        self.add_child(reg, field)

        self.assign_property(top, "udp_string", "my string")
        self.assign_property(top, "udp_string_array", ["str1", "str2", "str3"])
        self.assign_property(top, "udp_boolean", True)
        self.assign_property(top, "udp_boolean_array", [True, False, True])
        self.assign_property(top, "udp_longint", 123)
        self.assign_property(top, "udp_longint_array", [12, 34, 56])

        self.assign_property(reg, "udp_string_array", [])
        self.assign_property(reg, "udp_boolean_array", [])
        self.assign_property(reg, "udp_longint_array", [])

#-------------------------------------------------------------------------------

class TestImporter(unittest.TestCase):
    def test_importer(self):
        rdlc = RDLCompiler()

        i = MyImporter(rdlc)
        i.import_file("asdf")
        root = rdlc.elaborate()

        nodes = []
        for node in root.descendants():
            if isinstance(node, FieldNode):
                attr = (node.low, node.high)
            elif isinstance(node, AddressableNode):
                attr = node.raw_absolute_address
            nodes.append(
                (node.get_path(), type(node).__name__, node.type_name, attr)
            )

        expected_nodes = [
            ('top', 'AddrmapNode', 'top', 0),
            ('top.sub', 'AddrmapNode', None, 0x100),
            ('top.sub.subsub', 'RegfileNode', "my_rf", 0x100),
            ('top.sub.subsub.reg1', 'RegNode', None, 0x100),
            ('top.sub.subsub.reg1.f1', 'FieldNode', 'my_field_t', (0, 7)),
            ('top.sub.subsub.reg1.f3', 'FieldNode', None, (8, 15)),
            ('top.sub.subsub.reg1.f2', 'FieldNode', 'my_field_t', (16, 23)),
            ('top.sub.subsub.r2', 'RegNode', "my_reg_t", 0x110),
            ('top.sub.subsub.r2.f1', 'FieldNode', 'my_field_t', (0, 7)),
            ('top.sub.subsub.r2.f2', 'FieldNode', 'my_field_t', (8, 15)),
            ('top.sub.subsub.r2.f3', 'FieldNode', 'my_field_t', (16, 23)),
            ('top.sub.subsub.r3', 'RegNode', "my_reg_t", 0x120),
            ('top.sub.subsub.r3.f1', 'FieldNode', 'my_field_t', (0, 7)),
            ('top.sub.subsub.r3.f2', 'FieldNode', 'my_field_t', (8, 15)),
            ('top.sub.subsub.r3.f3', 'FieldNode', 'my_field_t', (16, 23)),
            ('top.my_mem[]', 'MemNode', None, 0x400),
            ('top.my_mem2[]', 'MemNode', 'my_mem_t', 0x800),
        ]

        self.assertEqual(nodes, expected_nodes)

    def test_illegal_inst_name_import_raises_error(self):
        rdlc = RDLCompiler()
        i = InstNameErrorTestcaseImporter(rdlc)
        with self.assertRaisesRegex(ValueError, "Instance name has invalid characters: 'reg1.some_signal'"):
            i.import_file("asdf")

    def test_illegal_type_name_import_raises_error(self):
        rdlc = RDLCompiler()
        i = TypeNameErrorTestcaseImporter(rdlc)
        with self.assertRaisesRegex(ValueError, "Type name has invalid characters: 'illegal.type.name'"):
            i.import_file("asdf")


    def test_importer_types(self):
        rdlc = RDLCompiler()

        this_dir = os.path.dirname(os.path.realpath(__file__))
        rdlc.compile_file(os.path.join(this_dir, "rdl_src/incdir/importer_udps.rdl"))

        i = TypeTestImporter(rdlc)
        i.import_file("asdf")

        root = rdlc.elaborate()

        top = root.top
        self.assertEqual(top.get_property("udp_string"), "my string")
        self.assertListEqual(top.get_property("udp_string_array"), ["str1", "str2", "str3"])
        self.assertIs(top.get_property("udp_boolean"), True)
        self.assertListEqual(top.get_property("udp_boolean_array"), [True, False, True])
        self.assertEqual(top.get_property("udp_longint"), 123)
        self.assertListEqual(top.get_property("udp_longint_array"), [12, 34, 56])

        reg = top.get_child_by_name("r")
        self.assertListEqual(reg.get_property("udp_string_array"), [])
        self.assertListEqual(reg.get_property("udp_boolean_array"), [])
        self.assertListEqual(reg.get_property("udp_longint_array"), [])
