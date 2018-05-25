from copy import deepcopy

from antlr4 import FileStream, CommonTokenStream

from . import messages
from .parser.SystemRDLLexer import SystemRDLLexer
from .parser.SystemRDLParser import SystemRDLParser
from .core.ComponentVisitor import RootVisitor
from .core.expressions import Expr
from .core.properties import PropertyRuleBook
from .core.namespace import NamespaceRegistry
from . import component as comp
from . import walker
from .node import Node, AddressableNode, RegNode
from . import rdltypes
from .core.helpers import is_pow2, roundup_pow2, roundup_to

class RDLCompiler:
    
    def __init__(self, message_printer=None):
        
        # Set up message handling
        if(message_printer is None):
            message_printer = messages.MessagePrinter()
        self.msg = messages.MessageHandler(message_printer)
        
        self.namespace = NamespaceRegistry(self)
        self.property_rules = PropertyRuleBook(self)
        
        self.visitor = RootVisitor(self)
        self.root = None
    
    
    def compile_file(self, path):
        """
        Parse & compile a single file and append it to the current root namespace
        
        Parameters
        ----------
        path:str
            Path to an RDL source file
        
        """
        
        input_stream = FileStream(path)
        
        lexer = SystemRDLLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(messages.RDLAntlrErrorListener(self.msg))
        
        token_stream = CommonTokenStream(lexer)
        
        parser = SystemRDLParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(messages.RDLAntlrErrorListener(self.msg))
        
        parsed_tree = parser.root()
        if(self.msg.error_count):
            self.msg.fatal("Parse aborted due to previous errors")
        
        self.root = self.visitor.visit(parsed_tree)
        
        if(self.msg.error_count):
            self.msg.fatal("Compile aborted due to previous errors")
    
    def elaborate(self, top_def_name, inst_name=None, parameters=None):
        """
        Elaborates the design with the specified component definition from
        the root namespace as the top-level component.
        
        Parameters
        ----------
        top_def_name: str
            Defined name of the top-level addrmap component in the root namespace.
        inst_name: str
            Overrides the top-component's instantiated name.
            By default, instantiated name is the same as *top_def_name*
        
        parameters: TBD
            Assign the top-component instance parameters
        
        Returns
        -------
        :class:`~systemrdl.node.AddrmapNode`
            Elaborated top-level component's Node object.
        """
        if(parameters is None):
            parameters = {}
        
        # Lookup top_def_name
        if(top_def_name not in self.root.comp_defs):
            self.msg.fatal("Elaboration target '%s' not found" % top_def_name)
        top_def = self.root.comp_defs[top_def_name]
        
        if(type(top_def) != comp.Addrmap):
            self.msg.fatal("Elaboration target '%s' is not an 'addrmap' component" % top_def_name)
        
        # Create a top-level instance
        top_inst = deepcopy(top_def)
        top_inst.is_instance = True
        if(inst_name is not None):
            top_inst.inst_name = inst_name
        else:
            top_inst.inst_name = top_def_name
        
        # Override parameters as needed
        if(len(parameters)):
            # TODO: Add mechanism to set parameters of top-level component
            raise NotImplementedError
        
        top_node = Node._factory(top_inst, self)
        
        # Resolve all expressions
        walker.RDLWalker(skip_not_present=False).walk(top_node, ElabExpressionsListener(self.msg))
        
        # Resolve address and field placement
        walker.RDLWalker(skip_not_present=False).walk(top_node, PrePlacementValidateListener(self.msg), StructuralPlacementListener(self.msg))
        
        # Validate design
        walker.RDLWalker().walk(top_node, ValidateListener(self))
        
        if(self.msg.error_count):
            self.msg.fatal("Elaborate aborted due to previous errors")
        
        return(top_node)

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
        if(node.inst.original_def is not None):
            # This is a parameterized instance
            # Generate the elaborated type name as per 5.1.1.4
            
            new_type_name = node.inst.original_def.type_name
            
            for i in range(len(node.inst.parameters)):
                orig_param_value = node.inst.original_def.parameters[i].get_value()
                new_param_value = node.inst.parameters[i].get_value()
                if(new_param_value != orig_param_value):
                    new_type_name = new_type_name + "_" + node.inst.parameters[i].get_normalized_parameter()
            node.inst.type_name = new_type_name
                
        else:
            # Evaluate parameters anyways
            # Result is not saved, but will catch evaluation errors if they exist
            for param in node.inst.parameters:
                param.get_value()
    
    def enter_AddressableComponent(self, node):
        # Evaluate instance object expressions
        if(issubclass(type(node.inst.addr_offset), Expr)):
            node.inst.addr_offset.resolve_expr_width()
            node.inst.addr_offset = node.inst.addr_offset.get_value()
        
        if(issubclass(type(node.inst.addr_align), Expr)):
            node.inst.addr_align.resolve_expr_width()
            node.inst.addr_align = node.inst.addr_align.get_value()
            if(node.inst.addr_align == 0):
                self.msg.fatal(
                    "Alignment allocator '%=' must be greater than zero",
                    node.inst.inst_err_ctx
                )
        
        if(node.inst.array_dimensions is not None):
            for i in range(len(node.inst.array_dimensions)):
                if(issubclass(type(node.inst.array_dimensions[i]), Expr)):
                    node.inst.array_dimensions[i].resolve_expr_width()
                    node.inst.array_dimensions[i] = node.inst.array_dimensions[i].get_value()
                    if(node.inst.array_dimensions[i] == 0):
                        self.msg.fatal(
                            "Array dimension must be greater than zero",
                            node.inst.inst_err_ctx
                        )
        
        if(issubclass(type(node.inst.array_stride), Expr)):
            node.inst.array_stride.resolve_expr_width()
            node.inst.array_stride = node.inst.array_stride.get_value()
            if(node.inst.array_stride == 0):
                self.msg.fatal(
                    "Array stride allocator '+=' must be greater than zero",
                    node.inst.inst_err_ctx
                )
    
    def enter_VectorComponent(self, node):
        # Evaluate instance object expressions
        if(issubclass(type(node.inst.width), Expr)):
            node.inst.width.resolve_expr_width()
            node.inst.width = node.inst.width.get_value()
            if(node.inst.width == 0):
                self.msg.fatal(
                    "Vector width must be greater than zero",
                    node.inst.inst_err_ctx
                )
        
        if(issubclass(type(node.inst.msb), Expr)):
            node.inst.msb.resolve_expr_width()
            node.inst.msb = node.inst.msb.get_value()
        
        if(issubclass(type(node.inst.lsb), Expr)):
            node.inst.lsb.resolve_expr_width()
            node.inst.lsb = node.inst.lsb.get_value()
    
    def exit_Component(self, node):
        # Evaluate component properties
        for prop_name, prop_value in node.inst.properties.items():
            if(issubclass(type(prop_value), Expr)):
                prop_value.resolve_expr_width()
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
        if('alignment' in node.inst.properties):
            n = node.inst.properties['alignment']
            if(n <= 0):
                self.msg.fatal(
                    "'alignment' property must be greater than zero",
                    node.inst.def_err_ctx
                )
            # 12.3.1-a, 13.4.1-b: All alignment values shall be a power of two (1, 2, 4, etc.)
            if(not is_pow2(n)):
                self.msg.fatal(
                    "'alignment' property must be a power of 2",
                    node.inst.def_err_ctx
                )
        
    
    
    def enter_Reg(self, node):
        # 10.6.1-a: All registers shall have a regwidth = 2 N , where N >=3.
        if('regwidth' in node.inst.properties):
            n = node.inst.properties['regwidth']
            if(n < 8):
                self.msg.fatal(
                    "'regwidth' property must be at least 8",
                    node.inst.def_err_ctx
                )
            if(not is_pow2(n)):
                self.msg.fatal(
                    "'regwidth' property must be a power of 2",
                    node.inst.def_err_ctx
                )
        
        # 10.6.1-b: All registers shall have a accesswidth = 2 N , where N >=3.
        if('accesswidth' in node.inst.properties):
            n = node.inst.properties['accesswidth']
            if(n < 8):
                self.msg.fatal(
                    "'accesswidth' property must be at least 8",
                    node.inst.def_err_ctx
                )
            if(not is_pow2(n)):
                self.msg.fatal(
                    "'accesswidth' property must be a power of 2",
                    node.inst.def_err_ctx
                )
        
    def enter_Field(self, node):
        if('fieldwidth' in node.inst.properties):
            n = node.inst.properties['fieldwidth']
            if(n <= 0):
                self.msg.fatal(
                    "'fieldwidth' property must be greater than zero",
                    node.inst.def_err_ctx
                )
    
    def enter_Signal(self, node):
        if('signalwidth' in node.inst.properties):
            n = node.inst.properties['signalwidth']
            if(n <= 0):
                self.msg.fatal(
                    "'signalwidth' property must be greater than zero",
                    node.inst.def_err_ctx
                )
        
    def enter_Mem(self, node):
        # 11.3.1-a: mementries shall be greater than 0.
        if('mementries' in node.inst.properties):
            n = node.inst.properties['mementries']
            if(n <= 0):
                self.msg.fatal(
                    "'mementries' property must be greater than zero",
                    node.inst.def_err_ctx
                )
        
        # 11.3.1-a: memwidth shall be greater than 0.
        if('memwidth' in node.inst.properties):
            n = node.inst.properties['memwidth']
            if(n <= 0):
                self.msg.fatal(
                    "'memwidth' property must be greater than zero",
                    node.inst.def_err_ctx
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
        if(alignment is None):
            # not set. Propagate from parent
            alignment = self.alignment_stack[-1]
        self.alignment_stack.append(alignment)
    
    def exit_Field(self, node):
        
        # Resolve field width
        if(node.inst.width is None):
            fieldwidth = node.get_property('fieldwidth')
            
            if((node.inst.lsb is not None) and (node.inst.msb is not None)):
                width = abs(node.inst.msb - node.inst.lsb) + 1
                
                node.inst.width = width
            elif(fieldwidth is not None):
                node.inst.width = fieldwidth
            else:
                node.inst.width = 1
        
        # Test field width again
        fieldwidth = node.get_property('fieldwidth')
        if(fieldwidth != node.inst.width):
            self.msg.fatal(
                "Width of field instance (%d) must match field's 'fieldwidth' property (%d)" % (node.inst.width, fieldwidth),
                node.inst.inst_err_ctx
            )
    
    def exit_Signal(self, node):
        
        # Resolve signal width
        if(node.inst.width is None):
            signalwidth = node.get_property('signalwidth')
            
            if((node.inst.lsb is not None) and (node.inst.msb is not None)):
                width = abs(node.inst.msb - node.inst.lsb) + 1
                
                node.inst.width = width
            elif(signalwidth is not None):
                node.inst.width = signalwidth
            else:
                node.inst.width = 1
        
        if((node.inst.lsb is None) or (node.inst.msb is None)):
            # Range instance style was not used. Deduce msb/lsb and high/low
            # Assume [width-1:0] style
            node.inst.lsb = 0
            node.inst.msb = node.inst.width - 1
            node.inst.low = 0
            node.inst.high = node.inst.width - 1
        
        # Test field width again
        signalwidth = node.get_property('signalwidth')
        if(signalwidth != node.inst.width):
            self.msg.fatal(
                "Width of signal instance (%d) must match signal's 'signalwidth' property (%d)" % (node.inst.width, signalwidth),
                node.inst.inst_err_ctx
            )
    
    
    def exit_Reg(self, node):
        
        regwidth = node.get_property('regwidth')
        
        # Resolve field positions.
        # First determine if there is an implied lsb/msb mode
        implied_lsb_inst = None
        implied_msb_inst = None
        for inst in node.inst.children:
            if(type(inst) != comp.Field):
                continue
            
            if((inst.lsb is None) or (inst.msb is None)):
                continue
            
            if(inst.msb > inst.lsb):
                # bit ordering is [high:low]. Implies lsb mode
                implied_lsb_inst = inst
            elif(inst.msb < inst.lsb):
                # bit ordering is [low:high]. Implies msb mode
                implied_msb_inst = inst
        
        # 10.7.1-a: Both the [low:high] and [high:low] bit specification forms 
        #   shall not be used together in the same register.
        if((implied_lsb_inst is not None) and (implied_msb_inst is not None)):
            # register uses both [high:low] and [low:high] ordering!
            self.msg.fatal(
                "Both the [low:high] (field '%s') and [high:low] (field '%s') bit specification forms shall not be used together in the same register."
                % (implied_msb_inst.inst_name, implied_lsb_inst.inst_name),
                node.inst.def_err_ctx
            )
        
        # Any implied lsb/msb modes override the property set by a parent
        if(implied_msb_inst is not None):
            is_msb0_mode = True
        elif(implied_lsb_inst is not None):
            is_msb0_mode = False
        else:
            is_msb0_mode = self.msb0_mode_stack[-1]
        
        # Assign field positions
        # Children are iterated in order of declaration
        prev_inst = None
        for inst in node.inst.children:
            if(type(inst) != comp.Field):
                continue
            
            if((inst.lsb is None) or (inst.msb is None)):
                # Offset is not known
                
                if(is_msb0_mode):
                    # In msb0 mode. Pack from top first
                    # lsb == high
                    # msb == low
                    if(prev_inst is None):
                        inst.lsb = regwidth - 1
                    else:
                        inst.lsb = prev_inst.msb - 1
                        
                    inst.msb = inst.lsb - inst.width + 1
                else:
                    # In lsb0 mode. Pack from bit 0 first
                    # lsb == low
                    # msb == high
                    if(prev_inst is None):
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
            if(type(inst) != comp.Field):
                return(-1)
            else:
                return(inst.low)
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
        if(node.inst.is_array and (node.inst.array_stride is None)):
            node.inst.array_stride = node.size
    
    
    def resolve_addresses(self, node):
        """
        Resolve addresses of children of Addrmap and Regfile components
        """
        
        # Get alignment based on 'alignment' property
        # This remains constant for all children
        prop_alignment = self.alignment_stack[-1]
        if(prop_alignment is None):
            # was not specified. Does not contribute to alignment
            prop_alignment = 1
        
        prev_node = None
        for child_node in node.children(skip_not_present=False):
            if(not issubclass(type(child_node), AddressableNode)):
                continue
            
            if(child_node.inst.addr_offset is not None):
                # Address is already known. Do not need to infer
                prev_node = child_node
                continue
            
            # Get alignment specified by '%=' allocator, if any
            alloc_alignment = child_node.inst.addr_align
            if(alloc_alignment is None):
                # was not specified. Does not contribute to alignment
                alloc_alignment = 1
            
            # Calculate alignment based on current addressing mode
            if(self.addressing_mode_stack[-1] == rdltypes.AddressingType.compact):
                if(type(child_node) == RegNode):
                    # Regs are aligned based on their accesswidth
                    mode_alignment = child_node.get_property('accesswidth') // 8
                else:
                    # Spec does not specify for other components
                    # Assuming absolutely compact packing
                    mode_alignment = 1
                    
            elif(self.addressing_mode_stack[-1] == rdltypes.AddressingType.regalign):
                # Components are aligned to a multiple of their size
                # Spec vaguely suggests that alignment is also a power of 2
                mode_alignment = child_node.size
                mode_alignment = roundup_pow2(mode_alignment)
                
            elif(self.addressing_mode_stack[-1] == rdltypes.AddressingType.fullalign):
                # Same as regalign except for arrays
                # Arrays are aligned to their total size
                # Both are rounded to power of 2
                mode_alignment = child_node.total_size
                mode_alignment = roundup_pow2(mode_alignment)
                
            else:
                raise RuntimeError
            
            # Calculate resulting address offset
            alignment = max(prop_alignment, alloc_alignment, mode_alignment)
            if(prev_node is None):
                next_offset = 0
            else:
                next_offset = prev_node.inst.addr_offset + prev_node.total_size
            
            # round next_offset up to alignment
            child_node.inst.addr_offset = roundup_to(next_offset, alignment)
            
            prev_node = child_node
        
        # Sort children by address offset
        # Non-addressable child components are sorted to be first (signals)
        def get_child_sort_key(inst):
            if(not issubclass(type(inst), comp.AddressableComponent)):
                return(-1)
            else:
                return(inst.addr_offset)
        node.inst.children.sort(key=get_child_sort_key)

#===============================================================================
# Validation Listeners
#===============================================================================
class ValidateListener(walker.RDLListener):
    # TODO: Validate design
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
        if(self.prev_field is None):
            self.msg.error(
                "Register '%s' does not contain any fields" % node.inst.inst_name,
                node.inst.inst_err_ctx
            )
        
    def enter_Field(self, node):
        
        # 9.4.1-Table 12: Check for bad sw/hw combinations
        this_f_hw = node.get_property('hw')
        this_f_sw = node.get_property('sw')
        if((this_f_sw == rdltypes.AccessType.w) and (this_f_hw == rdltypes.AccessType.w)):
            self.msg.error(
                "Field '%s' access property combination is meaningless: sw=w; hw=w;"
                % (node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        elif((this_f_sw == rdltypes.AccessType.w) and (this_f_hw == rdltypes.AccessType.na)):
            self.msg.error(
                "Field '%s' access property combination is meaningless: sw=w; hw=na;"
                % (node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        elif((this_f_sw == rdltypes.AccessType.na) and (this_f_hw == rdltypes.AccessType.w)):
            self.msg.error(
                "Field '%s' access property combination results in an unloaded net: sw=na; hw=w;"
                % (node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        elif((this_f_sw == rdltypes.AccessType.na) and (this_f_hw == rdltypes.AccessType.na)):
            self.msg.error(
                "Field '%s' access property combination results in a nonexistent net: sw=na; hw=na;"
                % (node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        
        # 10.1-d: Two field instances shall not occupy overlapping bit positions
        # within a register unless one field is read-only and the other field
        # is write-only.
        if((self.prev_field is not None) and (self.prev_field.inst.high >= node.inst.low)):
            prev_f_sw = self.prev_field.get_property('sw')
            
            if(
                (prev_f_sw == rdltypes.AccessType.r)
                and ((this_f_sw == rdltypes.AccessType.w) or this_f_sw == rdltypes.AccessType.w1)
            ):
                pass
            elif(
                (this_f_sw == rdltypes.AccessType.r)
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
        if(node.inst.high >= node.parent.get_property('regwidth')):
            self.msg.error(
                "High bit (%d) of field '%s' exceeds MSb of parent register"
                % (node.inst.high, node.inst.inst_name),
                node.inst.inst_err_ctx
            )
        
    
    def exit_Field(self, node):
        self.prev_field = node
        
        