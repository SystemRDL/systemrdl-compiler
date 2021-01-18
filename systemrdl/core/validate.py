from typing import TYPE_CHECKING, List

from .helpers import is_pow2, roundup_pow2, roundup_to
from .. import walker
from .. import rdltypes
from ..node import Node, AddressableNode
from ..node import AddrmapNode, RegfileNode, MemNode, RegNode, FieldNode

if TYPE_CHECKING:
    from ..compiler import RDLEnvironment
    from typing import Dict

#===============================================================================
# Validation Listeners
#===============================================================================
class ValidateListener(walker.RDLListener):
    def __init__(self, env: 'RDLEnvironment'):
        self.env = env
        self.msg = env.msg

        # Used in field overlap checks
        # This is a rolling buffer of previous fields that still have a chance
        # to possibly collide with a future field
        self.field_check_buffer = [] # type: List[FieldNode]

        # Used in addrmap, regfile, and reg overlap checks
        # Same concept as the field check buffer, but is also a stack
        self.addr_check_buffer_stack = [[]] # type: List[List[AddressableNode]]


    def enter_Component(self, node: Node) -> None:
        # Validate all properties that were applied to the component
        for prop_name in node.inst.properties.keys():
            prop_value = node.get_property(prop_name)

            if isinstance(prop_value, rdltypes.PropertyReference):
                prop_value._validate()

            prop_rule = self.env.property_rules.lookup_property(prop_name)
            prop_rule.validate(node, prop_value)


    def enter_AddressableComponent(self, node: AddressableNode) -> None:
        addr_check_buffer = self.addr_check_buffer_stack[-1]
        self.addr_check_buffer_stack.append([])

        # Check for collision with previous addressable sibling
        new_addr_check_buffer = []
        for prev_addressable in addr_check_buffer:
            if (prev_addressable.raw_address_offset + prev_addressable.total_size) > node.raw_address_offset:
                # Overlaps!

                # Only allowable overlaps are as follows:
                #   10.1-h: Registers shall not overlap, unless one contains only
                #   read-only fields and the other contains only write-only or
                #   write-once-only fields.
                overlap_allowed = False
                if isinstance(prev_addressable, RegNode) and isinstance(node, RegNode):
                    if (((not prev_addressable.has_sw_writable) and (not node.has_sw_readable))
                        or ((not prev_addressable.has_sw_readable) and (not node.has_sw_writable))
                    ):
                        overlap_allowed = True

                if not overlap_allowed:
                    self.msg.error(
                        "Instance '%s' at offset +0x%X:0x%X overlaps with '%s' at offset +0x%X:0x%X"
                        % (
                            node.inst_name, node.raw_address_offset, node.raw_address_offset + node.total_size - 1,
                            prev_addressable.inst_name, prev_addressable.raw_address_offset, prev_addressable.raw_address_offset + prev_addressable.total_size - 1,
                        ),
                        node.inst.inst_src_ref
                    )

                # Keep it in the list since it could collide again
                new_addr_check_buffer.append(prev_addressable)
        self.addr_check_buffer_stack[-2] = new_addr_check_buffer

        if node.is_array:
            assert node.array_stride is not None
            # Check if array interferes with itself
            if node.array_stride < node.size:
                self.msg.error(
                    "Instance array '%s' has address stride 0x%X, but the element size is 0x%X"
                    % (
                        node.inst_name, node.array_stride, node.size
                    ),
                    node.inst.inst_src_ref
                )

            if self.env.chk_stride_not_pow2:
                if not is_pow2(node.array_stride):
                    self.msg.message(
                        self.env.chk_stride_not_pow2,
                        "Address stride of instance array '%s' is not a power of 2"
                        % node.inst_name,
                        node.inst.inst_src_ref
                    )

        if self.env.chk_strict_self_align:
            req_align = roundup_pow2(node.size)
            if (node.raw_address_offset % req_align) != 0:
                self.msg.message(
                    self.env.chk_strict_self_align,
                    "Address offset +0x%x of instance '%s' is not a power of 2 multiple of its size 0x%x"
                    % (node.raw_address_offset, node.inst_name, node.size),
                    node.inst.inst_src_ref
                )


    def enter_Reg(self, node: RegNode) -> None:
        self.field_check_buffer = []

        if node.is_array and self.env.chk_sparse_reg_stride:
            assert node.array_stride is not None
            if node.array_stride > (node.get_property("regwidth") // 8):
                self.msg.message(
                    self.env.chk_sparse_reg_stride,
                    "Address stride (+= %d) of register array '%s' is not equal to it's width (regwidth/8 = %d)"
                    % (node.array_stride, node.inst_name, (node.get_property("regwidth") // 8)),
                    node.inst.inst_src_ref
                )

        # 11.2-e: Virtual register width is limited to the minimum power of two
        # bytes, which can contain the memory width ...
        if node.is_virtual:
            assert node.parent is not None # Reg always has a parent
            memwidth = node.parent.get_property('memwidth')
            memwidth_bytes = roundup_to(memwidth, 8) // 8
            max_regwidth = roundup_pow2(memwidth_bytes) * 8
            if node.get_property('regwidth') > max_regwidth:
                self.msg.error(
                    "regwidth (%d) of virtual register '%s' is too wide for this memory."
                    % (node.get_property('regwidth'), node.inst_name)
                    + " Virtual register width is limited to the minimum power of two bytes which can contain the memory width.",
                    node.inst.inst_src_ref
                )


    def exit_Reg(self, node: RegNode) -> None:
        # 10.1-c: At least one field shall be instantiated within a register
        #
        # At the end of field overlap checking, at least one entry is guaranteed to
        # be left over in the field_check_buffer
        if not self.field_check_buffer:
            self.msg.error(
                "Register '%s' does not contain any fields" % node.inst_name,
                node.inst.inst_src_ref
            )


    def enter_Field(self, node: FieldNode) -> None:
        assert node.parent is not None # fields are always enclosed by a reg

        this_f_hw = node.get_property('hw')
        this_f_sw = node.get_property('sw')
        parent_accesswidth = node.parent.get_property("accesswidth")
        parent_regwidth = node.parent.get_property("regwidth")

        # hw property values of w1 or rw1 don't make sense
        if this_f_hw in (rdltypes.AccessType.w1, rdltypes.AccessType.rw1):
            self.msg.error(
                "Field '%s' hw access property value of %s is meaningless"
                % (node.inst_name, this_f_hw.name),
                node.inst.inst_src_ref
            )

        # 9.4.1-Table 12: Check for bad sw/hw combinations
        if (this_f_sw == rdltypes.AccessType.w) and (this_f_hw == rdltypes.AccessType.w):
            self.msg.error(
                "Field '%s' access property combination is meaningless: sw=w; hw=w;"
                % (node.inst_name),
                node.inst.inst_src_ref
            )
        elif (this_f_sw == rdltypes.AccessType.w) and (this_f_hw == rdltypes.AccessType.na):
            self.msg.error(
                "Field '%s' access property combination is meaningless: sw=w; hw=na;"
                % (node.inst_name),
                node.inst.inst_src_ref
            )
        elif (this_f_sw == rdltypes.AccessType.na) and (this_f_hw == rdltypes.AccessType.w):
            self.msg.error(
                "Field '%s' access property combination results in an unloaded net: sw=na; hw=w;"
                % (node.inst_name),
                node.inst.inst_src_ref
            )
        elif (this_f_sw == rdltypes.AccessType.na) and (this_f_hw == rdltypes.AccessType.na):
            self.msg.error(
                "Field '%s' access property combination results in a nonexistent net: sw=na; hw=na;"
                % (node.inst_name),
                node.inst.inst_src_ref
            )
        elif this_f_sw == rdltypes.AccessType.na:
            self.msg.error(
                "Field '%s' sw access property value of na results in undefined behavior."
                % (node.inst_name),
                node.inst.inst_src_ref
            )

        # 10.1-d: Two field instances shall not occupy overlapping bit positions
        # within a register unless one field is read-only and the other field
        # is write-only.
        #
        # Scan through a copied list of the field_check_buffer for collisions
        # If an entry no longer collides with the current node, it can be removed
        # from the list since fields are sorted.
        new_field_check_buffer = []
        for prev_field in self.field_check_buffer:
            if prev_field.high >= node.low:
                # Found overlap!
                # Check if the overlap is allowed
                prev_f_sw = prev_field.get_property('sw')

                if((prev_f_sw == rdltypes.AccessType.r)
                    and (this_f_sw in (rdltypes.AccessType.w, rdltypes.AccessType.w1))
                ):
                    pass
                elif((this_f_sw == rdltypes.AccessType.r)
                    and (prev_f_sw in (rdltypes.AccessType.w, rdltypes.AccessType.w1))
                ):
                    pass
                else:
                    self.msg.error(
                        "Field '%s[%d:%d]' overlaps with field '%s[%d:%d]'"
                        % (node.inst_name, node.msb, node.lsb,
                            prev_field.inst_name, prev_field.msb, prev_field.lsb),
                        node.inst.inst_src_ref
                    )
                # Keep it in the list since it could collide again
                new_field_check_buffer.append(prev_field)
        self.field_check_buffer = new_field_check_buffer


        # 10.1-e: Field instances shall not occupy a bit position exceeding the
        # MSB of the register
        if node.high >= parent_regwidth:
            self.msg.error(
                "High bit (%d) of field '%s' exceeds MSb of parent register"
                % (node.high, node.inst_name),
                node.inst.inst_src_ref
            )

        # 10.6.1-f: Any field that is software-writable or clear on read shall
        # not span multiple software accessible sub-words (e.g., a 64-bit
        # register with a 32-bit access width may not have a writable field with
        # bits in both the upper and lower half of the register).
        #
        # Interpreting this further - this rule applies any time a field is
        # software-modifiable by any means, including rclr, rset, ruser
        if ((parent_accesswidth < parent_regwidth)
                and (node.lsb // parent_accesswidth) != (node.msb // parent_accesswidth)
                and (node.is_sw_writable or node.get_property("onread") is not None)):
            # Field spans across sub-words
            self.msg.error(
                "Software-modifiable field '%s' shall not span multiple software-accessible subwords."
                % node.inst_name,
                node.inst.inst_src_ref
            )

        # Optional warning if a field is missing a reset assignment
        if node.env.chk_missing_reset:
            # Implements storage but was never assigned a reset
            if node.implements_storage and (node.get_property("reset") is None):
                node.env.msg.message(
                    node.env.chk_missing_reset,
                    "Field '%s' implements storage but is missing a reset value. Initial state is undefined"
                    % node.inst_name,
                    node.inst.inst_src_ref
                )

            # Field is a static tie-off (no storage element, no hardware update path),
            # but the user never specified its value, so its readback value is
            # ambiguous.
            if (
                not node.implements_storage and node.is_sw_readable and (node.get_property("reset") is None)
                and (node.get_property('hw') in {rdltypes.AccessType.na, rdltypes.AccessType.r})
            ):
                node.env.msg.message(
                    node.env.chk_missing_reset,
                    "Field '%s' is a constant at runtime but does not have a known value. Recommend assigning it a reset value."
                    % node.inst_name,
                    node.inst.inst_src_ref
                )


        # 11.2-e: ... and all the virtual fields shall fit within the memory width.
        if node.is_virtual:
            assert node.parent.parent is not None # fields are always enclosed by something.reg
            memwidth = node.parent.parent.get_property('memwidth')
            if node.high >= memwidth:
                self.msg.error(
                    "Virtual field '%s' does not fit within the parent memory's width"
                    % node.inst_name,
                    node.inst.inst_src_ref
                )


    def exit_Field(self, node: FieldNode) -> None:
        self.field_check_buffer.append(node)


    def exit_Regfile(self, node: RegfileNode) -> None:
        # 12.2-c: At least one reg or regfile shall be instantiated within a regfile.
        if not self.addr_check_buffer_stack[-1]:
            self.msg.error(
                "Register file '%s' must contain at least one reg or regfile."
                % node.inst_name,
                node.inst.inst_src_ref
            )


    def exit_Addrmap(self, node: AddrmapNode) -> None:
        # 13.3-b: At least one register, register file, memory, or address map
        # shall be instantiated within an address map
        if not self.addr_check_buffer_stack[-1]:
            self.msg.error(
                "Address map '%s' must contain at least one reg, regfile, mem, or addrmap."
                % node.inst_name,
                node.inst.inst_src_ref
            )


    def exit_Mem(self, node: MemNode) -> None:
        # 11.2-i: The address space occupied by virtual registers shall be less
        # than or equal to the address space provided by the memory.
        if node.inst.children:
            last_child = Node._factory(node.inst.children[-1], node.env, node)
            if isinstance(last_child, RegNode):
                end_addr = last_child.raw_address_offset + last_child.total_size
                if end_addr > node.size:
                    self.msg.error(
                        "Address space occupied by registers (0x%X) exceeds size of mem '%s' (0x%X)"
                        % (end_addr, node.inst_name, node.size),
                        node.inst.inst_src_ref
                    )


    def exit_AddressableComponent(self, node: AddressableNode) -> None:
        self.addr_check_buffer_stack.pop()
        self.addr_check_buffer_stack[-1].append(node)
