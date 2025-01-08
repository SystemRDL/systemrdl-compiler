import glob
import os
from typing import Union, List, Optional
import sys

from typing_extensions import Literal, get_overloads, get_type_hints
from parameterized import parameterized_class
import pytest

from lib.type_hint_utils import value_is_compatible, hint_is
from systemrdl.node import AddressableNode, FieldNode, MemNode, Node, AddrmapNode, RegNode, RegfileNode, RootNode, SignalNode, VectorNode
from systemrdl import component as comp
from unittest_utils import RDLSourceTestCase

from systemrdl.walker import RDLListener, RDLWalker, WalkerAction

# Get all RDL sources
rdl_src_files = glob.glob("rdl_src/*.rdl")

# Exclude some files as root compile targets:
exclude = {
    "rdl_src/preprocessor_incl.rdl", # is an include file
    "rdl_src/udp_builtin.rdl", # uses builtins
}

# Build testcase list
cases = []
for file in rdl_src_files:
    if file in exclude:
        continue
    args = {
        "name": os.path.basename(file),
        "src": file,
    }
    cases.append(args)

@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="requires python3.11 or newer for proper type introspection"
)
@parameterized_class(cases)
class TestTypeHints(RDLSourceTestCase):
    def check_node_properties(self, node):
        """
        Check that each of the node's properties returns a value that matches
        the expected annotated type hint
        """
        gp_overloads = get_overloads(node.get_property)
        self.assertGreater(len(gp_overloads), 0)

        for gp_overload in gp_overloads:
            hints = get_type_hints(gp_overload)

            # Skip overloads that use default override signature:
            #   get_property(*, default=...)
            if "default" in hints:
                continue

            # Skip generic overloads that do not specify an explicit property
            if not hint_is(hints["prop_name"], Literal):
                continue

            # Currently assuming only one arg to Literal
            self.assertEqual(len(hints["prop_name"].__args__), 1)
            property_name = hints["prop_name"].__args__[0]
            #print(f"Checking {node.get_path()}->{property_name}")

            value = node.get_property(property_name)
            self.assertTrue(
                value_is_compatible(value, hints["return"]),
                f"Value '{value}' does not match expected type: {hints['return']}. "
                f"for: {node.get_path()}->{property_name}"
            )

    def assert_attr_type_hint(self, node, attr_name, hint):
        """
        Assert a node's attribute matches the expected type hint
        """
        value = getattr(node, attr_name)
        self.assertTrue(
            value_is_compatible(value, hint),
            f"Value '{value}' does not match expected type: {hint}."
            f"for: {node.get_path()}::{attr_name}"
        )

    def test_all_nodes(self):
        root = self.compile(
            [self.src],
            incl_search_paths=["rdl_src/incdir"]
        )

        walker = RDLWalker(skip_not_present=False)
        listener = RDLTestListener(self)
        walker.walk(root, listener)

        # Test root itself
        self.assertIsNone(root.parent)
        self.assert_attr_type_hint(root, "inst", comp.Root)
        self.assert_attr_type_hint(root, "inst_name", str)
        self.assert_attr_type_hint(root, "type_name", Optional[str])
        self.assert_attr_type_hint(root, "orig_type_name", Optional[str])
        self.assert_attr_type_hint(root, "external", bool)

