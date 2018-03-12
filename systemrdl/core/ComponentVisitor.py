from antlr4 import *
import inspect
from copy import deepcopy
from collections import OrderedDict

from ..parser.SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from .ExprVisitor import ExprVisitor
from .parameter import Parameter
from . import type_placeholders
from . import expressions
from ..errors import RDLCompileError, RDLNotSupportedYet

from .. import component as comp
from .. import rdltypes

#===============================================================================
# Base visitor
#===============================================================================
class ComponentVisitor(BaseVisitor):
    comp_type = None
    
    def __init__(self, ns, pr, def_name=None, param_defs=None):
        super().__init__(ns, pr)
        
        self.component = self.comp_type()
        self.component.type_name = def_name
        if(param_defs is None):
            self.component.parameters = []
        else:
            self.component.parameters = param_defs
        
        # Scratchpad of local property assignments encountered in body of component
        # format is:
        #   {
        #       prop_name : (prop_token, prop_rhs)
        #   }
        self.property_dict = OrderedDict()
        
        # Scratchpad of dynamic property assignments encountered in body of component
        # format is:
        #   {
        #       target_inst : {
        #           prop_name : (prop_token, prop_rhs)
        #       }
        #   }
        self.dynamic_property_dict = OrderedDict()
        
        # Scratchpad to pass stuff down between visitor functions
        self._tmp = None
    
    #---------------------------------------------------------------------------
    # Component Definitions
    #---------------------------------------------------------------------------
    def visitComponent_body(self, ctx:SystemRDLParser.Component_bodyContext):
        self.NS.enter_scope()
        
        self.component.def_err_ctx = ctx
        
        # Re-Load any parameters into the local scope
        for param in self.component.parameters:
            self.NS.register_element(param.name, param, None)
        
        # Visit all component elements.
        # Their visitors will apply changes to the current component
        self.visitChildren(ctx)
        
        self.apply_local_properties()
        self.apply_dynamic_properties()
        
        self.NS.exit_scope()
        return(self.component)
    
    def visitComponent_def(self, ctx:SystemRDLParser.Component_defContext):
        """
        Create, and possibly instantiate a component
        """
        
        # Get definition. Returns Component
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
        
        self.check_comp_def_allowed(type_token)
        
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
        self.NS.register_type(def_name, comp_def, ctx.ID())
        
        return(comp_def)
    
    
    def visitComponent_anon_def(self, ctx:SystemRDLParser.Component_anon_defContext):
        type_token = self.visit(ctx.component_type())
        
        self.check_comp_def_allowed(type_token)
        
        body = ctx.component_body()
        comp_def = self.define_component(body, type_token, None, [])
        
        return(comp_def)
    
    def check_comp_def_allowed(self, type_token):
        pass
    
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
                visitor = subclass(self.NS, self.PR, def_name, param_defs)
                return(visitor.visit(body))
        raise RuntimeError
    
    #---------------------------------------------------------------------------
    # Component Instantiation
    #---------------------------------------------------------------------------
    def visitExplicit_component_inst(self, ctx:SystemRDLParser.Explicit_component_instContext):
        if(ctx.component_inst_type() is not None):
            inst_type = self.visit(ctx.component_inst_type())
        else:
            inst_type = None
        
        if(ctx.component_inst_alias() is not None):
            raise NotImplementedError
        
        comp_def = self.component_def_from_token(ctx.ID())
        
        # Pass some temporary info to visitComponent_insts
        self._tmp = (comp_def, inst_type)
        self.visit(ctx.component_insts())
        
        return(None)

    def visitComponent_inst_alias(self, ctx:SystemRDLParser.Component_inst_aliasContext):
        raise NotImplementedError
    
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        # Unpack instance def info from parent
        comp_def, inst_type = self._tmp
        
        if(comp_def.type_name is not None):
            # Instantiating a named definition.
            # Make a copy of the component def to preserve original definition
            comp_inst_template = deepcopy(comp_def)
            comp_inst_template.original_def = comp_def
        else:
            comp_inst_template = comp_def
        
        # Get a dictionary of parameter assignments
        if(ctx.param_inst() is not None):
            param_assigns = self.visit(ctx.param_inst())
        else:
            param_assigns = {}
        
        # Assign parameter overrides, if any
        for param_name, assign_expr, err_ctx in param_assigns.items():
            # Lookup corresponding parameter in component
            for comp_param in comp_inst_template.parameters:
                if(comp_param.name == param_name):
                    param = comp_param
                    break
            else:
                raise RDLCompileError(
                    "Parameter '%s' not found in definition for component '%s'" 
                    % (param_name, comp_inst_template.name),
                    err_ctx
                )
            
            # Override the value
            assign_expr = expressions.AssignmentCast(err_ctx, assign_expr, param.param_type)
            assign_expr.predict_type()
            param.expr = assign_expr
        
        # Do instantiations
        for inst in ctx.getTypedRuleContexts(SystemRDLParser.Component_instContext):
            # Make a copy of the template so that the instance is unique
            comp_inst = deepcopy(comp_inst_template)
            
            # Pass some temporary info to visitComponent_inst
            self._tmp = comp_inst, inst_type
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
        
        visitor = ExprVisitor(self.NS, self.PR, self.component)
        expr = visitor.visit(ctx.expr())
        expr = expressions.AssignmentCast(ctx.op, expr, int)
        expr.predict_type()
        return(expr)
        
    def visitComponent_inst(self, ctx:SystemRDLParser.Component_instContext):
        # Unpack instance def info from parent
        comp_inst, inst_type = self._tmp
        
        inst_name = ctx.ID().getText()
        comp_inst.inst_name = inst_name
        comp_inst.inst_err_ctx = ctx.ID()
        
        # Get array or range suffix
        array_suffixes = []
        for as_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Array_suffixContext):
            array_suffixes.append(self.visit(as_ctx))
        
        if(ctx.range_suffix() is not None):
            range_suffix = self.visit(ctx.range_suffix())
        else:
            range_suffix = None
        
        # Check for invalid usage of array or range suffix
        if(type(comp_inst) == comp.Field):
            # field can use a range, or a single array suffix
            if(len(array_suffixes) > 1):
                raise RDLCompileError(
                    "Instances of a field can only use one array suffix",
                    ctx.array_suffix(1)
                )
        elif(type(comp_inst) == comp.Signal):
            # signal can use a single array suffix
            if(len(array_suffixes) > 1):
                raise RDLCompileError(
                    "Instances of a signal can only use one array suffix",
                    ctx.array_suffix(1)
                )
            if(range_suffix is not None):
                raise RDLCompileError(
                    "Unexpected range suffix after signal instance",
                    ctx.range_suffix()
                )
        else:
            # Everything else can use any number of array suffixes
            if(range_suffix is not None):
                raise RDLCompileError(
                    "Unexpected range suffix after instance",
                    ctx.range_suffix()
                )
        
        # Get all instance assignment expressions
        field_inst_reset = self.get_instance_assignment(ctx.field_inst_reset())
        inst_addr_fixed = self.get_instance_assignment(ctx.inst_addr_fixed())
        inst_addr_stride = self.get_instance_assignment(ctx.inst_addr_stride())
        inst_addr_align = self.get_instance_assignment(ctx.inst_addr_align())
        
        # Check for assignment expression incompatibility
        if(type(comp_inst) in [comp.Field, comp.Signal]):
            err_ctx = None
            if(inst_addr_fixed is not None):
                err_ctx = ctx.inst_addr_fixed().start
            elif(inst_addr_stride is not None):
                err_ctx = ctx.inst_addr_stride().start
            elif(inst_addr_align is not None):
                err_ctx = ctx.inst_addr_align().start
            
            if(err_ctx is not None):
                raise RDLCompileError(
                    "Unexpected address allocation operator for non-addressable instance",
                    err_ctx
                )
            
        if(type(comp_inst) == comp.Signal):
            # none of these are allowed for signals
            if(field_inst_reset is not None):
                raise RDLCompileError(
                    "Unexpected field reset assignment for non-field instance",
                    ctx.field_inst_reset().start
                )
        elif(type(comp_inst) != comp.Field):
            # Otherwise, inst_addr_fixed and inst_addr_align are mutually exclusive
            if(all([inst_addr_fixed, inst_addr_align])):
                raise RDLCompileError(
                    "Fixed address allocator '@' cannot be used along with an alignment allocator '%='",
                    ctx.inst_addr_fixed().start
                )
            
            if(field_inst_reset is not None):
                raise RDLCompileError(
                    "Unexpected field reset assignment for non-field instance",
                    ctx.field_inst_reset().start
                )
            
        
        # Specifying stride is only allowed if an array suffix is used
        if((inst_addr_stride is not None) and (len(array_suffixes) == 0)):
            raise RDLCompileError(
                "Unexpected address stride allocator '%=' on non-array instance",
                ctx.inst_addr_stride().start
            )
        
        # Do instantiation
        comp_inst.is_instance = True
        if(issubclass(type(comp_inst), comp.VectorComponent)):
            if(range_suffix is not None):
                comp_inst.msb, comp_inst.lsb = range_suffix
            if(len(array_suffixes) != 0):
                comp_inst.width = array_suffixes[0]
            comp_inst.reset_value = field_inst_reset
        elif(issubclass(type(comp_inst), comp.AddressableComponent)):
            comp_inst.addr_offset = inst_addr_fixed
            comp_inst.addr_align = inst_addr_align
            if(len(array_suffixes) != 0):
                comp_inst.is_array = True
                comp_inst.array_dimensions = array_suffixes
                comp_inst.array_stride = inst_addr_stride
        else:
            raise RuntimeError
        
        if(inst_type == SystemRDLParser.EXTERNAL_kw):
            comp_inst.external = True
        elif(inst_type == SystemRDLParser.INTERNAL_kw):
            comp_inst.external = False
        
        self.component.children.append(comp_inst)
        
        self.NS.register_element(inst_name, comp_inst, ctx.ID())
        
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
            visitor = ExprVisitor(self.NS, self.PR, self.component)
            default_expr = visitor.visit(ctx.expr())
            default_expr = expressions.AssignmentCast(ctx.ID(), default_expr, param_type)
            default_expr.predict_type()
        else:
            default_expr = None
        
        # Create Parameter object
        param = Parameter(param_type, param_name, default_expr)
        
        # Register it in the parameter def namespace scope
        self.NS.register_element(param_name, param, ctx.ID())
        
        return(param)
    
    def visitParam_inst(self, ctx:SystemRDLParser.Param_instContext):
        param_assigns = {}
        for assignment in ctx.getTypedRuleContexts(SystemRDLParser.Param_assignmentContext):
            param_name, assign_expr = self.visit(assignment)
            
            if(param_name in param_assigns):
                raise RDLCompileError(
                    "Duplicate assignment to parameter '%s'" % param_name,
                    assignment.ID()
                )
            
            param_assigns[param_name] = (assign_expr, assignment.ID())
        return(param_assigns)

    def visitParam_assignment(self, ctx:SystemRDLParser.Param_assignmentContext):
        param_name = ctx.ID().getText()
        
        visitor = ExprVisitor(self.NS, self.PR, self.component)
        # Note: AssignmentCast is handled in the visitComponent_insts Visitor
        assign_expr = visitor.visit(ctx.expr())
        return(param_name, assign_expr)
    
    #---------------------------------------------------------------------------
    # Property Assignments
    #---------------------------------------------------------------------------
    def visitLocal_property_assignment(self, ctx:SystemRDLParser.Local_property_assignmentContext):
        
        default = (ctx.DEFAULT_kw() is not None)
        
        # _tmp is used to store assignment target depth so that it can be passed
        # to the ExprVisitor. This is 0 for local property assignments
        self._tmp = 0
        
        if(ctx.normal_prop_assign() is not None):
            prop_token, prop_name, rhs = self.visit(ctx.normal_prop_assign())
        elif(ctx.encode_prop_assign() is not None):
            prop_token, prop_name, rhs = self.visit(ctx.encode_prop_assign())
        elif(ctx.prop_mod_assign() is not None):
            prop_mod_token, prop_mod = self.visit(ctx.prop_mod_assign())
            # TODO: Set intr property to True and apply prop_mod
            raise NotImplementedError
        else:
            raise RuntimeError
        
        if(default):
            self.NS.register_default_property(prop_name, (prop_token, rhs), prop_token)
        else:
            if(prop_name in self.property_dict):
                raise RDLCompileError(
                    "Property '%s' was already assigned in this scope" % prop_name,
                    prop_token
                )
            else:
                self.property_dict[prop_name] = (prop_token, rhs)
        
    def visitDynamic_property_assignment(self, ctx:SystemRDLParser.Dynamic_property_assignmentContext):
        
        # List of component instance names in the hierarchical path
        name_tokens = self.visit(ctx.instance_ref())
        
        # Keep track of assignment target's depth.
        # This needs to be passed to the ExprVisitor that generates RHS in order
        # to properly evaluate component references
        self._tmp = len(name_tokens)
        
        if(ctx.normal_prop_assign() is not None):
            prop_token, prop_name, rhs = self.visit(ctx.normal_prop_assign())
        elif(ctx.encode_prop_assign() is not None):
            prop_token, prop_name, rhs = self.visit(ctx.encode_prop_assign())
        else:
            raise RuntimeError
        
        # Lookup component instance being assigned
        target_inst = self.component
        for name_token in name_tokens:
            inst_name = name_token.getText()
            target_inst = target_inst.get_child_by_name(inst_name)
            if(target_inst is None):
                # Not found!
                raise RDLCompileError(
                    "Could not resolve hierarchical reference to '%s'" % inst_name,
                    name_token
                )
        
        # Add assignment to dynamic_property_dict
        target_inst_dict = self.dynamic_property_dict.get(target_inst, OrderedDict())
        if(prop_name in target_inst_dict):
            raise RDLCompileError(
                "Property '%s' was already assigned to component '%s' from within this scope"
                    % (prop_name, name_tokens[-1].getText()),
                prop_token
            )
        else:
            target_inst_dict[prop_name] = (prop_token, rhs)
        self.dynamic_property_dict[target_inst] = target_inst_dict
        
    
    def visitInstance_ref(self, ctx:SystemRDLParser.Instance_refContext):
        name_tokens = []
        for ref_elem in ctx.getTypedRuleContexts(SystemRDLParser.Instance_ref_elementContext):
            name_tokens.append(self.visit(ref_elem))
        return(name_tokens)
        
    def visitInstance_ref_element(self, ctx:SystemRDLParser.Instance_ref_elementContext):
        name_token = ctx.ID()
        
        # Intentionally not supporting array references in dynamic assignments
        # due to heterogeneous array complications.
        for as_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Array_suffixContext):
            raise RDLCompileError(
                "Use of array suffixes in dynamic property assignments is not supported",
                as_ctx
            )
        
        return(name_token)
        
    def visitNormal_prop_assign(self, ctx:SystemRDLParser.Normal_prop_assignContext):
        
        # Get property string
        if(ctx.prop_keyword() is not None):
            prop_token = self.visit(ctx.prop_keyword())
            prop_name = prop_token.text
        else:
            prop_token = ctx.ID()
            prop_name = prop_token.getText()
        
        if(ctx.prop_assignment_rhs() is not None):
            rhs = self.visit(ctx.prop_assignment_rhs())
        else:
            # No RHS implies "true" assignment
            rhs = True
        
        return(prop_token, prop_name, rhs)
    
    def visitEncode_prop_assign(self, ctx:SystemRDLParser.Encode_prop_assignContext):
        # Get property string
        prop_token = ctx.ENCODE_kw()
        prop_name = prop_token.getText()
        
        enum_name = ctx.ID().getText()
        
        enum_type = self.NS.lookup_type(enum_name)
        if(enum_type is None):
            raise RDLCompileError(
                "Type '%s' is not defined" % enum_name,
                ctx.ID()
            )
        if(not(inspect.isclass(enum_type) and (issubclass(enum_type, rdltypes.UserEnum)))):
            raise RDLCompileError(
                "Assignment to encode property is not an enum type",
                ctx.ID()
            )
        rhs = enum_type
        
        return(prop_token, prop_name, rhs)
        
        
    def visitProp_mod_assign(self, ctx:SystemRDLParser.Prop_mod_assignContext):
        prop_mod_token = self.visit(ctx.prop_mod())
        prop_mod = prop_mod_token.text
        
        intr_token = ctx.ID()
        
        if(intr_token.getText() != "intr"):
            raise RDLCompileError(
                "extraneous input '%s' expecting 'intr'" % intr_token.getText(),
                intr_token
            )

        return(prop_mod_token, prop_mod)
        
    def visitProp_assignment_rhs(self, ctx:SystemRDLParser.Prop_assignment_rhsContext):
        target_depth = self._tmp
        
        if(ctx.expr() is not None):
            visitor = ExprVisitor(self.NS, self.PR, self.component, target_depth)
            rhs = visitor.visit(ctx.expr())
        else:
            rhs = self.visit(ctx.precedencetype_literal())
            
        return(rhs)
    
    def visitPrecedencetype_literal(self, ctx:SystemRDLParser.Precedencetype_literalContext):
        return(rdltypes.PrecedenceType[ctx.kw.text])
    
    def apply_local_properties(self):
        
        # First, apply default property assignments inherited from namespace
        for prop_name, (prop_token, prop_rhs) in self.NS.get_default_properties(type(self.component), self.PR).items():
            rule = self.PR.lookup_property(prop_name)
            if(rule is None):
                raise RDLCompileError(
                    "Unrecognized property '%s'" % prop_name,
                    prop_token
                )
            rule.assign_value(self.component, prop_rhs, prop_token)
        
        # Apply locally-assigned properties
        mutex_bins = {}
        for prop_name, (prop_token, prop_rhs) in self.property_dict.items():
            rule = self.PR.lookup_property(prop_name)
            if(rule is None):
                raise RDLCompileError(
                    "Unrecognized property '%s'" % prop_name,
                    prop_token
                )
            
            # Check for mutex collisions
            if(rule.mutex_group is not None):
                # Is mutually exclusive with other props. Check for collision
                if(rule.mutex_group in mutex_bins):
                    # Already saw something in this mutex group
                    raise RDLCompileError(
                        "Properties '%s' and '%s' cannot be assigned in the same component" % (prop_name, mutex_bins[rule.mutex_group]),
                        prop_token
                    )
                else:
                    mutex_bins[rule.mutex_group] = prop_name
        
            # Apply property
            rule.assign_value(self.component, prop_rhs, prop_token)
    
    def apply_dynamic_properties(self):
        
        for target_inst, target_inst_dict in self.dynamic_property_dict.items():
            mutex_bins = {}
            for prop_name, (prop_token, prop_rhs) in target_inst_dict.items():
                rule = self.PR.lookup_property(prop_name)
                if(rule is None):
                    raise RDLCompileError(
                        "Unrecognized property '%s'" % prop_name,
                        prop_token
                    )
                
                # Is dynamic assignment allowed?
                if(rule.dyn_assign_allowed == False):
                    raise RDLCompileError(
                        "Dynamic assignment to property '%s' is not allowed" % prop_name,
                        prop_token
                    )
                
                # Check for mutex collisions
                if(rule.mutex_group is not None):
                    # Is mutually exclusive with other props. Check for collision
                    if(rule.mutex_group in mutex_bins):
                        # Already saw something in this mutex group
                        raise RDLCompileError(
                            "Properties '%s' and '%s' cannot be assigned in the same component" % (prop_name, mutex_bins[rule.mutex_group]),
                            prop_token
                        )
                    else:
                        mutex_bins[rule.mutex_group] = prop_name
                
                # Apply property
                rule.assign_value(target_inst, prop_rhs, prop_token)

    #---------------------------------------------------------------------------
    # Array and Range suffixes
    #---------------------------------------------------------------------------
    def visitRange_suffix(self, ctx:SystemRDLParser.Range_suffixContext):
        visitor = ExprVisitor(self.NS, self.PR, self.component)
        expr1 = visitor.visit(ctx.expr(0))
        expr1 = expressions.AssignmentCast(ctx.expr(0), expr1, int)
        expr1.predict_type()
        
        expr2 = visitor.visit(ctx.expr(1))
        expr2 = expressions.AssignmentCast(ctx.expr(1), expr2, int)
        expr2.predict_type()
        
        return(expr1, expr2)

    def visitArray_suffix(self, ctx:SystemRDLParser.Array_suffixContext):
        visitor = ExprVisitor(self.NS, self.PR, self.component)
        expr = visitor.visit(ctx.expr())
        expr = expressions.AssignmentCast(ctx.expr(), expr, int)
        expr.predict_type()
        return(expr)
    
    #---------------------------------------------------------------------------
    # Type Handling
    #---------------------------------------------------------------------------
    _DataType_Map = {
        SystemRDLParser.BIT_kw              : int,
        SystemRDLParser.LONGINT_kw          : int,
        SystemRDLParser.ACCESSTYPE_kw       : rdltypes.AccessType,
        SystemRDLParser.ADDRESSINGTYPE_kw   : rdltypes.AddressingType,
        SystemRDLParser.ONREADTYPE_kw       : rdltypes.OnReadType,
        SystemRDLParser.ONWRITETYPE_kw      : rdltypes.OnWriteType,
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
                raise RDLCompileError(
                    "Type '%s' is not defined" % token.text,
                    token
                )
            
            if(inspect.isclass(typ)):
                if(issubclass(typ, rdltypes.UserEnum) or issubclass(typ, rdltypes.UserStruct)):
                    return(typ)
                else:
                    raise RDLCompileError(
                        "Type '%s' is not a struct or enum" % token.text,
                        token
                    )
            else:
                raise RDLCompileError(
                    "Type '%s' is not a struct or enum" % token.text,
                    token
                )
            
        else:
            return(self._DataType_Map[token.type])
    
    def component_def_from_token(self, id_token):
        def_name = id_token.getText()
        comp_def = self.NS.lookup_type(def_name)
        if(comp_def is None):
            raise RDLCompileError(
                "Type '%s' is not defined" % def_name,
                id_token
            )
        if(not issubclass(type(comp_def), comp.Component)):
            raise RDLCompileError(
                "Type '%s' is not a component type" % def_name,
                id_token
            )
        
        return(comp_def)
        
#===============================================================================
# Root meta-component visitor
#===============================================================================
class RootVisitor(ComponentVisitor):
    comp_type = comp.Root
    
    def visitRoot(self, ctx:SystemRDLParser.RootContext):
        self.visitChildren(ctx)
        return(self.component)
    
    
    def define_component(self, body, type_token, def_name, param_defs):
        comp_def = super().define_component(body, type_token, def_name, param_defs)
        
        if(def_name is not None):
            self.component.comp_defs[def_name] = comp_def
        
        return(comp_def)
    
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        # Unpack instance def info from parent
        comp_def, inst_type = self._tmp
        
        if(type(comp_def) != comp.Signal):
            raise RDLCompileError(
                "Instantiation of '%s' components not allowed in the root namespace" % type(comp_def).__name__.lower(),
                ctx.component_inst(0).ID()
            )
        
        return(super().visitComponent_insts(ctx))
    
#===============================================================================
# Field Component visitor
#===============================================================================
class FieldComponentVisitor(ComponentVisitor):
    comp_type = comp.Field
    
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        raise RDLCompileError(
            "Instantiation of components not allowed inside a field definition",
            ctx.component_inst(0).ID()
        )
    
    def check_comp_def_allowed(self, type_token):
        raise RDLCompileError(
            "Definitions of components not allowed inside a reg definition",
            type_token
        )
#===============================================================================
# Reg Component visitor
#===============================================================================
class RegComponentVisitor(ComponentVisitor):
    comp_type = comp.Reg
    
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        # Unpack instance def info from parent
        comp_def, inst_type = self._tmp
        
        if(type(comp_def) not in [comp.Signal, comp.Field]):
            raise RDLCompileError(
                "Instantiation of '%s' components not allowed inside a reg definition" % type(comp_def).__name__.lower(),
                ctx.component_inst(0).ID()
            )
        return(super().visitComponent_insts(ctx))
    
    def check_comp_def_allowed(self, type_token):
        comp_type = self._CompType_Map[type_token.type]
        
        if(comp_type not in [comp.Signal, comp.Field]):
            raise RDLCompileError(
                "Definitions of '%s' components not allowed inside a reg definition" % comp_type.__name__.lower(),
                type_token
            )

#===============================================================================
# Regfile Component visitor
#===============================================================================
class RegfileComponentVisitor(ComponentVisitor):
    comp_type = comp.Regfile
    
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        # Unpack instance def info from parent
        comp_def, inst_type = self._tmp
        
        if(type(comp_def) not in [comp.Signal, comp.Reg, comp.Regfile]):
            raise RDLCompileError(
                "Instantiation of '%s' components not allowed inside a regfile definition" % type(comp_def).__name__.lower(),
                ctx.component_inst(0).ID()
            )
        return(super().visitComponent_insts(ctx))
    
    def check_comp_def_allowed(self, type_token):
        comp_type = self._CompType_Map[type_token.type]
        
        if(comp_type in [comp.Addrmap, comp.Mem]):
            raise RDLCompileError(
                "Definitions of '%s' components not allowed inside a regfile definition" % comp_type.__name__.lower(),
                type_token
            )
#===============================================================================
# Addrmap Component visitor
#===============================================================================
class AddrmapComponentVisitor(ComponentVisitor):
    comp_type = comp.Addrmap
    
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        # Unpack instance def info from parent
        comp_def, inst_type = self._tmp
        
        if(type(comp_def) == comp.Field):
            raise RDLCompileError(
                "Instantiation of 'field' components not allowed inside a addrmap definition",
                ctx.component_inst(0).ID()
            )
        return(super().visitComponent_insts(ctx))

#===============================================================================
# Mem Component visitor
#===============================================================================
class MemComponentVisitor(ComponentVisitor):
    comp_type = comp.Mem
    
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        # Unpack instance def info from parent
        comp_def, inst_type = self._tmp
        
        if(type(comp_def) != comp.Reg):
            raise RDLCompileError(
                "Instantiation of '%s' components not allowed inside a mem definition" % type(comp_def).__name__.lower(),
                ctx.component_inst(0).ID()
            )
        return(super().visitComponent_insts(ctx))
        
    def check_comp_def_allowed(self, type_token):
        comp_type = self._CompType_Map[type_token.type]
        
        if(comp_type in [comp.Field, comp.Reg]):
            raise RDLCompileError(
                "Definitions of '%s' components not allowed inside a mem definition" % comp_type.__name__.lower(),
                type_token
            )
#===============================================================================
# Signal Component visitor
#===============================================================================
class SignalComponentVisitor(ComponentVisitor):
    comp_type = comp.Signal
    
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        raise RDLCompileError(
            "Instantiation of components not allowed inside a signal definition",
            ctx.component_inst(0).ID()
        )
    
    def check_comp_def_allowed(self, type_token):
        raise RDLCompileError(
            "Definitions of components not allowed inside a signal definition",
            type_token
        )
