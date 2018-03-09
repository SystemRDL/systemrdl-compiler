import sys
import math
import operator
import functools
from copy import deepcopy

from antlr4 import FileStream, CommonTokenStream

from .parser.SystemRDLLexer import SystemRDLLexer
from .parser.SystemRDLParser import SystemRDLParser
from .compiler.ComponentVisitor import RootVisitor
from .compiler.errors import RDLParserErrorListener, RDLCompileError, ConsoleErrorPrinter
from .compiler.expressions import Expr
from .compiler.properties import PropertyRuleBook
from .compiler.namespace import NamespaceRegistry
from .model import component as comp
from .model import walker
from .model.node import Node, AddressableNode, RegNode
from .model import rdl_types

class RDLCompiler:
    
    def __init__(self):
        namespace = NamespaceRegistry()
        
        self.property_rules = PropertyRuleBook()
        self.visitor = RootVisitor(namespace, self.property_rules)
        self.root = None
        self.error_handler = ConsoleErrorPrinter()
    
    
    def compile_file(self, path):
        """
        Parse & compile the file specified by path
        
        Call this multiple times to add file contents to the Root meta-component
        """
        
        input_stream = FileStream(path)
        lexer = SystemRDLLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = SystemRDLParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(RDLParserErrorListener())
        
        try:
            self.root = self.visitor.visit(parser.root())
        except RDLCompileError as e:
            self.error_handler.handle_exception(e)
            sys.exit(1)
    
    
    def elaborate(self, top_def_name, inst_name=None, parameters=None):
        """
        Elaborates the design with the specified component definition from
        the Root namespace as the top-level component.
        
        inst_name overrides the top-component's instantiated name
        
        Returns the elaborated top-level component Node object
        """
        if(parameters is None):
            parameters = {}
        
        try:
            return(self._do_elaborate(top_def_name, inst_name, parameters))
        except RDLCompileError as e:
            self.error_handler.handle_exception(e)
            sys.exit(1)
    
    
    def _do_elaborate(self, top_def_name, inst_name, parameters):
        
        # Lookup top_def_name
        if(top_def_name not in self.root.comp_defs):
            raise RDLCompileError("Elaboration target '%s' not found" % top_def_name)
        top_def = self.root.comp_defs[top_def_name]
        
        if(type(top_def) != comp.Addrmap):
            raise RDLCompileError("Elaboration target '%s' is not an 'addrmap' component" % top_def_name)
        
        # Create a top-level instance
        top_inst = deepcopy(top_def)
        top_inst.is_instance = True
        if(inst_name is not None):
            top_inst.inst_name = inst_name
        else:
            top_inst.inst_name = top_def_name
        
        # Override parameters as needed
        if(len(parameters)):
            # TODO
            raise NotImplementedError
        
        top_node = Node.factory(top_inst, self)
        
        # Resolve all expressions
        walker.RDLWalker().walk(ElabExpressionsListener(), top_node)
        
        # TODO: Resolve address and field placement
        walker.RDLWalker().walk(StructuralPlacementListener(), top_node)
        
        # TODO: Uniquify parameterized Component type names
        
        # TODO: Validate design
        
        return(top_node)

#===============================================================================

class ElabExpressionsListener(walker.RDLListener):
    """
    Elaborates all expressions
    - Component parameters
    - Instance array suffixes
    - Vector dimensions
    - Instance address allocators
    - Property assignments
    """
    def enter_Component(self, node):
        # Evaluate parameters
        # Result is not saved, but will catch evaluation errors if they exist
        for param in node.inst.parameters:
            if(issubclass(type(param.expr), Expr)):
                param.expr.resolve_expr_width()
                param.expr.get_value()
    
    
    def enter_AddressableComponent(self, node):
        # Evaluate instance object expressions
        if(issubclass(type(node.inst.addr_offset), Expr)):
            node.inst.addr_offset.resolve_expr_width()
            node.inst.addr_offset = node.inst.addr_offset.get_value()
        
        if(issubclass(type(node.inst.addr_align), Expr)):
            node.inst.addr_align.resolve_expr_width()
            node.inst.addr_align = node.inst.addr_align.get_value()
        
        if(node.inst.array_dimensions is not None):
            for i in range(len(node.inst.array_dimensions)):
                if(issubclass(type(node.inst.array_dimensions[i]), Expr)):
                    node.inst.array_dimensions[i].resolve_expr_width()
                    node.inst.array_dimensions[i] = node.inst.array_dimensions[i].get_value()
        
        if(issubclass(type(node.inst.array_stride), Expr)):
            node.inst.array_stride.resolve_expr_width()
            node.inst.array_stride = node.inst.array_stride.get_value()
    
    
    def enter_VectorComponent(self, node):
        # Evaluate instance object expressions
        if(issubclass(type(node.inst.width), Expr)):
            node.inst.width.resolve_expr_width()
            node.inst.width = node.inst.width.get_value()
        
        if(issubclass(type(node.inst.msb), Expr)):
            node.inst.msb.resolve_expr_width()
            node.inst.msb = node.inst.msb.get_value()
        
        if(issubclass(type(node.inst.lsb), Expr)):
            node.inst.lsb.resolve_expr_width()
            node.inst.lsb = node.inst.lsb.get_value()
        
    def enter_Field(self, node):
        if(issubclass(type(node.inst.reset_value), Expr)):
            node.inst.reset_value.resolve_expr_width()
            node.inst.reset_value = node.inst.reset_value.get_value()
    
    
    def exit_Component(self, node):
        # Evaluate component properties
        for prop_name, prop_value in node.inst.properties.items():
            if(issubclass(type(prop_value), Expr)):
                prop_value.resolve_expr_width()
                node.inst.properties[prop_name] = prop_value.get_value()

