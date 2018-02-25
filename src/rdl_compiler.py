import sys

from antlr4 import FileStream, CommonTokenStream

from .parser.SystemRDLLexer import SystemRDLLexer
from .parser.SystemRDLParser import SystemRDLParser
from .compiler.ComponentVisitor import RootVisitor
from .compiler.errors import RDLParserErrorListener, RDLCompileError, ConsoleErrorPrinter
from .compiler.expressions import Expr
from .model import component as comp
from .model import walker
from .model.node import Node

class RDLCompiler:
    
    def __init__(self):
        self.visitor = RootVisitor()
        self.property_rules = self.visitor.PR
        self.root = None
        self.error_handler = ConsoleErrorPrinter()
    
    def compile_file(self, path):
        """
        Parse & compile the file specified by path
        Returns the Root meta-component
        
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
        
        return(self.root)
    
    def elaborate(self, top_def_name, parameters=None):
        """
        Elaborates the design with the specified component definition from
        the Root namespace as the top-level component.
        
        Returns the elaborated top-level component Node object
        """
        if(parameters is None):
            parameters = {}
        
        try:
            return(self._do_elaborate(top_def_name, parameters))
        except RDLCompileError as e:
            self.error_handler.handle_exception(e)
            sys.exit(1)
        
    def _do_elaborate(self, top_def_name, parameters):
        
        # Lookup top_def_name
        top_inst = self.root.comp_defs[top_def_name]
        
        # Create a top-level instance
        top_inst.is_instance = True
        top_inst.inst_name = top_def_name
        
        # TODO: Check if type is a reasonable elaboration target (Limit to addrmap, and regmap?)
        
        # Override parameters as needed
        if(len(parameters)):
            # TODO
            raise NotImplementedError
        
        top_node = Node.factory(top_inst, self)
        
        # Resolve all expressions
        walker.RDLWalker().walk(ElabExpressionsListener(), top_node)
        
        # TODO: Propagate defaults & addressing mode rules
        
        # TODO: Resolve addresses
        
        # TODO: Merge duplicate derived ComponentDef 
        
        # TODO: Uniquify derived ComponentDef type names
        
        # TODO: Validate design
        
        return(top_node)

#===============================================================================

class ElabExpressionsListener(walker.RDLListener):
    def enter_Component_before(self, node):
        
        # Evaluate instance object expressions
        if(issubclass(type(node.inst), comp.AddressableComponent)):
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
                
        elif(issubclass(type(node.inst), comp.VectorComponent)):
            if(issubclass(type(node.inst.width), Expr)):
                node.inst.width.resolve_expr_width()
                node.inst.width = node.inst.width.get_value()
            
            if(issubclass(type(node.inst.offset), Expr)):
                node.inst.offset.resolve_expr_width()
                node.inst.offset = node.inst.offset.get_value()
            
            if(issubclass(type(node.inst.msb), Expr)):
                node.inst.msb.resolve_expr_width()
                node.inst.msb = node.inst.msb.get_value()
            
            if(issubclass(type(node.inst.lsb), Expr)):
                node.inst.lsb.resolve_expr_width()
                node.inst.lsb = node.inst.lsb.get_value()
            
            if(issubclass(type(node.inst.reset_value), Expr)):
                node.inst.reset_value.resolve_expr_width()
                node.inst.reset_value = node.inst.reset_value.get_value()
        
        # Evaluate parameters
        # Result is not saved, but will catch evaluation errors if they exist
        for param in node.inst.parameters:
            if(issubclass(type(param.expr), Expr)):
                param.expr.resolve_expr_width()
                param.expr.get_value()
        
        # Evaluate component properties
        for prop_name, prop_value in node.inst.properties.items():
            if(issubclass(type(prop_value), Expr)):
                prop_value.resolve_expr_width()
                node.inst.properties[prop_name] = prop_value.get_value()
        