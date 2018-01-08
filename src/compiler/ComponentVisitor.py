from antlr4 import *

from ..parser.SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from .ExprVisitor import ExprVisitor
from .namespace import NamespaceRegistry
from .parameter import Parameter

from ..model import component as comp

#===============================================================================
# Base visitor
#===============================================================================
class ComponentVisitor(BaseVisitor):
    comp_type = None
    
    def __init__(self, ns=None, def_name=None, param_defs=[]):
        if(ns is None):
            self.NS = NamespaceRegistry()
        else:
            self.NS = ns
        
        if(self.comp_type is not None):
            self.component = self.comp_type()
            self.component.name = def_name
        else:
            self.component = None
    
    #---------------------------------------------------------------------------
    # Component Definitions & Instantiations
    #---------------------------------------------------------------------------
    def visitComponent_def(self, ctx:SystemRDLParser.Component_defContext):
        """
        Create, and possibly instantiate a component
        """
        
        # Get definition. Returns ComponentDef
        if(ctx.component_anon_def() is not None):
            comp_def = self.visit(ctx.component_anon_def())
        elif(ctx.component_named_def() is not None):
            comp_def = self.visit(ctx.component_named_def())
        else:
            raise RuntimeError
        
        if(ctx.component_insts() is not None):
            # Component is instantiated one or more times
            if(ctx.component_inst_type() is not None):
                inst_type = self.visit(ctx.component_inst_type())
            else:
                inst_type = None
            
            self._tmp = (comp_def, inst_type)
            self.visit(ctx.component_insts())
            
        return(None)
    
    
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        comp_def, inst_type = self._tmp
        print("TODO: Instantiate stuff")
    
    
    def visitComponent_named_def(self, ctx:SystemRDLParser.Component_named_defContext):
        type_token = self.visit(ctx.component_type())
        
        def_name = ctx.ID().getText()
        # Get any parameters for the component
        if(ctx.param_def() is not None):
            param_defs = self.visit(ctx.param_def())
        else:
            param_defs = []
        
        # Recurse into the component definition body
        body = ctx.component_body()
        comp_def = self.define_component(body, type_token, def_name, param_defs)
        
        # Since the definition is named, register it with the namespace
        self.NS.register_type(def_name, comp_def)
        
        return(comp_def)
    
    
    def visitComponent_anon_def(self, ctx:SystemRDLParser.Component_anon_defContext):
        type_token = self.visit(ctx.component_type())
        
        body = ctx.component_body()
        comp_def = self.define_component(body, type_token, None, [])
        
        return(comp_def)
    
    
    _CompType_Map = {
        SystemRDLParser.FIELD_kw    : comp.Field,
        SystemRDLParser.REG_kw      : comp.Reg,
        SystemRDLParser.REGFILE_kw  : comp.Regfile,
        SystemRDLParser.ADDRMAP_kw  : comp.Addrmap,
        SystemRDLParser.SIGNAL_kw   : comp.Signal,
        SystemRDLParser.MEM_kw      : comp.Mem
    }
    def define_component(self, body, type_token, def_name, param_defs):
        """
        Given component definition, recurse to another ComponentVisitor
        to define a new component
        """
        for subclass in ComponentVisitor.__subclasses__():
            if(subclass.comp_type == self._CompType_Map[type_token.type]):
                visitor = subclass(self.NS, def_name, param_defs)
                return(visitor.visit(body))
        else:
            raise RuntimeError
            
    def visitParam_def(self, ctx:SystemRDLParser.Param_defContext):
        """
        Parameter Definition block
        """
        self.NS.enter_scope()
        
        param_defs = []
        for elem in ctx.getTypedRuleContexts(SystemRDLParser.Param_def_elemContext):
            param_def = self.visit(elem)
            param_defs.append(param_def)
        
        self.NS.exit_scope()
        return(param_defs)
    
    def visitParam_def_elem(self, ctx:SystemRDLParser.Param_def_elemContext):
        """
        Individual parameter definition elements
        """
        param_data_type = self.visit(ctx.data_type())
        if(ctx.array_type_suffix() is None):
            # Non-array type
            param_type = None
            raise NotImplementedError("TODO")
        else:
            # Array-like type
            param_type = None
            raise NotImplementedError("TODO")
        
        param_name = ctx.ID().getText()
        
        if(ctx.expr() is not None):
            visitor = ExprVisitor(self.NS)
            default_expr = visitor.visit(ctx.expr())
        else:
            default_expr = None
        
        return(Parameter(param_type, param_name, default_expr))
    
    def visitComponent_body(self, ctx:SystemRDLParser.Component_bodyContext):
        self.NS.enter_scope()
        
        # Visit all component elements.
        # Their visitors will apply changes to the current component
        self.visitChildren(ctx)
        
        self.NS.exit_scope()
        return(self.component)



#===============================================================================
# Field Component visitor
#===============================================================================
class FieldComponentVisitor(ComponentVisitor):
    comp_type = comp.Field

#===============================================================================
# Reg Component visitor
#===============================================================================
class RegComponentVisitor(ComponentVisitor):
    comp_type = comp.Reg

#===============================================================================
# Regfile Component visitor
#===============================================================================
class RegfileComponentVisitor(ComponentVisitor):
    comp_type = comp.Regfile

#===============================================================================
# Addrmap Component visitor
#===============================================================================
class AddrmapComponentVisitor(ComponentVisitor):
    comp_type = comp.Addrmap

#===============================================================================
# Mem Component visitor
#===============================================================================
class MemComponentVisitor(ComponentVisitor):
    comp_type = comp.Mem

#===============================================================================
# Signal Component visitor
#===============================================================================
class SignalComponentVisitor(ComponentVisitor):
    comp_type = comp.Signal

