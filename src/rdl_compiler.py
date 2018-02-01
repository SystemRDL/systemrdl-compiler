import sys

from antlr4 import FileStream, CommonTokenStream

from .parser.SystemRDLLexer import SystemRDLLexer
from .parser.SystemRDLParser import SystemRDLParser
from .compiler.ComponentVisitor import RootVisitor
from .compiler.errors import RDLParserErrorListener, RDLCompileError, ConsoleErrorPrinter
from .compiler.expressions import Expr
from .model import component as comp
from .util import walker

class RDLCompiler:
    
    def __init__(self):
        self.visitor = RootVisitor()
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
    
    def elaborate(self, top_def_name, parameters={}):
        """
        Elaborates the design with the specified component definition from
        the Root namespace as the top-level component.
        
        Returns the elaborated top-level component Inst object
        """
        try:
            return(self._do_elaborate(top_def_name, parameters))
        except RDLCompileError as e:
            self.error_handler.handle_exception(e)
            sys.exit(1)
        
    def _do_elaborate(self, top_def_name, parameters):
        
        # Lookup top_def_name
        top_def = self.root.comp_defs[top_def_name]
        
        # Create a top-level instance
        top_inst = top_def.INST_TYPE(top_def)
        top_inst.name = top_def.name
        
        # Override parameters as needed
        if(len(parameters)):
            # TODO
            raise NotImplementedError
        
        # Resolve all expressions
        walker.RDLWalker().walk(ElabExpressionsListener(), top_inst)
        
        # TODO: Propagate defaults & addressing mode rules
        
        # TODO: Resolve addresses
        
        # TODO: Merge duplicate derived ComponentDef 
        
        # TODO: Uniquify derived ComponentDef type names
        
        # TODO: Validate design
        
        return(top_inst)

#===============================================================================

class ElabExpressionsListener(walker.RDLListener):
    def enter_Component_before(self, ctx):
        
        # Evaluate instance object expressions
        if(issubclass(type(ctx.inst), comp.AddressableInst)):
            if(issubclass(type(ctx.inst.addr_offset), Expr)):
                ctx.inst.addr_offset.resolve_expr_width()
                ctx.inst.addr_offset = ctx.inst.addr_offset.get_value()
            
            if(issubclass(type(ctx.inst.addr_align), Expr)):
                ctx.inst.addr_align.resolve_expr_width()
                ctx.inst.addr_align = ctx.inst.addr_align.get_value()
            
            if(ctx.inst.array_size is not None):
                for i in range(len(ctx.inst.array_size)):
                    if(issubclass(type(ctx.inst.array_size[i]), Expr)):
                        ctx.inst.array_size[i].resolve_expr_width()
                        ctx.inst.array_size[i] = ctx.inst.array_size[i].get_value()
            
            if(issubclass(type(ctx.inst.array_stride), Expr)):
                ctx.inst.array_stride.resolve_expr_width()
                ctx.inst.array_stride = ctx.inst.array_stride.get_value()
                
        elif(issubclass(type(ctx.inst), comp.VectorInst)):
            if(issubclass(type(ctx.inst.width), Expr)):
                ctx.inst.width.resolve_expr_width()
                ctx.inst.width = ctx.inst.width.get_value()
            
            if(issubclass(type(ctx.inst.offset), Expr)):
                ctx.inst.offset.resolve_expr_width()
                ctx.inst.offset = ctx.inst.offset.get_value()
            
            if(issubclass(type(ctx.inst.msb), Expr)):
                ctx.inst.msb.resolve_expr_width()
                ctx.inst.msb = ctx.inst.msb.get_value()
            
            if(issubclass(type(ctx.inst.lsb), Expr)):
                ctx.inst.lsb.resolve_expr_width()
                ctx.inst.lsb = ctx.inst.lsb.get_value()
            
            if(issubclass(type(ctx.inst.reset_value), Expr)):
                ctx.inst.reset_value.resolve_expr_width()
                ctx.inst.reset_value = ctx.inst.reset_value.get_value()
        
        # Evaluate parameters
        # Result is not saved, but will catch evaluation errors if they exist
        for param in ctx.comp.parameters:
            if(issubclass(type(param.expr), Expr)):
                param.expr.resolve_expr_width()
                param.expr.get_value()
        
        # Evaluate component properties
        # TODO