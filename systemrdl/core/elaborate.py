
from .expressions import Expr
from .helpers import is_pow2, roundup_pow2, roundup_to

from .. import component as comp
from .. import walker
from .. import rdltypes
from ..node import AddressableNode, RegNode


#===============================================================================
# Elaboration Listeners
#===============================================================================

class ElabExpressionsListener(walker.RDLListener):
    """
    Elaborates all expressions
    - Component parameters
    - Instance array suffixes
    - Vector dimensions
    - Instance address allocators
    - Property assignments
    
    Also elaborates parameterized component type names
    """
    
    def __init__(self, msg_handler):
        self.msg = msg_handler
    
    def enter_Component(self, node):
        if node.inst.original_def is not None:
            # Generate the elaborated type name as per 5.1.1.4
            new_type_name = node.inst.original_def.type_name
            
            for i in range(len(node.inst.parameters)):
                orig_param_value = node.inst.original_def.parameters[i].get_value()
                new_param_value = node.inst.parameters[i].get_value()
                if new_param_value != orig_param_value:
                    new_type_name = new_type_name + "_" + node.inst.parameters[i].get_normalized_parameter()
            node.inst.type_name = new_type_name

    
    def enter_AddressableComponent(self, node):
        # Evaluate instance object expressions
        if isinstance(node.inst.addr_offset, Expr):
            node.inst.addr_offset = node.inst.addr_offset.get_value()
        
        if isinstance(node.inst.addr_align, Expr):
            node.inst.addr_align = node.inst.addr_align.get_value()
            if node.inst.addr_align == 0:
                self.msg.fatal(
                    "Alignment allocator '%=' must be greater than zero",
                    node.inst.inst_src_ref
                )
        
        if node.inst.array_dimensions is not None:
            for i in range(len(node.inst.array_dimensions)):
                if isinstance(node.inst.array_dimensions[i], Expr):
                    node.inst.array_dimensions[i] = node.inst.array_dimensions[i].get_value()
                    if node.inst.array_dimensions[i] == 0:
                        self.msg.fatal(
                            "Array dimension must be greater than zero",
                            node.inst.inst_src_ref
                        )
        
        if isinstance(node.inst.array_stride, Expr):
            node.inst.array_stride = node.inst.array_stride.get_value()
            if node.inst.array_stride == 0:
                self.msg.fatal(
                    "Array stride allocator '+=' must be greater than zero",
                    node.inst.inst_src_ref
                )
    
    def enter_VectorComponent(self, node):
        # Evaluate instance object expressions
        if isinstance(node.inst.width, Expr):
            node.inst.width = node.inst.width.get_value()
            if node.inst.width == 0:
                self.msg.fatal(
                    "Vector width must be greater than zero",
                    node.inst.inst_src_ref
                )
        
        if isinstance(node.inst.msb, Expr):
            node.inst.msb = node.inst.msb.get_value()
        
        if isinstance(node.inst.lsb, Expr):
            node.inst.lsb = node.inst.lsb.get_value()
    
    def exit_Component(self, node):
        # Evaluate component properties
        for prop_name, prop_value in node.inst.properties.items():
            if isinstance(prop_value, Expr):
                node.inst.properties[prop_name] = prop_value.get_value()

