
from .. import walker
from .. import rdltypes
from ..node import RegNode

#===============================================================================
# Validation Listeners
#===============================================================================
class ValidateListener(walker.RDLListener):
    # TODO: Finish Validate design
    def __init__(self, compiler):
        self.compiler = compiler
        self.msg = compiler.msg
        
        # Used in field overlap checks
        # This is a rolling buffer of previous fields that still have a chance
        # to possibly collide with a future field
        self.field_check_buffer = []
        
        # Used in addrmap, regfile, and reg overlap checks
        # Same concept as the field check buffer, but is also a stack
        self.addr_check_buffer_stack = [[]]
    
    
    def enter_Component(self, node):
        
        # Validate all properties that were applied to the component
        for prop_name in node.inst.properties.keys():
            prop_value = node.get_property(prop_name)
            prop_rule = self.compiler.property_rules.lookup_property(prop_name)
            prop_rule.validate(node, prop_value)
    
    
    def enter_AddressableComponent(self, node):
        addr_check_buffer = self.addr_check_buffer_stack[-1]
        self.addr_check_buffer_stack.append([])
        
        # Check for collision with previous addressable sibling
        new_addr_check_buffer = []
        for prev_addressable in addr_check_buffer:
            if (prev_addressable.inst.addr_offset + prev_addressable.total_size) > node.inst.addr_offset:
                # Overlaps!
                
                # Only allowable overlaps are as follows:
                #   10.1-h: Registers shall not overlap, unless one contains only
                #   read-only fields and the other contains only write-only or
                #   write-once-only fields.
                overlap_allowed = False
                if isinstance(prev_addressable, RegNode) and isinstance(node, RegNode):
                    if ((not prev_addressable.has_sw_writable) and (not node.has_sw_readable)
                        or (not prev_addressable.has_sw_readable) and (not node.has_sw_writable)
                    ):
                        overlap_allowed = True
                
                if not overlap_allowed:
                    self.msg.error(
                        "Instance '%s' at offset +0x%X:0x%X overlaps with '%s' at offset +0x%X:0x%X"
                        % (
                            node.inst.inst_name, node.inst.addr_offset, node.inst.addr_offset + node.total_size - 1,
                            prev_addressable.inst.inst_name, prev_addressable.inst.addr_offset, prev_addressable.inst.addr_offset + prev_addressable.total_size - 1,
                        ),
                        node.inst.inst_err_ctx
                    )
                
                # Keep it in the list since it could collide again
                new_addr_check_buffer.append(prev_addressable)
        self.addr_check_buffer_stack[-2] = new_addr_check_buffer
        
    
    def exit_AddressableComponent(self, node):
        self.addr_check_buffer_stack.pop()
        self.addr_check_buffer_stack[-1].append(node)
    
    
    def enter_Reg(self, node):
        self.field_check_buffer = []
    
    
    def exit_Reg(self, node):
        # 10.1-c: At least one field shall be instantiated within a register
        #
        # At the end of field overlap checking, at least one entry is guaranteed to
        # be left over in the field_check_buffer
        if not self.field_check_buffer:
            self.msg.error(
                "Register '%s' does not contain any fields" % node.inst.inst_name,
                node.inst.inst_err_ctx
            )
    
    
    def enter_Field(self, node):
        this_f_hw = node.get_property('hw')
        this_f_sw = node.get_property('sw')
        
        # hw property values of w1 or rw1 don't make sense
        if (this_f_hw == rdltypes.AccessType.w1) or (this_f_hw == rdltypes.AccessType.rw1):
            self.msg.error(
                "Field '%s' hw access property value of %s is meaningless"
                % (node.inst.inst_name, this_f_hw.name),
                node.inst.inst_err_ctx
            )
        
        # 9.4.1-Table 12: Check for bad sw/hw combinations
        if (this_f_sw == rdltypes.AccessType.w) and (this_f_hw == rdltypes.AccessType.w):
            self.msg.error(
                "Field '%s' access property combination is meaningless: sw=w; hw=w;"
                % (node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        elif (this_f_sw == rdltypes.AccessType.w) and (this_f_hw == rdltypes.AccessType.na):
            self.msg.error(
                "Field '%s' access property combination is meaningless: sw=w; hw=na;"
                % (node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        elif (this_f_sw == rdltypes.AccessType.na) and (this_f_hw == rdltypes.AccessType.w):
            self.msg.error(
                "Field '%s' access property combination results in an unloaded net: sw=na; hw=w;"
                % (node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        elif (this_f_sw == rdltypes.AccessType.na) and (this_f_hw == rdltypes.AccessType.na):
            self.msg.error(
                "Field '%s' access property combination results in a nonexistent net: sw=na; hw=na;"
                % (node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        elif this_f_sw == rdltypes.AccessType.na:
            self.msg.error(
                "Field '%s' sw access property value of na results in undefined behavior."
                % (node.inst.inst_name),
                node.inst.inst_err_ctx
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
            if prev_field.inst.high >= node.inst.low:
                # Found overlap!
                # Check if the overlap is allowed
                prev_f_sw = prev_field.get_property('sw')
                
                if((prev_f_sw == rdltypes.AccessType.r)
                    and ((this_f_sw == rdltypes.AccessType.w) or this_f_sw == rdltypes.AccessType.w1)
                ):
                    pass
                elif((this_f_sw == rdltypes.AccessType.r)
                    and ((prev_f_sw == rdltypes.AccessType.w) or prev_f_sw == rdltypes.AccessType.w1)
                ):
                    pass
                else:
                    self.msg.error(
                        "Field '%s[%d:%d]' overlaps with field '%s[%d:%d]'"
                        % (node.inst.inst_name, node.inst.msb, node.inst.lsb,
                            prev_field.inst.inst_name, prev_field.inst.msb, prev_field.inst.lsb),
                        node.inst.inst_err_ctx
                    )
                # Keep it in the list since it could collide again
                new_field_check_buffer.append(prev_field)
        self.field_check_buffer = new_field_check_buffer
            
        
        # 10.1-e: Field instances shall not occupy a bit position exceeding the
        # MSB of the register
        if node.inst.high >= node.parent.get_property('regwidth'):
            self.msg.error(
                "High bit (%d) of field '%s' exceeds MSb of parent register"
                % (node.inst.high, node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        
    
    def exit_Field(self, node):
        self.field_check_buffer.append(node)
