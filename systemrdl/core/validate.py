
from .. import walker
from .. import rdltypes

#===============================================================================
# Validation Listeners
#===============================================================================
class ValidateListener(walker.RDLListener):
    # TODO: Finish Validate design
    def __init__(self, compiler):
        self.compiler = compiler
        self.msg = compiler.msg
        
        # Used in field overlap checks
        self.prev_field = None
        
    def enter_Component(self, node):
        
        # Validate all properties that were applied to the component
        for prop_name in node.inst.properties.keys():
            prop_value = node.get_property(prop_name)
            prop_rule = self.compiler.property_rules.lookup_property(prop_name)
            prop_rule.validate(node, prop_value)
        
    def enter_Reg(self, node):
        self.prev_field = None
        
    def exit_Reg(self, node):
        # 10.1-c: At least one field shall be instantiated within a register
        if self.prev_field is None:
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
        if (self.prev_field is not None) and (self.prev_field.inst.high >= node.inst.low):
            prev_f_sw = self.prev_field.get_property('sw')
            
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
                    "Field '%s' overlaps with field '%s'"
                    % (node.inst.inst_name, self.prev_field.inst.inst_name),
                    node.inst.inst_err_ctx
                )
            
        
        # 10.1-e: Field instances shall not occupy a bit position exceeding the
        # MSB of the register
        if node.inst.high >= node.parent.get_property('regwidth'):
            self.msg.error(
                "High bit (%d) of field '%s' exceeds MSb of parent register"
                % (node.inst.high, node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        
    
    def exit_Field(self, node):
        self.prev_field = node