#-------------------------------------------------------------------------------
class PrePlacementValidateListener(walker.RDLListener):
    """
    Performs value checks of some properties prior to StructuralPlacementListener
    """
    def __init__(self, msg_handler):
        self.msg = msg_handler
    
    def enter_Addrmap(self, node):
        self.check_alignment(node)
        
    def enter_Regfile(self, node):
        self.check_alignment(node)
        
    def check_alignment(self, node):
        if 'alignment' in node.inst.properties:
            n = node.inst.properties['alignment']
            if n <= 0:
                self.msg.fatal(
                    "'alignment' property must be greater than zero",
                    node.inst.def_src_ref
                )
            # 12.3.1-a, 13.4.1-b: All alignment values shall be a power of two (1, 2, 4, etc.)
            if not is_pow2(n):
                self.msg.fatal(
                    "'alignment' property must be a power of 2",
                    node.inst.def_src_ref
                )
        
    
    
    def enter_Reg(self, node):
        # 10.6.1-a: All registers shall have a regwidth = 2 N , where N >=3.
        if 'regwidth' in node.inst.properties:
            n = node.inst.properties['regwidth']
            if n < 8:
                self.msg.fatal(
                    "'regwidth' property must be at least 8",
                    node.inst.def_src_ref
                )
            if not is_pow2(n):
                self.msg.fatal(
                    "'regwidth' property must be a power of 2",
                    node.inst.def_src_ref
                )
        
        # 10.6.1-b: All registers shall have a accesswidth = 2 N , where N >=3.
        if 'accesswidth' in node.inst.properties:
            n = node.inst.properties['accesswidth']
            if n < 8:
                self.msg.fatal(
                    "'accesswidth' property must be at least 8",
                    node.inst.def_src_ref
                )
            if not is_pow2(n):
                self.msg.fatal(
                    "'accesswidth' property must be a power of 2",
                    node.inst.def_src_ref
                )
        
    def enter_Field(self, node):
        if 'fieldwidth' in node.inst.properties:
            n = node.inst.properties['fieldwidth']
            if n <= 0:
                self.msg.fatal(
                    "'fieldwidth' property must be greater than zero",
                    node.inst.def_src_ref
                )
    
    def enter_Signal(self, node):
        if 'signalwidth' in node.inst.properties:
            n = node.inst.properties['signalwidth']
            if n <= 0:
                self.msg.fatal(
                    "'signalwidth' property must be greater than zero",
                    node.inst.def_src_ref
                )
        
    def enter_Mem(self, node):
        # 11.3.1-a: mementries shall be greater than 0.
        if 'mementries' in node.inst.properties:
            n = node.inst.properties['mementries']
            if n <= 0:
                self.msg.fatal(
                    "'mementries' property must be greater than zero",
                    node.inst.def_src_ref
                )
        
        # 11.3.1-a: memwidth shall be greater than 0.
        if 'memwidth' in node.inst.properties:
            n = node.inst.properties['memwidth']
            if n <= 0:
                self.msg.fatal(
                    "'memwidth' property must be greater than zero",
                    node.inst.def_src_ref
                )
    
