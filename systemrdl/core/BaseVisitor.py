
from antlr4 import *

from ..parser.SystemRDLParser import SystemRDLParser
from ..parser.SystemRDLVisitor import SystemRDLVisitor

from .namespace import NamespaceRegistry
from .properties import PropertyRuleBook

class BaseVisitor(SystemRDLVisitor):
    
    def __init__(self, compiler):
        self.compiler = compiler
        self.msg = compiler.msg

    #---------------------------------------------------------------------------
    # Keyword passthrough visitors
    #---------------------------------------------------------------------------
    
    # It is convenient to be able to group commonly-used sets of tokens in the
    # grammar.
    # These visitors propagate the original tokens all the way back up to the
    # visitor that actually needs to know which keyword was used.
    
    def passthru_kw_token(self, ctx):
        if(ctx.kw is not None):
            return(ctx.kw)
        else:
            return(self.visitChildren(ctx))
        
    def visitComponent_inst_type(self, ctx:SystemRDLParser.Component_inst_typeContext):
        return(self.passthru_kw_token(ctx))

    def visitComponent_type(self, ctx:SystemRDLParser.Component_typeContext):
        return(self.passthru_kw_token(ctx))

    def visitComponent_type_primary(self, ctx:SystemRDLParser.Component_type_primaryContext):
        return(self.passthru_kw_token(ctx))
    
    def visitData_type(self, ctx:SystemRDLParser.Data_typeContext):
        return(self.passthru_kw_token(ctx))

    def visitBasic_data_type(self, ctx:SystemRDLParser.Basic_data_typeContext):
        return(self.passthru_kw_token(ctx))
    
    def visitProp_keyword(self, ctx:SystemRDLParser.Prop_keywordContext):
        return(self.passthru_kw_token(ctx))
    
    def visitProp_mod(self, ctx:SystemRDLParser.Prop_modContext):
        return(self.passthru_kw_token(ctx))
        
    