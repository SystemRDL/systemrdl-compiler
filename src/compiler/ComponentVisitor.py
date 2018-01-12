from antlr4 import *
import sys
import inspect

from ..parser.SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from .ExprVisitor import ExprVisitor
from .namespace import NamespaceRegistry
from .parameter import Parameter
from . import type_placeholders
from . import expressions

from ..model import component as comp
from ..model import rdl_types

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
            self.component.parameters = param_defs
        else:
            self.component = None
    
    #---------------------------------------------------------------------------
    # Component Definitions
    #---------------------------------------------------------------------------
    def visitComponent_body(self, ctx:SystemRDLParser.Component_bodyContext):
        self.NS.enter_scope()
        
        # Re-Load any parameters into the local scope
        for param in self.component.parameters:
            self.NS.register_element(param.name, param)
        
        # Visit all component elements.
        # Their visitors will apply changes to the current component
        self.visitChildren(ctx)
        
        self.NS.exit_scope()
        return(self.component)
    
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
            
            # Pass some temporary info to visitComponent_insts
            self._tmp = (comp_def, inst_type)
            self.visit(ctx.component_insts())
            
        return(None)
    
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
    
    #---------------------------------------------------------------------------
    # Component Instantiation
    #---------------------------------------------------------------------------
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        # Unpack instance def info from parent
        comp_def, inst_type = self._tmp
        
        # Get a dictionary of parameter assignments
        if(ctx.param_inst() is not None):
            param_assigns = self.visit(ctx.param_inst())
        else:
            param_assigns = {}
        
        if(len(param_assigns)):
            # Instance is overriding parameters.
            
            # Uniquify the comp_def by making a derived version
            comp_def = comp_def.create_derived_def()
            
            # Assign parameter overrides
            for param_name, assign_expr in param_assigns.items():
                # Lookup corresponding parameter in component
                for cparam in comp_def.parameters:
                    if(cparam.name == param_name):
                        param = cparam
                        break
                else:
                    raise ValueError("Parameter '%s' not found in definition for component '%s'" % (param_name, comp_def.name))
                
                # Override the value
                param.set_inst_value(assign_expr)
        
        # Do instantiations
        for inst in ctx.getTypedRuleContexts(SystemRDLParser.Component_instContext):
            # Pass some temporary info to visitComponent_inst
            self._tmp = comp_def, inst_type
            self.visit(inst)
        
        return(None)

    def visitField_inst_reset(self, ctx:SystemRDLParser.Field_inst_resetContext):
        return(self.get_instance_assignment(ctx))

    def visitInst_addr_fixed(self, ctx:SystemRDLParser.Inst_addr_fixedContext):
        return(self.get_instance_assignment(ctx))
    
    def visitInst_addr_stride(self, ctx:SystemRDLParser.Inst_addr_strideContext):
        return(self.get_instance_assignment(ctx))

    def visitInst_addr_align(self, ctx:SystemRDLParser.Inst_addr_alignContext):
        return(self.get_instance_assignment(ctx))
    
    def get_instance_assignment(self, ctx):
        """
        Gets the integer expression in any of the four instance assignment
        operators ('=' '@' '+=' '%=')
        """
        if(ctx is None):
            return(None)
        
        visitor = ExprVisitor(self.NS)
        expr = visitor.visit(ctx.expr())
        expr = expressions.AssignmentCast(expr, int)
        return(expr)
        
    def visitComponent_inst(self, ctx:SystemRDLParser.Component_instContext):
        # Unpack instance def info from parent
        comp_def, inst_type = self._tmp
        
        inst_name = ctx.ID().getText()
        
        # Get array or range suffix
        array_suffixes = []
        for as_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Array_suffixContext):
            array_suffixes.append(self.visit(as_ctx))
        
        if(ctx.range_suffix() is not None):
            range_suffix = self.visit(ctx.range_suffix())
        else:
            range_suffix = None
        
        # Check for invalid usage of array or range suffix
        if(type(comp_def) == comp.Field):
            # field can use a range, or a single array suffix
            if(len(array_suffixes) > 1):
                raise ValueError("Instances of a field can only use one array suffix")
        elif(type(comp_def) == comp.Signal):
            # signal can use a single array suffix
            if(len(array_suffixes) > 1):
                raise ValueError("Instances of a signal can only use one array suffix")
            if(range_suffix is not None):
                raise ValueError("Unexpected range suffix after signal instance")
        else:
            # Everything else can use any number of array suffixes
            if(range_suffix is not None):
                raise ValueError("Unexpected range suffix after instance")
        
        # Get all instance assignment expressions
        field_inst_reset = self.get_instance_assignment(ctx.field_inst_reset())
        inst_addr_fixed = self.get_instance_assignment(ctx.inst_addr_fixed())
        inst_addr_stride = self.get_instance_assignment(ctx.inst_addr_stride())
        inst_addr_align = self.get_instance_assignment(ctx.inst_addr_align())
        
        # Check for assignment expression incompatibility
        if(type(comp_def) == comp.Field):
            # field_inst_reset is the only thing allowed for fields
            # All others are invalid
            if(any([inst_addr_fixed, inst_addr_stride, inst_addr_align])):
                raise ValueError("Unexpected address allocation operator for field instance")
        elif(type(comp_def) == comp.Field):
            # none of these are allowed for signals
            if(field_inst_reset is not None):
                raise ValueError("Unexpected field reset assignment for non-field instance")
            if(any([inst_addr_fixed, inst_addr_stride, inst_addr_align])):
                raise ValueError("Unexpected address allocation operator for signal instance")
        else:
            # Otherwise, inst_addr_fixed and inst_addr_align are mutually exclusive
            if(field_inst_reset is not None):
                raise ValueError("Unexpected field reset assignment for non-field instance")
            
            if(all([inst_addr_fixed, inst_addr_align])):
                raise ValueError("Fixed address allocator '@' cannot be used along with an alignment allocator '%='")
        
        # Specifying stride is only allowed if an array suffix is used
        if((inst_addr_stride is not None) and (len(array_suffixes) == 0)):
            raise ValueError("Unexpected address stride allocator '%=' on non-array instance")
        
        # Assign instantiation info
        if(type(comp_def) in [comp.Field, comp.Signal]):
            inst = comp.VectorInst(comp_def)
            if(range_suffix is not None):
                inst.msb, inst.lsb = range_suffix
            if(len(array_suffixes) != 0):
                inst.width = array_suffixes[0]
        else:
            inst = comp.AddressableInst(comp_def)
            inst.addr_offset = inst_addr_fixed
            inst.addr_align = inst_addr_align
            if(len(array_suffixes) != 0):
                inst.is_array = True
                inst.array_size = array_suffixes
                inst.array_stride = inst_addr_stride
                
        if(inst_type == SystemRDLParser.EXTERNAL_kw):
            inst.external = True
        elif(inst_type == SystemRDLParser.INTERNAL_kw):
            inst.external = False
        
        inst.name = inst_name
        
        self.NS.register_element(inst_name, inst)
        
        if(self.component is not None):
            self.component.children.append(inst)
        
        return(None)
        
    #---------------------------------------------------------------------------
    # Parameters
    #---------------------------------------------------------------------------
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
        
        # Construct parameter type
        data_type_token = self.visit(ctx.data_type())
        param_data_type = self.datatype_from_token(data_type_token)
        if(ctx.array_type_suffix() is None):
            # Non-array type
            param_type = param_data_type
        else:
            # Array-like type
            param_type = type_placeholders.Array(param_data_type)
        
        # Get parameter name
        param_name = ctx.ID().getText()
        
        # Get expression for parameter default, if any
        if(ctx.expr() is not None):
            visitor = ExprVisitor(self.NS)
            default_expr = visitor.visit(ctx.expr())
        else:
            default_expr = None
        
        # Create Parameter object
        param = Parameter(param_type, param_name, default_expr)
        
        # Register it in the parameter def namespace scope
        self.NS.register_element(param_name, param)
        
        return(param)
    
    def visitParam_inst(self, ctx:SystemRDLParser.Param_instContext):
        param_assigns = {}
        for assignment in ctx.getTypedRuleContexts(SystemRDLParser.Param_assignmentContext):
            param_name, assign_expr = self.visit(assignment)
            
            if(param_name in param_assigns):
                raise ValueError("Duplicate parameter assignment to '%s'" % param_name)
            
            param_assigns[param_name] = assign_expr
        return(param_assigns)

    def visitParam_assignment(self, ctx:SystemRDLParser.Param_assignmentContext):
        param_name = ctx.ID().getText()
        
        visitor = ExprVisitor(self.NS)
        assign_expr = visitor.visit(ctx.expr())
        return(param_name, assign_expr)
    
    #---------------------------------------------------------------------------
    # Array and Range suffixes
    #---------------------------------------------------------------------------
    def visitRange_suffix(self, ctx:SystemRDLParser.Range_suffixContext):
        visitor = ExprVisitor(self.NS)
        expr1 = visitor.visit(ctx.expr(0))
        expr1 = expressions.AssignmentCast(expr1, int)
        expr2 = visitor.visit(ctx.expr(1))
        expr2 = expressions.AssignmentCast(expr2, int)
        
        return(expr1, expr2)

    def visitArray_suffix(self, ctx:SystemRDLParser.Array_suffixContext):
        visitor = ExprVisitor(self.NS)
        expr = visitor.visit(ctx.expr())
        expr = expressions.AssignmentCast(expr, int)
        return(expr)
    
    #---------------------------------------------------------------------------
    # Type Handling
    #---------------------------------------------------------------------------
    _DataType_Map = {
        SystemRDLParser.BIT_kw              : type_placeholders.Bit,
        SystemRDLParser.LONGINT_kw          : int,
        SystemRDLParser.ACCESSTYPE_kw       : rdl_types.AccessType,
        SystemRDLParser.ADDRESSINGTYPE_kw   : rdl_types.AddressingType,
        SystemRDLParser.ONREADTYPE_kw       : rdl_types.OnReadType,
        SystemRDLParser.ONWRITETYPE_kw      : rdl_types.OnWriteType,
        SystemRDLParser.STRING_kw           : str,
        SystemRDLParser.BOOLEAN_kw          : bool
    }
    def datatype_from_token(self, token):
        """
        Given a SystemRDLParser token, lookup the type
        This only includes types under the "data_type" grammar rule
        """
        
        if(token.type == SystemRDLParser.ID):
            # Is an identifier for either an enum or struct type
            
            typ = self.NS.lookup_type(token.text)
            if(typ is None):
                raise ValueError("Type '%s' is not defined" % token.text)
            
            if(inspect.isclass(typ)):
                if(issubclass(typ, rdl_types.UserEnum) or issubclass(typ, rdl_types.UserStruct)):
                    return(typ)
                else:
                    raise ValueError("Type '%s' is not a struct or enum" % token.text)
            else:
                raise ValueError("Type '%s' is not a struct or enum" % token.text)
            
        else:
            return(self._DataType_Map[token.type])
        

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

