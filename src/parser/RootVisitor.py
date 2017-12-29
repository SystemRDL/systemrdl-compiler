
from antlr4 import *

from .SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor

class RootVisitor(BaseVisitor):

    # Visit a parse tree produced by SystemRDLParser#component_named_def.
    def visitComponent_named_def(self, ctx:SystemRDLParser.Component_named_defContext):
        print("named", self.visit(ctx.component_type()))
        return self.visitChildren(ctx)
        
    # Visit a parse tree produced by SystemRDLParser#component_anon_def.
    def visitComponent_anon_def(self, ctx:SystemRDLParser.Component_anon_defContext):
        print("anon", self.visit(ctx.component_type()))
        return self.visitChildren(ctx)