#-------------------------------------------------------------------------------
class StructuralPlacementListener(walker.RDLListener):
    """
    Resolves inferred locations of structural components
    - Field width and offset
    - Component addresses TODO
    - Signal stuff?? TODO - TBD
    """
    def __init__(self):
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
                width = node.inst.msb - node.inst.lsb + 1
                if(width <= 0):
                    raise RDLCompileError(
                        "Invalid field bit range",
                        node.inst.inst_err_ctx
                    )
                
                node.inst.width = width
            elif(fieldwidth is not None):
                node.inst.width = fieldwidth
            else:
                node.inst.width = 1
        
        # Test field width again
        fieldwidth = node.get_property('fieldwidth')
        if(fieldwidth != node.inst.width):
            raise RDLCompileError(
                "Width of field instance (%d) must match field's 'fieldwidth' preoperty (%d)" % (node.inst.width, fieldwidth),
                node.inst.inst_err_ctx
            )
    
    
    def exit_Reg(self, node):
        
        regwidth = node.get_property('regwidth')
        
        # Resolve field positions
        # Children are iterated in order of declaration
        prev_inst = None
        for inst in node.inst.children:
            if(type(inst) != comp.Field):
                continue
            
            if((inst.lsb is None) or (inst.msb is None)):
                # Offset is not known
                
                if(self.msb0_mode_stack[-1]):
                    # In msb0 mode. Pack from top first
                    if(prev_inst is None):
                        inst.msb = regwidth - 1
                    else:
                        inst.msb = prev_inst.lsb - 1
                        
                    inst.lsb = inst.msb - inst.width + 1
                else:
                    # In lsb0 mode. Pack from bit 0 first
                    if(prev_inst is None):
                        inst.lsb = 0
                    else:
                        inst.lsb = prev_inst.msb + 1
                        
                    inst.msb = inst.lsb + inst.width - 1
            prev_inst = inst
        
        # Sort fields by lsb.
        # Non-field child components are sorted to be first (signals)
        def get_field_sort_key(inst):
            if(type(inst) != comp.Field):
                return(-1)
            else:
                return(inst.lsb)
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
        for child_node in node.children():
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
            if(self.addressing_mode_stack[-1] == rdl_types.AddressingType.compact):
                if(type(child_node) == RegNode):
                    # Regs are aligned based on their accesswidth
                    mode_alignment = child_node.get_property('accesswidth') // 8
                else:
                    # Spec does not specify for other components
                    # Assuming absolutely compact packing
                    mode_alignment = 1
                    
            elif(self.addressing_mode_stack[-1] == rdl_types.AddressingType.regalign):
                # Components are aligned to a multiple of their size
                # Spec vaguely suggests that alignment is also a power of 2
                mode_alignment = child_node.size
                mode_alignment = 2**(math.ceil(math.log(mode_alignment, 2)))
            
            elif(self.addressing_mode_stack[-1] == rdl_types.AddressingType.fullalign):
                # Same as regalign except for arrays
                # Arrays are aligned to their total size
                # Both are rounded to power of 2
                mode_alignment = child_node.total_size
                mode_alignment = 2**(math.ceil(math.log(mode_alignment, 2)))
                
            else:
                raise RuntimeError
            
            # Calculate resulting address offset
            alignment = max(prop_alignment, alloc_alignment, mode_alignment)
            if(prev_node is None):
                next_offset = 0
            else:
                next_offset = prev_node.inst.addr_offset + prev_node.total_size + 1
            
            # round next_offset up to alignment
            child_node.inst.addr_offset = math.ceil(next_offset/alignment) * alignment
            
            prev_node = child_node