#-------------------------------------------------------------------------------
class StructuralPlacementListener(walker.RDLListener):
    """
    Resolves inferred locations of structural components
    - Field width and offset
    - Component addresses
    - Signals.
    """
    
    def __init__(self, msg_handler):
        self.msg = msg_handler
        self.msb0_mode_stack = []
        self.addressing_mode_stack = []
        self.alignment_stack = []
    
    
    def enter_Addrmap(self, node):
        self.msb0_mode_stack.append(node.get_property("msb0"))
        self.addressing_mode_stack.append(node.get_property("addressing"))
        self.alignment_stack.append(node.get_property("alignment"))
    
    
    def enter_Regfile(self, node):
        # Regfile can override the current alignment, but does not block
        # the propagation of a parent's setting if left undefined
        alignment = node.get_property("alignment")
        if alignment is None:
            # not set. Propagate from parent
            alignment = self.alignment_stack[-1]
        self.alignment_stack.append(alignment)
    
    def exit_Field(self, node):
        
        # Resolve field width
        if node.inst.width is None:
            fieldwidth = node.get_property('fieldwidth')
            
            if (node.inst.lsb is not None) and (node.inst.msb is not None):
                width = abs(node.inst.msb - node.inst.lsb) + 1
                
                node.inst.width = width
            elif fieldwidth is not None:
                node.inst.width = fieldwidth
            else:
                node.inst.width = 1
        
        # Test field width again
        fieldwidth = node.get_property('fieldwidth')
        if fieldwidth != node.inst.width:
            self.msg.fatal(
                "Width of field instance (%d) must match field's 'fieldwidth' property (%d)"
                % (node.inst.width, fieldwidth),
                node.inst.inst_src_ref
            )
    
    def exit_Signal(self, node):
        
        # Resolve signal width
        if node.inst.width is None:
            signalwidth = node.get_property('signalwidth')
            
            if (node.inst.lsb is not None) and (node.inst.msb is not None):
                width = abs(node.inst.msb - node.inst.lsb) + 1
                
                node.inst.width = width
            elif signalwidth is not None:
                node.inst.width = signalwidth
            else:
                node.inst.width = 1
        
        if (node.inst.lsb is None) or (node.inst.msb is None):
            # Range instance style was not used. Deduce msb/lsb and high/low
            # Assume [width-1:0] style
            node.inst.lsb = 0
            node.inst.msb = node.inst.width - 1
            node.inst.low = 0
            node.inst.high = node.inst.width - 1
        
        # Test field width again
        signalwidth = node.get_property('signalwidth')
        if signalwidth != node.inst.width:
            self.msg.fatal(
                "Width of signal instance (%d) must match signal's 'signalwidth' property (%d)"
                % (node.inst.width, signalwidth),
                node.inst.inst_src_ref
            )
    
    
    def exit_Reg(self, node):
        
        regwidth = node.get_property('regwidth')
        
        # Resolve field positions.
        # First determine if there is an implied lsb/msb mode
        implied_lsb_inst = None
        implied_msb_inst = None
        for inst in node.inst.children:
            if not isinstance(inst, comp.Field):
                continue
            
            if (inst.lsb is None) or (inst.msb is None):
                continue
            
            if inst.msb > inst.lsb:
                # bit ordering is [high:low]. Implies lsb mode
                implied_lsb_inst = inst
            elif inst.msb < inst.lsb:
                # bit ordering is [low:high]. Implies msb mode
                implied_msb_inst = inst
        
        # 10.7.1-a: Both the [low:high] and [high:low] bit specification forms 
        #   shall not be used together in the same register.
        if (implied_lsb_inst is not None) and (implied_msb_inst is not None):
            # register uses both [high:low] and [low:high] ordering!
            self.msg.fatal(
                "Both the [low:high] (field '%s') and [high:low] (field '%s') bit specification forms shall not be used together in the same register."
                % (implied_msb_inst.inst_name, implied_lsb_inst.inst_name),
                node.inst.def_src_ref
            )
        
        # Any implied lsb/msb modes override the property set by a parent
        if implied_msb_inst is not None:
            is_msb0_mode = True
        elif implied_lsb_inst is not None:
            is_msb0_mode = False
        else:
            is_msb0_mode = self.msb0_mode_stack[-1]
        
        # Assign field positions
        # Children are iterated in order of declaration
        prev_inst = None
        for inst in node.inst.children:
            if not isinstance(inst, comp.Field):
                continue
            
            if (inst.lsb is None) or (inst.msb is None):
                # Offset is not known
                
                if node.env.warn_implicit_field_pos:
                    node.env.msg.warning(
                        "Bit offset for field '%s' is not explicit" % inst.inst_name,
                        inst.inst_src_ref
                    )
                
                if is_msb0_mode:
                    # In msb0 mode. Pack from top first
                    # lsb == high
                    # msb == low
                    if prev_inst is None:
                        inst.lsb = regwidth - 1
                    else:
                        inst.lsb = prev_inst.msb - 1
                        
                    inst.msb = inst.lsb - inst.width + 1
                else:
                    # In lsb0 mode. Pack from bit 0 first
                    # lsb == low
                    # msb == high
                    if prev_inst is None:
                        inst.lsb = 0
                    else:
                        inst.lsb = prev_inst.msb + 1
                        
                    inst.msb = inst.lsb + inst.width - 1
            inst.high = max(inst.msb, inst.lsb)
            inst.low = min(inst.msb, inst.lsb)
            prev_inst = inst
        
        # Sort fields by low-bit.
        # Non-field child components are sorted to be first (signals)
        def get_field_sort_key(inst):
            if not isinstance(inst, comp.Field):
                return -1
            else:
                return inst.low
        node.inst.children.sort(key=get_field_sort_key)
    
    
    def exit_Regfile(self, node):
        self.resolve_addresses(node)
        
        self.alignment_stack.pop()
    
    
    def exit_Addrmap(self, node):
        self.resolve_addresses(node)
        
        self.msb0_mode_stack.pop()
        self.addressing_mode_stack.pop()
        self.alignment_stack.pop()
    
    
    def exit_AddressableComponent(self, node):
        # Resolve array stride if needed
        if node.inst.is_array and (node.inst.array_stride is None):
            node.inst.array_stride = node.size
    
    
    def resolve_addresses(self, node):
        """
        Resolve addresses of children of Addrmap and Regfile components
        """
        
        # Get alignment based on 'alignment' property
        # This remains constant for all children
        prop_alignment = self.alignment_stack[-1]
        if prop_alignment is None:
            # was not specified. Does not contribute to alignment
            prop_alignment = 1
        
        prev_node = None
        for child_node in node.children(skip_not_present=False):
            if not isinstance(child_node, AddressableNode):
                continue
            
            if child_node.inst.addr_offset is not None:
                # Address is already known. Do not need to infer
                prev_node = child_node
                continue
            
            if node.env.warn_implicit_addr:
                node.env.msg.warning(
                    "Address offset of component '%s' is not explicitly set" % child_node.inst.inst_name,
                    child_node.inst.inst_src_ref
                )
            
            # Get alignment specified by '%=' allocator, if any
            alloc_alignment = child_node.inst.addr_align
            if alloc_alignment is None:
                # was not specified. Does not contribute to alignment
                alloc_alignment = 1
            
            # Calculate alignment based on current addressing mode
            if self.addressing_mode_stack[-1] == rdltypes.AddressingType.compact:
                if isinstance(child_node, RegNode):
                    # Regs are aligned based on their accesswidth
                    mode_alignment = child_node.get_property('accesswidth') // 8
                else:
                    # Spec does not specify for other components
                    # Assuming absolutely compact packing
                    mode_alignment = 1
                    
            elif self.addressing_mode_stack[-1] == rdltypes.AddressingType.regalign:
                # Components are aligned to a multiple of their size
                # Spec vaguely suggests that alignment is also a power of 2
                mode_alignment = child_node.size
                mode_alignment = roundup_pow2(mode_alignment)
                
            elif self.addressing_mode_stack[-1] == rdltypes.AddressingType.fullalign:
                # Same as regalign except for arrays
                # Arrays are aligned to their total size
                # Both are rounded to power of 2
                mode_alignment = child_node.total_size
                mode_alignment = roundup_pow2(mode_alignment)
                
            else:
                raise RuntimeError
            
            # Calculate resulting address offset
            alignment = max(prop_alignment, alloc_alignment, mode_alignment)
            if prev_node is None:
                next_offset = 0
            else:
                next_offset = prev_node.inst.addr_offset + prev_node.total_size
            
            # round next_offset up to alignment
            child_node.inst.addr_offset = roundup_to(next_offset, alignment)
            
            prev_node = child_node
        
        # Sort children by address offset
        # Non-addressable child components are sorted to be first (signals)
        def get_child_sort_key(inst):
            if not isinstance(inst, comp.AddressableComponent):
                return -1
            else:
                return inst.addr_offset
        node.inst.children.sort(key=get_child_sort_key)