class RDLTestListener(RDLListener):
    def __init__(self, test_class: TestTypeHints) -> None:
        super().__init__()
        self.test_class = test_class

    def enter_Component(self, node: Node) -> None:
        self.test_class.check_node_properties(node)
        self.test_class.assert_attr_type_hint(node, "owning_addrmap", Optional[AddrmapNode])
        self.test_class.assert_attr_type_hint(node, "inst_name", str)
        self.test_class.assert_attr_type_hint(node, "type_name", Optional[str])
        self.test_class.assert_attr_type_hint(node, "orig_type_name", Optional[str])
        self.test_class.assert_attr_type_hint(node, "external", bool)

    def enter_AddressableComponent(self, node: AddressableNode) -> None:
        self.test_class.assert_attr_type_hint(node, "raw_address_offset", int)
        self.test_class.assert_attr_type_hint(node, "raw_absolute_address", int)
        self.test_class.assert_attr_type_hint(node, "size", int)
        self.test_class.assert_attr_type_hint(node, "total_size", int)
        if node.is_array:
            self.test_class.assert_attr_type_hint(node, "array_dimensions", List[int])
            self.test_class.assert_attr_type_hint(node, "array_stride", int)
        else:
            self.test_class.assertIsNone(node.array_dimensions)
            self.test_class.assertIsNone(node.array_stride)


    def enter_VectorComponent(self, node: VectorNode) -> None:
        self.test_class.assert_attr_type_hint(node, "width", int)
        self.test_class.assert_attr_type_hint(node, "msb", int)
        self.test_class.assert_attr_type_hint(node, "lsb", int)
        self.test_class.assert_attr_type_hint(node, "high", int)
        self.test_class.assert_attr_type_hint(node, "low", int)

    def enter_Signal(self, node: SignalNode) -> None:
        self.test_class.assert_attr_type_hint(node, "parent", Node)
        self.test_class.assert_attr_type_hint(node, "inst", comp.Signal)

    def enter_Field(self, node: FieldNode) -> None:
        self.test_class.assert_attr_type_hint(node, "parent", RegNode)
        self.test_class.assert_attr_type_hint(node, "inst", comp.Field)
        self.test_class.assert_attr_type_hint(node, "is_virtual", bool)
        self.test_class.assert_attr_type_hint(node, "is_volatile", bool)
        self.test_class.assert_attr_type_hint(node, "is_sw_writable", bool)
        self.test_class.assert_attr_type_hint(node, "is_sw_readable", bool)
        self.test_class.assert_attr_type_hint(node, "is_hw_writable", bool)
        self.test_class.assert_attr_type_hint(node, "is_hw_readable", bool)
        self.test_class.assert_attr_type_hint(node, "implements_storage", bool)
        self.test_class.assert_attr_type_hint(node, "is_up_counter", bool)
        self.test_class.assert_attr_type_hint(node, "is_down_counter", bool)
        self.test_class.assert_attr_type_hint(node, "is_alias", bool)
        self.test_class.assert_attr_type_hint(node, "has_aliases", bool)

    def enter_Reg(self, node: RegNode) -> None:
        self.test_class.assert_attr_type_hint(node, "parent", Union[AddrmapNode, RegfileNode, MemNode])
        self.test_class.assert_attr_type_hint(node, "inst", comp.Reg)
        self.test_class.assert_attr_type_hint(node, "size", int)
        self.test_class.assert_attr_type_hint(node, "is_virtual", bool)
        self.test_class.assert_attr_type_hint(node, "has_sw_writable", bool)
        self.test_class.assert_attr_type_hint(node, "has_sw_readable", bool)
        self.test_class.assert_attr_type_hint(node, "has_hw_writable", bool)
        self.test_class.assert_attr_type_hint(node, "has_hw_readable", bool)
        self.test_class.assert_attr_type_hint(node, "is_interrupt_reg", bool)
        self.test_class.assert_attr_type_hint(node, "is_halt_reg", bool)
        self.test_class.assert_attr_type_hint(node, "is_alias", bool)
        self.test_class.assert_attr_type_hint(node, "has_aliases", bool)

    def enter_Regfile(self, node: RegfileNode) -> None:
        self.test_class.assert_attr_type_hint(node, "parent", Union[AddrmapNode, RegfileNode])
        self.test_class.assert_attr_type_hint(node, "inst", comp.Regfile)
        self.test_class.assert_attr_type_hint(node, "size", int)

    def enter_Addrmap(self, node: AddrmapNode) -> None:
        self.test_class.assert_attr_type_hint(node, "parent", Union[AddrmapNode, RootNode])
        self.test_class.assert_attr_type_hint(node, "inst", comp.Addrmap)
        self.test_class.assert_attr_type_hint(node, "size", int)

    def enter_Mem(self, node: MemNode) -> None:
        self.test_class.assert_attr_type_hint(node, "parent", AddrmapNode)
        self.test_class.assert_attr_type_hint(node, "inst", comp.Mem)
        self.test_class.assert_attr_type_hint(node, "size", int)
        self.test_class.assert_attr_type_hint(node, "is_sw_writable", bool)
        self.test_class.assert_attr_type_hint(node, "is_sw_readable", bool)