#-------------------------------------------------------------------------------
class LateElabListener(walker.RDLListener):
    """
    Elaboration listener for misc late-stage things
    """
    def __init__(self, msg_handler):
        self.msg = msg_handler
    
    def enter_Field(self, node):
        
        # 9.6.1-d: swwe and swwel have precedence over the software access
        # property in determining its current access state, e.g., if a field is
        # declared as sw=rw, has a swwe property, and the value is currently
        # false, the effective software access property is sw=r.
        #
        # Extending this idea further: if swwe/swwel has a field/signal reference
        # then it implies that the software access CAN be writable, and therefore
        # overrides sw to include the "w"
        override_to_writable = False
        override_to_not_writable = False
        if "swwe" in node.inst.properties:
            swwe = node.inst.properties['swwe']
            if isinstance(swwe, rdltypes.ComponentRef):
                override_to_writable = True
            elif swwe is True:
                override_to_writable = True
            else:
                override_to_not_writable = True
            
        elif "swwel" in node.inst.properties:
            swwel = node.inst.properties['swwel']
            if isinstance(swwel, rdltypes.ComponentRef):
                override_to_writable = True
            elif swwel is False:
                override_to_writable = True
            else:
                override_to_not_writable = True
        
        this_f_sw = node.get_property('sw')
        if override_to_writable:
            if this_f_sw == rdltypes.AccessType.r:
                node.inst.properties['sw'] = rdltypes.AccessType.rw
            elif this_f_sw == rdltypes.AccessType.na:
                node.inst.properties['sw'] = rdltypes.AccessType.w
        elif override_to_not_writable:
            if this_f_sw == rdltypes.AccessType.rw:
                node.inst.properties['sw'] = rdltypes.AccessType.r
            elif this_f_sw == rdltypes.AccessType.w:
                node.inst.properties['sw'] = rdltypes.AccessType.na
            elif this_f_sw == rdltypes.AccessType.rw1:
                node.inst.properties['sw'] = rdltypes.AccessType.r
            elif this_f_sw == rdltypes.AccessType.w1:
                node.inst.properties['sw'] = rdltypes.AccessType.na
